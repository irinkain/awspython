import boto3

s3 = boto3.client("s3")
resource = boto3.resource('s3')


# 1. დაწერეთ პროგრამა რომელიც საცავში არსებულ ყველა ფაილს გადმოწერს.(2 ქულა)
def download_file(bucket, filename, path="Quiz"):
    try:
        s3.download_file(bucket, filename, path)
        print("File was downloaded successfully")
    except Exception as ex:
        print(f"Something went wrong :( {ex}")


def main():
    bucket = "irinasnewbucket"
    my_bucket = resource.Bucket(bucket)
    for my_bucket_object in my_bucket.objects.all():
        download_file(bucket, my_bucket_object.key, my_bucket_object.key)


if __name__ == "__main__":
    main()
