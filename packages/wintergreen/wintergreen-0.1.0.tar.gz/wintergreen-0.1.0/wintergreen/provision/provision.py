"""
Create a cert and private key for a new device that will connect to AWS IoT.
"""

from os import path
from uuid import uuid4
import json

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from ..file_system import configpath
from ..crypto import serialize_key_cert_pair, generate_csr, generate_signed_cert


def provision(country='US', days=365, key_size=2048, **kwargs):
    """
    Creates a new device key and certificate that is signed by a custom root CA.
    """
    thing_type = kwargs.get('thing_type')
    root_ca_path = kwargs.get('root_ca_path')
    root_ca_key_path = kwargs.get('root_ca_key_path')
    common_name = kwargs.get('common_name', str(uuid4()))
    organization = kwargs.get('organization')
    state = kwargs.get('state')
    locality = kwargs.get('locality')
    unit = kwargs.get('unit')

    if thing_type != None:
        ca_path = path.join(configpath, thing_type, 'rootCA.crt')
        ca_key_path = path.join(configpath, thing_type, 'rootCA.key')
    else:
        if (root_ca_path == None) or (root_ca_key_path == None):
            raise Exception('If thing-type is not provided, --root-ca-path and --root-ca-key-path must be set.')
        ca_path = root_ca_path
        ca_key_path = root_ca_key_path


    with open(ca_path, 'rb') as f:
        serialized_ca_cert = f.read()

    ca_cert = x509.load_pem_x509_certificate(serialized_ca_cert, default_backend())

    with open(ca_key_path, 'rb') as f:
        ca_key = load_pem_private_key(f.read(), None, default_backend())

    csr_pair = generate_csr(key_size, common_name, None, organization, country, state, locality, unit)

    cert = generate_signed_cert(csr_pair['csr'], {'cert': ca_cert, 'key': ca_key}, days)['cert']

    serialized_pair = serialize_key_cert_pair({'cert': cert, 'key': csr_pair['key']})

    output = {
        'deviceCert': serialized_pair['cert'],
        'deviceCertPlusCACert': serialized_pair['cert'] + serialized_ca_cert.decode('utf-8'),
        'deviceKey': serialized_pair['key'],
        'commonName': common_name
    }

    return output