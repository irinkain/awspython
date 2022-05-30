import boto3
import argparse

rds_client = boto3.client("rds")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance", type=str, help="Instance id", required=True)
    args = parser.parse_args()
    return args


def create_snapshot(instance_id):
    response = rds_client.create_db_snapshot(
        DBSnapshotIdentifier='IrinasDbSnapshot-1',
        DBInstanceIdentifier=instance_id,
        Tags=[
            {
                'Key': 'Name',
                'Value': 'IrinasSnapshot'
            },
        ]
    )
    print(f"Snapshot created successfully: {response}")


def main():
    args = parse_args()
    create_snapshot(args.instance)
