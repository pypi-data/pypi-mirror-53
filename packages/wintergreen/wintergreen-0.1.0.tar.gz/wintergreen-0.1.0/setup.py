# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['wintergreen', 'wintergreen.initialize', 'wintergreen.provision']

package_data = \
{'': ['*'], 'wintergreen': ['templates/*']}

install_requires = \
['boto3>=1.9,<2.0',
 'click>=7.0,<8.0',
 'cryptography>=2.6,<3.0',
 'mock>=3.0,<4.0',
 'pytest>=4.5,<5.0']

entry_points = \
{'console_scripts': ['wintergreen = wintergreen.cli:cli']}

setup_kwargs = {
    'name': 'wintergreen',
    'version': '0.1.0',
    'description': 'A tool for dealing with AWS IoT certificates',
    'long_description': '# THIS REPOSITORY IS A WORK IN PROGRESS\n**IF YOU SEE THIS MESSAGE DO NOT UNDER ANY CIRCUMSTANCE DELETE INFRASTRUCTURE HOPING THAT WINTERGREEN CAN REBUILD IT**\nWe\'re working on it.\n\n## Purpose\n\nAutomate device registry in AWS IoT because it sucks. `wintergreen` is a command line utility that provides mechanisms to automate cumbersome tasks related to signing and registering AWS IoT Thing device certificates.\n\n## Install\nThis project uses [poetry](https://poetry.eustace.io/) to manage and install dependencies.\n```\npoetry install\n```\n\nThis will install the required dependencies as well as the `wintergreen` cli, which can be invoked by running `poetry run wintergreen`\n\n\n### Using with direnv\nFollow this [layout_poetry](https://github.com/direnv/direnv/wiki/Python#poetry) example\n\n## Run\n\n## Initialize\nInitialization means\n- Creating a ThingType\n- Creating a RootCA cert/key pair\n- Registering that RootCA with AWS\n- Creating a Just-in-time Provisioning role\n\nExample:\n`poetry run wintergreen init -t my-cool-thing`\nCheck your `~/.wintergreen` directory to see a subdirectory for `my-cool-thing`\n\n```bash\n$  wintergreen init --help\nUsage: wintergreen init [OPTIONS]\n\n  Creates a custom root CA and registers it with the cloud provider for\n  automatic provisioning.\n\nOptions:\n  -t, --thing-type TEXT       AWS IoT thing type  [required]\n  -c, --country TEXT          Country code (2-letter) to use for provisioning\n                              certs i.e. US  [required]\n  -f, --fqdn TEXT             Domain of the organization to use in the CA e.g.\n                              verypossible.com\n  -o, --organization TEXT     Organization name i.e. Very\n  -s, --state TEXT            State or Province code (2-letter) to use for\n                              provisioning certs i.e. TN\n  -l, --locality TEXT         Locality to use for provisioning certs i.e.\n                              Chattanooga\n  -u, --unit TEXT             Organizational unit to use for provisioning\n                              certs i.e. Engineering\n  -d, --root-ca-days INTEGER  Days until CA will expire  [default: 365]\n  -k, --key-size INTEGER      [default: 2048]\n  --log-level TEXT\n  --help                      Show this message and exit.\n\nOutputs:\n{\n    jitpRoleArn: "arn:to:role",\n    rootCACertPath: "${HOME}/.wintergreen/things/Widget/rootCA.crt",\n    rootCAKeyPath: "${HOME}/.wintergreen/things/Widget/rootCA.key",\n    certificateArn:"arn:aws:iot:account:region:cacert/1234"\n}\n```\n\n## Provision a new device\n\nProvisioning a device means generating a certificate/key pair to be used for the device to authenticate with AWS IoT.\n\n```bash\n$ wintergreen provision --help\nUsage: wintergreen provision [OPTIONS]\n\n  Creates a new device key and certificate that is signed by a custom root\n  CA.\n\nOptions:\n  -t, --thing-type TEXT    Same as the thing-type that was chosen in the\n                           `init` step.\n  --root-ca-path PATH      Required if thing-type from a previous run of\n                           `init` is not provided.\n  --root-ca-key-path PATH  Required if thing-type from a previous run of\n                           `init` is not provided.\n  -c, --common-name TEXT   Defaults to a UUIDv4\n  -c, --country TEXT       [required]\n  -o, --organization TEXT\n  -s, --state TEXT\n  -l, --locality TEXT\n  -u, --unit TEXT\n  -d, --days INTEGER       Days until certificate will expire  [default: 365]\n  -k, --key-size INTEGER   [default: 2048]\n  -n, --number             Number of certificates to provision\n  --help                   Show this message and exit.\n\nOutputs:\n{\n    deviceCert: "-----BEGIN CERTIFICATE-----....",\n    deviceCertPlusCACert: "-----BEGIN CERTIFICATE-----....",\n    deviceKey: "------BEGIN RSA PRIVATE KEY----...",\n    commonName: "thing-name"\n}\n```\n\nThese will be written as files scoped by date into your `.wintergreen` directory. If you use the `-n` argument, it will generate a unique uuid for each cert and put all of the certs generated in their own folder. You\'ll also see an output.csv which contains a table of all the certs generated on this run.\n\n### Example provisioning cert example (AWS)\nAfter running the `provision` command the cert/key will be saved in a directory named after the thing-type as `deviceCertPlusCACert-{common_name}.crt` and `deviceKey-{common_name}.key`\nYou\'ll also need to grab the `aws-root-ca.pem` from [AWS Trust](https://www.amazontrust.com/repository/).\nLastly to test, you\'ll need to get your ATS endpoint by running `aws iot describe-endpoint --endpoint-type iot:Data-ATS --region us-east-1`\nIf you have an mqtt client (`brew install mosquitto`) installed, you can verify that a generated device will provision correctly by running something like\n\n```\nmosquitto_pub --cafile aws-root-ca.pem \\\n --cert path/to/deviceCertPlusCACert-my-thing-common-name.crt \\\n --key path/to/deviceKey-my-thing-common-name.key \\\n -h your-endpoint-for-ats.iot.us-east-1.amazonaws.com \\\n --tls-version tlsv1.2 \\\n -p 8883 \\\n -q 1 \\\n -t /my-thing-type/my-thing-common-name/events \\\n -I anyclientID -m "{Hello}" -d\n```\n\nEventually, you will see a device `my-thing-common-name` in the Things menu.',
    'author': 'Dan Lindeman',
    'author_email': 'lindemda@gmail.com',
    'url': 'https://github.com/verypossible/wintergreen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
