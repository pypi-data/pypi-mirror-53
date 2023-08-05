import os
import csv

basepath = os.path.dirname(os.path.abspath(__file__))

def get_home_directory():
    home = os.curdir

    if 'HOME' in os.environ:
        home = os.environ['HOME']
    elif os.name == 'posix':
        home = os.path.expanduser("~/")
    elif os.name == 'nt':
        if 'HOMEPATH' in os.environ and 'HOMEDRIVE' in os.environ:
            home = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    else:
        home = os.environ['HOMEPATH']

    return home

configpath = os.path.join(get_home_directory(), '.wintergreen')

def mkdir(base=".", subdir="tmp"):
    """
    Side Effect!
        Creates a directory in at base/subdir
    """
    directory = os.path.join(base, subdir)
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory

def write_output(output_dir, common_name, output):
    """
    Side Effects!
        Writes deviceKey-<common_name>.key
        Writes deviceCert-<common_name>.crt
        Writes deviceCertPlusCACert-<common_name>.crt
    """
    device_dir = mkdir(base=output_dir, subdir=common_name)
    write_device_key(device_dir, common_name, output)
    write_device_cert(device_dir, common_name, output)
    write_device_combined_cert(device_dir, common_name, output)

def record_output(date, output_dir, generated):
    """
    CommonName = UUID
    DateProvisioned = today, ISO-8601
    CommonName, DateProvisioned
    """
    record_path = os.path.join(output_dir, 'output.csv')
    with open(record_path, 'w') as csvfile:
        fieldnames = ['DateProvisioned', 'CommonName']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for g in generated:
            writer.writerow(
                {
                    'DateProvisioned': date,
                    'CommonName': g,
                }
            )


def write_device_key(device_dir, common_name, output):
    write_file(device_dir, common_name, output, "deviceKey", "key")

def write_device_cert(device_dir, common_name, output):
    write_file(device_dir, common_name, output, "deviceCert", "crt")

def write_device_combined_cert(device_dir, common_name, output):
    write_file(device_dir, common_name, output, "deviceCertPlusCACert", "crt")

def write_file(device_dir, common_name, output, file_name, file_type):
    path = os.path.join(device_dir, '{}-{}.{}'.format(file_name, common_name, file_type))
    with open(path,'w') as myFile:
        myFile.writelines([line for line in output[file_name]])
