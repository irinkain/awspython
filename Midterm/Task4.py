import boto3

s3 = boto3.client("s3")


# დაწერეთ პროგრამა, რომელსაც არგუმენტებად გადაეცემა საცავის სახელი,
# ფაილის სახელი და მოქმედება(download, delete). პროგრამამ მითითებული
# საცავიდან უნდა გადმოწეროს მითითებული ფაილი, თუ მოქმედება არის
# download. პროგრამამ მითითებული საცავიდან უნდა წაშალოს ფაილი, თუ
# მოქმედება არის delete.
def delete_file_from_bucket(bucket, filename):
    try:
        s3.delete_object(Bucket=bucket, Key=filename)
        print("File was deleted successfully")
    except Exception as ex:
        print(f"Something went wrong :( {ex}")


def download_file(bucket, filename, path):
    try:
        s3.download_file(bucket, filename, path)
        print("File was downloaded successfully")
    except Exception as ex:
        print(f"Something went wrong :( {ex}")


def download_or_delete(bucket, file, action):
    if action == "delete":
        delete_file_from_bucket(bucket, file)
    if action == "download":
        download_file(bucket, file, "Midterm")


def main():
    download_or_delete("useririnaaaa", "1.jpg", "delete")


if __name__ == "__main__":
    main()
