import boto3

s3 = boto3.client('s3')


# დაწერეთ პროგრამა რომელსაც გადაეცემა საცავის სახელი და დაბეჭდავს
# ყველა ფაილს ამ საცავიდან. ფაილები უნდა დაალაგოთ გასაღების მიხედვით.
def print_sorted_list(bucket):
    res = s3.list_objects(Bucket=bucket)
    output = sorted(res['Contents'], key=lambda i: i['Key'], reverse=True)
    print(output)


if __name__ == '__main__':
    print_sorted_list("useririnaaaa")
