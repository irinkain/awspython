import boto3

# დაწერეთ პროგრამა, რომელსაც არგუმენტად გადაეცემა ბაკეტის სახელი.
# პროგრამამ უნდა შეამოწმოს ბაკეტი არსებობს თუ არა. თუ არსებობს უნდა
# დაწეროს რომ ბაკეტი უკვე არსებობს, თუ არ არსებობს უნდა შექმნას ის.
s3 = boto3.client("s3")


def make_bucket_if_not_exists(bucket):
    if bucket_exists(bucket):
        print("Bucket has already exists")
    else:
        create_bucket(bucket)


def bucket_exists(bucket_name):
    try:
        response = s3.head_bucket(Bucket=bucket_name)
    except s3.exceptions.ClientError as ex:
        print(ex)
        return False
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        return True
    return False


def create_bucket(bucket_name):
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} was created successfully")
    except Exception as ex:
        print(ex)


def main():
    make_bucket_if_not_exists("irinasnewbucket")


if __name__ == "__main__":
    main()
