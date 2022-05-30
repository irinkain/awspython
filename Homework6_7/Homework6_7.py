import boto3

#  დაწერეთ პროგრამა რომელიც შექმნის VPC ს დაარქმევს მას სახელს(tag-ის
# გამოყენებით). პროგრამამ უნდა შექმნას IGW და მიაბას VPC-ს
ec2_client = boto3.client("ec2")


def create_igw_and_attach(vpc_id):
    response = ec2_client.create_internet_gateway()
    igw = response.get("InternetGateway")
    igw_id = igw.get("InternetGatewayId")
    response = ec2_client.attach_internet_gateway(
        InternetGatewayId=igw_id,
        VpcId=vpc_id
    )
    print(f"successfully attached: {response}")
    return igw_id


def create_vpc_and_attach_igw():
    result = ec2_client.create_vpc(CidrBlock="10.0.0.0/16")
    vpc = result.get("Vpc")
    vpc_id = vpc.get("VpcId")
    ec2_client.create_tags(Resources=[vpc_id], Tags=[{"Key": "Name", "Value": "Irina'sVpc"}])
    create_igw_and_attach(vpc_id)


def create_subnet(vpc_id, cidr):
    response = ec2_client.create_subnet(VpcId=vpc_id, CidrBlock=cidr)
    subnet = response.get("Subnet")
    subnet_id = subnet.get("SubnetId")
    ec2_client.create_tags(
        Resources=[subnet_id],
        Tags=[
            {"Key": "Name", "Value": "Irina'sSubnet"},
        ],
    )
    print(subnet_id)


def main():
    create_vpc_and_attach_igw()


if __name__ == "__main__":
    main()
