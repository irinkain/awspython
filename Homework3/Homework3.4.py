import boto3

s3 = boto3.client("s3")


# დაწერეთ პროგრამა, რომელსაც არგუმენტად გადაეცემა ბაკეტის სახელი.
# პროგრამამ მითითებულ ბაკეტში უნდა აღმოაჩნოს ყველა ფაილი და დააჯგუფოს
# მათ გაფართოებების მიხედვით. პროგრამის შედეგი უნდა იყოს ეკრანზე დაბეჭდილი
# გაფართოება - რაოდენობა ჩანაწერები. მაგალითად, თუ ბაკეტშ არის შემდეგი
# ფაილები:
# image.jpg
# demo.csv
# users.csv
# პროგრამის შედეგი იქნება:
# jpg - 1
# csv - 2

def sort_objects(bucket):
    extension_list = []
    result = s3.list_objects(Bucket=bucket)
    for obj in result.get("Contents", []):
        keys = obj.get("Key")
        try:
            key, value = keys.split(".")
        except ValueError:
            print("Object has no extension")
            continue
        else:
            extension_list.append(value)

    uniquelist = unique(extension_list)
    for el in uniquelist:
        print(f"{el} - {extension_list.count(el)}")


def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def main():
    sort_objects("irinasnewbucket")


if __name__ == "__main__":
    main()


#Type-თი რომ ჰქონდეს ფილტრი object -ს, კარგი იქნებოდა..
