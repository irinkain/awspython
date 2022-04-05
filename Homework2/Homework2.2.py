import boto3
import json

s3 = boto3.client("s3")
# დაწერეთ პროგრამა, რომელსაც არგუმენტად გადაეცემა ბაკეტის სახელი.
# პროგრამამ უნდა შეამოწმოს ბაკეტს გააჩნია თუ არა policy. თუ policy უკვე
# არსებობს უნდა დაბეჭდოს რომ policy უკვე არსებოს, წინააღმდეგ შემთხვევაში,
# უნდა შექმნას policy, რომელიც საჯაროდ წვდომადს გახდის ყველა ფაილს /dev და
# /test პრეფიქსების ქვეშ.


def check_if_policy_exists(bucket_name):
    try:
        policy = s3.get_bucket_policy(Bucket=bucket_name)
        policy_str = policy["Policy"]
        if policy_str is None:
            return False
        else:
            return True
    except Exception as ex:
        print(ex)


def create_bucket_policy(bucket_name):
    s3.put_bucket_policy(Bucket=bucket_name, Policy=generate_policy(bucket_name))
    print("Bucket policy created successfully")


def generate_policy(bucket_name):
    policy = {"Version": "2012-10-17",
              "Statement": [
                  {"Sid": "PublicReadGetObject",
                   "Effect": "Allow",
                   "Principal": "*",
                   "Action": "s3:GetObject",
                   "Resource": [f"arn:aws:s3:::{bucket_name}/dev/*", f"arn:aws:s3:::{bucket_name}/test/*"]
                   }
              ]
              }
    return json.dumps(policy)


def main():
    if check_if_policy_exists("irinasnewbucket"):
        print("Sorry! Policy has already exists")
    else:
        create_bucket_policy("irinasnewbucket")


if __name__ == "__main__":
    main()
