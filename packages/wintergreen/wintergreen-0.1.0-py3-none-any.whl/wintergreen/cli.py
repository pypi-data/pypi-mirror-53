"""
Entrypoint for the Wintergreen CLI
"""
import datetime
import json
import os
from uuid import uuid4, UUID

import click

from .initialize import init as init_impl
from .provision import provision as provision_impl
from .file_system import write_output, mkdir, record_output, configpath

basepath = os.path.dirname(os.path.abspath(__file__))

@click.group()
def cli():
    pass

@click.command()
@click.option('-t', '--thing-type', required=True, help='AWS IoT thing type')
@click.option('-c', '--country', required=True, type=str, help='Country code (2-letter) to use for provisioning certs i.e. US', default='US')
# @click.option('--template', help='Optional path to custom just-in-time provisioning template https://docs.aws.amazon.com/iot/latest/developerguide/jit-provisioning.html')
# @click.option('-p', '--policy', help='Optional path to custom aws iot policy https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html')
@click.option('-f', '--fqdn', help='Domain of the organization to use in the CA e.g. verypossible.com')
@click.option('-o', '--organization', help='Organization name i.e. Very')
@click.option('-s', '--state', type=str, help='State or Province code (2-letter) to use for provisioning certs i.e. TN')
@click.option('-l', '--locality', type=str, help='Locality to use for provisioning certs i.e. Chattanooga')
@click.option('-u', '--unit', type=str, help='Organizational unit to use for provisioning certs i.e. Engineering')
@click.option('-d', '--days', type=int, show_default=True, default=365, help='Days until CA will expire')
@click.option('-k', '--key-size', type=int, show_default=True, default=2048)
@click.option('--log-level', type=str, default='DEBUG')
def init(thing_type, country, fqdn, organization, state, locality, unit, days, key_size, log_level):
    output = init_impl(
        thing_type,
        country,
        fqdn=fqdn,
        organization=organization,
        state=state,
        locality=locality,
        unit=unit,
        days=days,
        key_size=key_size,
        log_level=log_level
    )

    click.echo(json.dumps(output, indent=4))

@click.command()
@click.option('-t', '--thing-type', help='Same as the thing-type that was chosen in the `init` step.')
@click.option('--root-ca-path', type=click.Path(), help='Required if thing-type from a previous run of `init` isn\'nt provided.')
@click.option('--root-ca-key-path', type=click.Path(), help='Required if thing-type from a previous run of `init` isn\'nt provided.')
@click.option('-c', '--common-name', default=str(uuid4()), help='Defaults to a UUIDv4')
@click.option('-c', '--country', required=True, default='US')
@click.option('-o', '--organization')
@click.option('-s', '--state')
@click.option('-l', '--locality')
@click.option('-u', '--unit')
@click.option('-d', '--days', help='Days until certificate will expire', type=int, default=365, show_default=True)
@click.option('-k', '--key-size', type=int, show_default=True, default=2048)
@click.option('-n', '--number', type=int, show_default=True, default=1, help='Number of certificates to provision')
@click.option('-p', '--print-output', type=bool, default=False, help='Print results to console?')
def provision(thing_type, root_ca_path, root_ca_key_path, common_name, country, organization, state, locality, unit, days, key_size, number, print_output):
    date = datetime.datetime.utcnow().isoformat()
    dated_dir = os.path.join(thing_type, date)
    output_dir = mkdir(base=configpath, subdir=dated_dir)
    if number > 1 and not is_uuid(common_name):
        click.echo("Skipping redundant cert creations, forcing n=1")
        number = 1

    generated = []
    for n in range(number):
        # We need to change the common_name when generating more than one cert
        if n > 0:
            common_name = str(uuid4())
        output = provision_impl(
            country,
            thing_type=thing_type,
            root_ca_path=root_ca_path,
            root_ca_key_path=root_ca_key_path,
            common_name=common_name,
            organization=organization,
            state=state,
            locality=locality,
            unit=unit,
            days=days,
            key_size=key_size
        )
        generated.append(common_name)
        write_output(output_dir, common_name, output)
        if print_output:
            click.echo(json.dumps(output, indent=4))
    click.echo("Generated {0} certificate(s)".format(len(generated)))
    record_output(date, output_dir, generated)

def is_uuid(common_name):
    try:
        UUID(common_name)
        return True
    except ValueError:
        return False

cli.add_command(init)
cli.add_command(provision)

if __name__ == "__main__":
    cli()
