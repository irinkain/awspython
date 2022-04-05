import boto3
s3 = boto3.client("s3")


# დაწერეთ პროგრამა, რომელსაც არგუმენტებად გადაეცემა ბაკეტის სახელი და
# ფაილის სახელი. პროგრამამ მითითებულ ბაკეტში უნდა ატვირთოს გადმოცემული
# ფაილი

def upload_file(bucket, filename):
    try:
        s3.upload_file(filename, bucket, "Image1.jpg")
        print("File was uploaded successfully")
    except Exception as ex:
        print(f"Something went wrong :( {ex}")


def main():
    upload_file("irinasnewbucket", "img.jpg")


if __name__ == "__main__":
    main()
