'''
Create a root CA, just-in-time provisioning role, and registration config on AWS IoT.
'''
import json
import os
from os import path

import boto3
from cryptography.hazmat.primitives import serialization

from .jitp_role import create_jitp_role
from ..crypto import \
    generate_ca_cert, \
    serialize_key_cert_pair, \
    generate_csr, \
    serialize_key_csr_pair, \
    generate_signed_cert
from ..file_system import basepath, configpath, get_home_directory


def init(thing_type, country='US', days=365, key_size=2048, log_level='DEBUG', **kwargs):
    """
    Creates a custom root CA and registers it with the cloud provider for automatic provisioning.
    """
    fqdn = kwargs.get('fqdn')
    organization = kwargs.get('organization')
    state = kwargs.get('state')
    locality = kwargs.get('locality')
    unit = kwargs.get('unit')

    root_ca_directory = path.join(configpath, thing_type)

    if path.isdir(root_ca_directory):
        raise Exception('A root CA for this thing type is already present at ' + root_ca_directory)

    IOT = boto3.client('iot')

    root_pair = generate_ca_cert(days, key_size)

    # aws iot get-registration-code
    # TODO: Make this client cloud-provider agnostic
    registration_code = IOT.get_registration_code().get("registrationCode", None)

    # Using this registration_code as common name
    csr_pair = generate_csr(key_size, registration_code, fqdn, organization, country, state, locality, unit)

    verification_cert = generate_signed_cert(csr_pair['csr'], root_pair, days)

    # This only happens on AWS
    jitp_role = create_jitp_role("wintergreen")

    registration_config = generate_registration_config(thing_type, jitp_role["role_arn"])

    serialized_ca_pair = serialize_key_cert_pair(root_pair)
    serialized_verification_pair = serialize_key_cert_pair({'cert': verification_cert['cert'], 'key': csr_pair['key']})

    ca_response = IOT.register_ca_certificate(
        caCertificate=serialized_ca_pair['cert'],
        verificationCertificate=serialized_verification_pair['cert'],
        setAsActive=True,
        allowAutoRegistration=True,
        registrationConfig=registration_config
    )

    logging_options_response = IOT.set_v2_logging_options(
        roleArn=jitp_role['role_arn'],
        defaultLogLevel=log_level
    )

    thing_type_response = IOT.create_thing_type(
        thingTypeName=thing_type
    )

    os.makedirs(root_ca_directory)

    root_ca_cert_path = path.join(root_ca_directory, 'rootCA.crt')
    root_ca_key_path = path.join(root_ca_directory, 'rootCA.key')

    with open(root_ca_cert_path, 'w') as f:
        f.write(serialized_ca_pair['cert'])

    with open(root_ca_key_path, 'w') as f:
        f.write(serialized_ca_pair['key'])

    output = {
        'thingTypeName': thing_type_response['thingTypeName'],
        'thingTypeArn': thing_type_response['thingTypeArn'],
        'thingTypeId': thing_type_response['thingTypeId'],
        'jitpRoleArn': jitp_role['role_arn'],
        'rootCACertPath': root_ca_cert_path,
        'rootCAKeyPath': root_ca_key_path,
        'certificateArn': ca_response['certificateArn']
    }

    IOT.create_thing_type(thingTypeName=thing_type)

    return output

def generate_registration_config(thing_type, role_arn):
    with open(path.join(basepath, 'templates', 'policy.json'), 'r') as policy:
        json_policy = json.loads(policy.read())

    with open(path.join(basepath, 'templates', 'provisioning.json'), 'r') as provisioning_file:
        pf = json.loads(provisioning_file.read())

    pf["Resources"]["thing"]["Properties"]["ThingTypeName"] = thing_type
    pf["Resources"]["policy"]["Properties"]["PolicyDocument"] = json.dumps(json_policy)

    return {
        "roleArn": role_arn,
        "templateBody": json.dumps(pf)
    }

