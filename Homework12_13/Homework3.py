import boto3
import argparse

rds_client = boto3.client("rds")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance", type=str, help="Instance id", required=True)
    args = parser.parse_args()
    return args


def increase_storage(identifier):
    response = rds_client.modify_db_instance(
        DBInstanceIdentifier=identifier,
        AllocatedStorage=123
    )
    print(f"RDS - {identifier} increased storage successfully")


def main():
    args = parse_args()
    increase_storage(args.instance)


if __name__ == "__main__":
    main()
