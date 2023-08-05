"""
Handles crypto functions, creates certs
"""
import datetime
import ipaddress
from uuid import uuid4
from cryptography import x509
from cryptography.x509.oid import NameOID

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

ISSUER = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u"wintergreen"),
])

def serialize_key_cert_pair(pair):
    return {'cert': pair['cert'].public_bytes(serialization.Encoding.PEM).decode('utf-8')
           ,'key': pair['key'].private_bytes(encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()).decode('utf-8')
           }

def serialize_key_csr_pair(pair):
    return {'csr': pair['csr'].public_bytes(serialization.Encoding.PEM).decode('utf-8')
           ,'key': pair['key'].private_bytes(encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()).decode('utf-8')
           }

def private_key(key_size):
    """
    Equivalent to openssl genrsa -out rootCA.key key_size
    """
    return rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=key_size)

def generate_ca_cert(root_ca_days, key_size):
    """
    Equivalent to
    openssl req -x509 -new -nodes -key rootCA.key -sha256 -days root_ca_days -out rootCA.pem
    """
    key = private_key(key_size)
    valid_until = datetime.datetime.utcnow() + datetime.timedelta(days=root_ca_days)
    cert = x509.CertificateBuilder().subject_name(
            ISSUER
        ).issuer_name(
            ISSUER
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            valid_until
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=0)
            ,critical=True
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True
                ,key_encipherment=False
                ,content_commitment=False
                ,data_encipherment=False
                ,key_agreement=False
                ,key_cert_sign=True
                ,crl_sign=True
                ,encipher_only=False
                ,decipher_only=False
                )
            ,critical=True
        ).sign(key, hashes.SHA256(), default_backend())

    return {'cert': cert, 'key': key}

def generate_csr(key_size, common_name, fqdn, organization, country, state, locality, unit):
    """
    Equivalent to
    openssl req -new -key verificationCert.key -out verificationCert.csr -config provisioning.cnf
    """
    key = private_key(key_size)
    csr = x509.CertificateSigningRequestBuilder().subject_name(
        x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u"{common_name}".format(common_name=common_name)),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"{organization}".format(organization=organization)),
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"{country}".format(country=country)),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"{state}".format(state=state)),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"{locality}".format(locality=locality)),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u"{unit}".format(unit=unit))
        ])
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(u"{fqdn}".format(fqdn=fqdn)),
        ]),
        critical=False,
    ).sign(key, hashes.SHA256(), default_backend())
    return {'csr': csr, 'key': key}

def generate_signed_cert(csr, ca_pair, days):
    crt = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        ca_pair['cert'].subject
    ).public_key(
        csr.public_key()
    ).serial_number(
        uuid4().int  # pylint: disable=no-member
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=days)
    ).add_extension(
        extension=x509.KeyUsage(
            digital_signature=True, key_encipherment=True, content_commitment=True,
            data_encipherment=False, key_agreement=False, encipher_only=False, decipher_only=False, key_cert_sign=False, crl_sign=False
        ),
        critical=True
    ).add_extension(
        extension=x509.BasicConstraints(ca=False, path_length=None),
        critical=True
    ).add_extension(
        extension=x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_pair['key'].public_key()),
        critical=False
    ).sign(
        private_key=ca_pair['key'],
        algorithm=hashes.SHA256(),
        backend=default_backend()
    )
    return {'cert': crt}

def generate_cert(ca_key, device_name, days):
    """
    Using this common name
    openssl genrsa -out verificationCert.key 2048 -config provisioning.cnf
    openssl req -new -key verificationCert.key -out verificationCert.csr -config provisioning.cnf
    """
    key = private_key()
    valid_until = datetime.datetime.utcnow() + datetime.timedelta(days=root_ca_days)
    cert = x509.CertificateBuilder().subject_name(
            x509.Name([
                x509.NameAttribute(NameOID.COMMON_NAME, device_name),
            ])
        ).issuer_name(
            ISSUER
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            VALID_UNTIL
        ).add_extension(
            x509.BasicConstraints(ca=False, path_length=None)
            ,critical=False
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True
                ,key_encipherment=True
                ,content_commitment=True
                ,data_encipherment=False
                ,key_agreement=False
                ,key_cert_sign=False
                ,crl_sign=False
                ,encipher_only=False
                ,decipher_only=False
                )
            ,critical=True
        ).sign(ca_key, hashes.SHA256(), default_backend())

    return {'cert': cert, 'key': key}