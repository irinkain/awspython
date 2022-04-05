import boto3

s3 = boto3.client("s3")


# დაწერეთ პროგრამა, რომელსაც არგუმენტებად გადაეცემა ბაკეტის სახელი და
# ფაილის სახელი. პროგრამამ უნდა ატვირთოს ფაილის ბოლოს წინა ვერსია ახალ
# ვერსიად ბაკეტში


def renew_version(bucket, filename):
    file_versions = []
    keys = []
    result = s3.list_object_versions(Bucket=bucket)
    for ver in result.get("Versions", []):
        if ver.get("Key") == filename:
            keys.append(ver.get("Key"))
            version_id = ver.get("VersionId")
            file_versions.append(version_id)
        else:
            continue
    print(file_versions)
    if len(file_versions) < 2:
        print("Object has only one version")
    else:
        pre_last_version_object = s3.get_object(Bucket=bucket, Key=filename, VersionId=file_versions[1])
        print(pre_last_version_object)
        s3.download_file(
            bucket,
            "newObject",
            "Homework3",
            ExtraArgs={"VersionId": pre_last_version_object})
        upload_file_obj(bucket, "ImageObj")


def upload_file_obj(bucket, filename):
    with open(filename, filename) as file:
        s3.upload_fileobj(file, bucket, filename)


def main():
    renew_version("irinasnewbucket", "Image1.jpg")


if __name__ == "__main__":
    main()
