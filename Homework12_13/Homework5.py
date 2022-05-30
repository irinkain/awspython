import boto3
import argparse

dynamodb = boto3.resource("dynamodb")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--table", type=str, help="Table name", required=True)
    args = parser.parse_args()
    return args


def get_table_info(name):
    response = dynamodb.query(
        TableName=name,
        Select='ALL_ATTRIBUTES' | 'ALL_PROJECTED_ATTRIBUTES')
    with open("info.pem", "w") as file:
        file.write(response)


def main():
    args = parse_args()
    get_table_info(args.table)


if __name__ == "__main__":
    main()
