import boto3
import json

IAM = boto3.client('iam')

TRUST_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
            "Service": "iot.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

def create_jitp_role(project_name):
    try:
        response = IAM.create_role(
            RoleName='{project_name}-JITPRole'.format(project_name=project_name),
            AssumeRolePolicyDocument=json.dumps(TRUST_POLICY),
            Description='Just-in-time-provisioning Role for AWS IoT for {project_name}'.format(project_name=project_name),
        )
        role_name = response.get("Role", {}).get("RoleName", None)
        role_arn = response.get("Role", {}).get("Arn", None)

        managed_policies = [
            "arn:aws:iam::aws:policy/service-role/AWSIoTThingsRegistration",
            "arn:aws:iam::aws:policy/service-role/AWSIoTLogging",
            "arn:aws:iam::aws:policy/service-role/AWSIoTRuleActions"
        ]

        for policy in managed_policies:
            IAM.attach_role_policy(RoleName=role_name, PolicyArn=policy)
        return {"role_name": role_name, "role_arn": role_arn}

    except IAM.exceptions.EntityAlreadyExistsException as e:
        response = IAM.get_role(RoleName='{project_name}-JITPRole'.format(project_name=project_name))
        role_name = response.get("Role", {}).get("RoleName", None)
        role_arn = response.get("Role", {}).get("Arn", None)
        return {"role_name": role_name, "role_arn": role_arn}

    except Exception as e:
        raise