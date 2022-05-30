import boto3

# დაწერეთ პროგრამა რომელიც დაბეჭდავს თქვენი სისტემიდან ყველა s3
# საცავს რომლის სახელიც იწყება users-ით.

s3 = boto3.client('s3')


def main():
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        if bucket["Name"].startswith("users"):
            print(f'bucket starts with users - {bucket["Name"]}')


if __name__ == '__main__':
    main()
