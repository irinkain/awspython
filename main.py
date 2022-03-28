import boto3

s3 = boto3.client('s3')


def main():
    response = s3.list_buckets()
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')
        if bucket["Name"].startswith("prod"): {
            print(f'bucket starts with prod - {bucket["Name"]}')
        }


if __name__ == '__main__':
    main()
