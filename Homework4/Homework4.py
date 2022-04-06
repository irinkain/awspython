import mimetypes

import boto3
import json

s3 = boto3.client('s3')
WebsiteConfiguration = {
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}
Region = "us-east-1"


def guess_type(path):
    mimetype, _ = mimetypes.guess_type(path)
    if mimetype is None:
        return "binary/octet-stream"
    return mimetype


def enable_static_website_hosting(bucket):
    s3.put_bucket_website(
        Bucket=bucket,
        WebsiteConfiguration=WebsiteConfiguration
    )
    print(f"http://{bucket}.s3-website-{Region}.amazonaws.com")


def upload_files_to_bucket(bucket):
    filename = ['index.html', 'error.html']
    for file in filename:
        data = open(file, "rb")
        s3.put_object(Body=data,
                      Bucket=bucket,
                      Key=file,
                      ContentType=guess_type(file))


def create_bucket_policy(bucket):
    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'AddPermission',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': "arn:aws:s3:::%s/*" % bucket
        }]
    }
    bucket_policy = json.dumps(bucket_policy)
    s3.put_bucket_policy(Bucket=bucket, Policy=bucket_policy)


def create_bucket(bucket_name):
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} was created successfully")
    except Exception as ex:
        print(ex)


def main():
    bucket_name = "irinasnewbucket"
    create_bucket(bucket_name)
    create_bucket_policy(bucket_name)
    enable_static_website_hosting(bucket_name)
    upload_files_to_bucket(bucket_name)


if __name__ == "__main__":
    main()
