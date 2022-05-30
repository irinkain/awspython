import boto3
from botocore.exceptions import ClientError
import argparse

ec2_client = boto3.client("ec2")


# სატესტოდ მაქვს
# VPC_ID = "vpc-0aa2e50ba7c676d6f"
# Subnet_Id = "subnet-0c0d357852dd04109"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vpc", type=str, help="Vpc id", required=True)
    parser.add_argument("-s", "--subnet", type=str, help="Subnet id", required=True)

    args = parser.parse_args()
    return args


def main_task(vpc_id, subnet_id, key_pair_name):
    response = ec2_client.create_security_group(
        Description='irinas security group',
        GroupName='irinasSG',
        VpcId=vpc_id)
    group_id = response.get("GroupId")
    print("Created security Group Id - ", group_id)
    add_ports_access_sg(group_id)
    print("Adding an ingress rule to a security group finished successfully")
    run_ec2(group_id, subnet_id, key_pair_name)


def add_ports_access_sg(security_group_id):
    response = ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 443,
             'ToPort': 443,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    if response.get("Return"):
        print("Ingress Successfully Set")
    else:
        print("Something went wrong!")


def create_key_pair(key_name):
    response = ec2_client.create_key_pair(
        KeyName=key_name,
        KeyType="rsa",
        KeyFormat="pem"
    )
    key_id = response.get("KeyPairId")
    with open(f"{key_name}.pem", "w") as file:
        file.write(response.get("KeyMaterial"))
    print("Key pair created successfully: Id - ", key_id)
    return key_id


def run_ec2(sg_id, subnet_id, key_pair):
    response = ec2_client.run_instances(
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/sdh",
                "Ebs": {"DeleteOnTermination": True,
                        "VolumeSize": 9,
                        "VolumeType": "gp2",
                        "Encrypted": False},
            },
        ],
        ImageId="ami-015c25ad8763b2f11",
        InstanceType="t3.micro",
        KeyName=key_pair,
        MaxCount=1,
        MinCount=1,
        Monitoring={"Enabled": True},
        UserData="""#!/bin/bash
echo "Hello I am Irina" > irina.txt
""",
        InstanceInitiatedShutdownBehavior="stop",
        NetworkInterfaces=[
            {
                "AssociatePublicIpAddress": True,
                "DeleteOnTermination": True,
                "Groups": [
                    sg_id,
                ],
                "DeviceIndex": 0,
                "SubnetId": subnet_id,
            },
        ],
    )
    for instance in response.get("Instances"):
        instance_id = instance.get("InstanceId")
        print("Instance created successfully: Id - ", instance_id)
    return None


def main():
    args = parse_args()
    key_pair = create_key_pair("irinaskeypair")
    try:
        main_task(args.vpc, args.subnet, key_pair)
    except ClientError as e:
        print(e)
    print("Something went wrong...")


if __name__ == "__main__":
    main()
