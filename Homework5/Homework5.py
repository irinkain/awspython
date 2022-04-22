import boto3

s3 = boto3.client("s3")
client = boto3.client('lambda')


def create_s3_trigger(bucket, func_name):
    configs = []
    extensions = ['.png', '.jpg', '.jpeg']
    for extension in extensions:
        configs.append({
            'LambdaFunctionArn': client.get_function(
                FunctionName=func_name)['Configuration']['FunctionArn'],
            'Events': [
                's3:ObjectCreated:*'
            ],
            'Filter': {
                'Key': {
                    'FilterRules': [
                        {
                            'Name': 'suffix',
                            'Value': extension
                        },
                    ]
                }
            }
        }, )
    try:
        grant_permission(func_name, bucket)
        s3.put_bucket_notification_configuration(
            Bucket=bucket,
            NotificationConfiguration={
                'LambdaFunctionConfigurations': configs,
            }
        )
        print(f'{func_name} has been added to {bucket} successfully')
    except Exception as e:
        print(e)


# ფერმიშენის მინიჭება, რომ უფლება გვქონდეს ლამბდა ფუნქციის გამოძახების
# ვაპირებდი ფოოლისის გაწერასს, მაგრამ - Lambda does not support adding policies to version $LATEST.

def grant_permission(function_name, bucket_name):
    client.add_permission(
        FunctionName=function_name,
        StatementId='1',
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn=f'arn:aws:s3:::{bucket_name}',
    )


if __name__ == '__main__':
    create_s3_trigger('irinasnewbucket', 'lambda_img_processor')
