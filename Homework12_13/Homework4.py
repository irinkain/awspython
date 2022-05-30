import boto3
import argparse

dynamodb = boto3.resource("dynamodb")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region", type=str, help="Region name", required=True)
    args = parser.parse_args()
    return args


def get_all_tables(reg_name):
    response = dynamodb.list_global_tables(
        RegionName=reg_name
    )
    print(response)
    return response.get("TableNames")


def main():
    args = parse_args()
    get_all_tables(args.region)


if __name__ == "__main__":
    main()
