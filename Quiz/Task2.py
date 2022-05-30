import boto3

# 2. დაწერეთ პროგრამა რომელიც შექმნის საცავს და მასში ატვირთავს რაღაც ფაილს(3 ქულა)


s3 = boto3.client("s3")


def create_bucket(bucket_name):
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} was created successfully")
    except Exception as ex:
        print(ex)


def upload_file(bucket, filename):
    try:
        s3.upload_file(filename, bucket, "Image1.jpg")
        print("File was uploaded successfully")
    except Exception as ex:
        print(f"Something went wrong :( {ex}")


def main():
    bucket = "irinasnewbucket2"
    create_bucket(bucket)
    upload_file(bucket, "img.jpg")


if __name__ == "__main__":
    main()
