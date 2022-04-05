import boto3

s3 = boto3.client("s3")


# დაწერეთ პროგრამა, რომელსაც არგუმენტებად გადაეცემა ბაკეტის სახელი და
# ფაილის სახელი. პროგრამამ მითითებულ ბაკეტში უნდა წაშალოს გადმოცემული
# ფაილი.
def delete_file_from_bucket(bucket, filename):
    try:
        s3.delete_object(Bucket=bucket, Key=filename)
        print("File was deleted successfully")
    except Exception as ex:
        print(f"Something went wrong :( {ex}")


def main():
    delete_file_from_bucket("irinasnewbucket", "img.jpg")


if __name__ == "__main__":
    main()
