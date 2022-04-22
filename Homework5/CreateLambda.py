import boto3
from pathlib import Path

client = boto3.client('lambda')
iam = boto3.client('iam')


def convert_zip_to_bytes(zip_file):
    with open(zip_file, 'rb') as file_data:
        bytes_content = file_data.read()
    return bytes_content


# ლამბდა ფუნქციის შექმნის მეთოდი, რომელიც არგუმენტად იღებს ფუნქციის სახელს, iam როლს, ლამბდა ფუნქციის სახელს,
# რომლითაც სერვისი გამოიძახებს ჩვენ ფუნქციას (ეს ჰენდლერი აუცილებელია თუ .zip ფაილს ვტვირთავთ) და იღებს მეოთხე
# პარამეტრს, ზიპ-ფაილს, რომელის ამავდროულად გადაეცემა მეორე მეთოდს და ის გარდაქმნის ბაიტებად ფაილის შიგთავსს.


def create_lambda_function(func_name, iam_role, func_handler, zip_file):
    try:
        client.create_function(
            FunctionName=func_name,
            Runtime='python3.8',
            Role=iam.get_role(RoleName=iam_role)['Role']['Arn'],
            Handler=f'{Path(zip_file).stem}.{func_handler}',
            Code={
                'ZipFile': convert_zip_to_bytes(zip_file)
            },
            Description='New lambda function'
        )
        print(f'function {func_name} has been created successfully')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    create_lambda_function('lambda_img_processor', 'LabRole',
                           'lambda_handler', './lambda_func.zip')
