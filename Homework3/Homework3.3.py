import boto3

s3 = boto3.client("s3")


# დაწერეთ პროგრამა, რომელსაც არგუმენტებად გადაეცემა ბაკეტის სახელი,
# გადმოსაწერი ფაილის სახელი და სადაც უნდა ჩაიწეროს ფაილი. პროგრამამ
# მითითებული ბაკეტიდან უნდა გადმოწეროს გადმოსაწერი ფაილი და ჩაწეროს
# დანიშნულების ფაილში. თუ პროგრამას არ გადაეცა არგუმენტი სადაც უნდა
# ჩაიწეროს ფაილი, ნაგულისხმევად ჩაწეროს მიმდინარე დირექტორიაში.

def download_file(bucket, filename, path="Homework3"):
    try:
        s3.download_file(bucket, filename, path)
        print("File was downloaded successfully")
    except Exception as ex:
        print(f"Something went wrong :( {ex}")


def main():
    download_file("irinasnewbucket", "Image1.jpg")


if __name__ == "__main__":
    main()
