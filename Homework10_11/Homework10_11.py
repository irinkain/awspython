import boto3
import argparse
import urllib

ec2_client = boto3.client("ec2")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vpc", type=str, help="Vpc id", required=True)
    parser.add_argument("-s", "--subnet", type=str, help="Subnet id", required=True)
    args = parser.parse_args()
    return args


def get_my_public_ip():
    external_ip = urllib.request.urlopen("https://ident.me").read().decode("utf8")
    return external_ip


def create_security_group(name, vpc_id):
    response = ec2_client.create_security_group(
        Description="irinassg",
        GroupName=name,
        VpcId=vpc_id)
    group_id = response.get("GroupId")
    print("Security Group Id - ", group_id)
    return group_id


def add_http_port_access_sg(security_group_id):
    response = ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    if response.get("Return"):
        print("Ingress Successfully Set")
    else:
        print("Something went wrong!")


def add_ssh_access_sg(sg_id, ip_address):
    ip_address = f"{ip_address}/32"
    response = ec2_client.authorize_security_group_ingress(
        CidrIp=ip_address,
        FromPort=22,
        GroupId=sg_id,
        IpProtocol='tcp',
        ToPort=22,
    )
    if response.get("Return"):
        print("Rule added successfully")
    else:
        print("Rule was not added")


def create_key_pair(key_name):
    response = ec2_client.create_key_pair(
        KeyName=key_name,
        KeyType="rsa",
        KeyFormat="pem"
    )
    return response.get("KeyPairId")


def run_ec2(sg_id, subnet_id, key_pair):
    response = ec2_client.run_instances(
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/sdh",
                "Ebs": {"DeleteOnTermination": False,
                        "VolumeSize": 10,
                        "VolumeType": "gp1",
                        "Encrypted": False},
            },
        ],
        ImageId="ami-015c25ad8763b2f11",
        InstanceType="t2.micro",
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
    sg_id = create_security_group("irinasSGroup", args.vpc)
    add_http_port_access_sg(sg_id)
    add_ssh_access_sg(sg_id, get_my_public_ip())
    key_pair = create_key_pair("irinasKey")
    run_ec2(sg_id, args.subnet, key_pair)


if __name__ == "__main__":
    main()
