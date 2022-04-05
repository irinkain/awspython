import boto3

s3 = boto3.client("s3")


# დაწერეთ პროგრამა, რომელსაც არგუმენტად გადაეცემა ბაკეტის სახელი.
# პროგრამამ უნდა შეამოწმოს ბაკეტი არსებობს თუ არა. თუ არსებობს უნდა
# წაშალოს, თუ არ არსებობს დაბეჭდოს რომ ბაკეტი არ არსებობს

def delete_bucket_if_exists(bucket):
    if bucket_exists(bucket):
        s3.delete_bucket(Bucket=bucket)
        print("Bucket has deleted successfully")
    else:
        print("Bucket does not exists")


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


def main():
    delete_bucket_if_exists("irinasnewbucket")


if __name__ == "__main__":
    main()
