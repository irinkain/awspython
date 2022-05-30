import boto3
import argparse

ec2_client = boto3.client("ec2")
rds_client = boto3.client("rds")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vpc", type=str, help="Vpc id", required=True)
    parser.add_argument("-i", "--instance", type=str, help="Instance id", required=True)
    args = parser.parse_args()
    return args


def create_security_group(name, vpc_id):
    response = ec2_client.create_security_group(
        Description="irinassg",
        GroupName=name,
        VpcId=vpc_id)
    group_id = response.get("GroupId")
    print("Security Group Id - ", group_id)
    return group_id


def create_postgres_instance(sg_id):
    response = rds_client.create_db_instance(
        DBName='postgres',
        DBInstanceIdentifier='demo-pg-db-1',
        AllocatedStorage=60,
        DBInstanceClass='db.t4g.micro',
        Engine='mysql',
        MasterUsername='postgres',
        MasterUserPassword='strongrandompassword',
        VpcSecurityGroupIds=[
            sg_id,
        ],
        BackupRetentionPeriod=7,
        Port=5432,
        MultiAZ=False,
        EngineVersion='13.5',
        AutoMinorVersionUpgrade=True,
        # Iops=123, # Necessary when StorageType is 'io1'
        PubliclyAccessible=True,
        Tags=[
            {
                'Key': 'Name',
                'Value': 'First RDS'
            },
        ],
        StorageType='gp2',
        EnablePerformanceInsights=True,
        PerformanceInsightsRetentionPeriod=7,
        DeletionProtection=False,
    )
    _id = response.get("DBInstance").get("DBInstanceIdentifier")
    print(f"Instance {_id} was created")


def main():
    args = parse_args()
    sg_id = create_security_group("irinasSg", args.vpc)
    create_postgres_instance(sg_id)


if __name__ == "__main__":
    main()
