import boto3

ec2_client = boto3.client("ec2")


# 1.დაწერეთ პროგრამა რომელიც შექმნის VPC-ს CIDR ბლოკით 10.10.0.0/16. VPC
# დაადეთ ორი თაგი(tag) გასაღებებით Name და Creator. Name თაგში ჩაწერეთ რაც
# გინდათ, ხოლო Creator თაგში ჩაწერეთ თქვენი სახელი. პროგრამამ ეკრანზე უნდა
# დაბეჭდოს შექმნილი VPC-ის იდენტიფიკატორი
def create_vpc_and_add_tags():
    result = ec2_client.create_vpc(CidrBlock="10.0.0.0/16")
    vpc = result.get("Vpc")
    vpc_id = vpc.get("VpcId")
    ec2_client.create_tags(Resources=[vpc_id],
                           Tags=[{"Key": "Name", "Value": "Irina'sVpc"}, {"Key": "Creator", "Value": "Irina"}])
    print(vpc_id)


# 2.დაწერეთ პროგრამა რომელსაც გადაეცემა VPC იდენტიფიკატორი და CIDR
# ბლოკი. პროგრამამ CIDR ბლოკის გამოყენებით უნდა შექმნას ქვე-ქსელი VPC-ში.
# პროგრამამ ეკრანზე უნდა დაბეჭდოს შექმნილი ქვე-ქსელის იდენტიფიკატორი
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


# 3.დაწერეთ პროგრამა რომელსაც არგუმენტად გადაეცემა VPC იდენტიფიკატორი.
# პროგრამამ უნდა შექმნას ინტერნეტ გეითვეი(IGW) და მიაბას VPC-ს. პროგრამამ
# ეკრანზე უნდა დაბეჭდოს შექმნილი IGW-ს იდენტიფიკატორი
def create_igw_and_attach(vpc_id):
    response = ec2_client.create_internet_gateway()
    igw = response.get("InternetGateway")
    igw_id = igw.get("InternetGatewayId")
    response = ec2_client.attach_internet_gateway(
        InternetGatewayId=igw_id,
        VpcId=vpc_id
    )
    print(f"successfully attached: {response}")
    print(igw_id)


# 4.დაწერეთ პროგრამა რომელსაც არგუმენტად გადაეცემა VPC იდენტიფიკატორი.
# პროგრამამ მითითებულ VPC-ში უნდა შექმნას სამარშუტო ცხრილი(Routing table).
# პროგრამამ ეკრანზე უნდა დაბეჭდოს შექმნილი RTB-ის იდენტიფიკატორი.
def create_route_table(vpc_id):
    response = ec2_client.create_route_table(VpcId=vpc_id)
    route_table = response.get("RouteTable")
    route_table_id = route_table.get("RouteTableId")
    print(route_table_id)


# 5.დაწერეთ პროგრამა რომელსაც არგუმენტად გადაეცემა სამარშუტო
# ცხრილი(Routing table)-ის იდენტიფიკატორი და ინტერნეტ გეითვეის
# იდენტიფიკატორი. პროგრამამ უნდა ჩაამატოს გზა სამარშუტო ცხრილში ინტერნეტ
# გეითვეიმდე
def create_route_table_with_route(route_table_id, igw_id):
    response = ec2_client.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw_id,
        RouteTableId=route_table_id,
    )
    print(f"Route succesfully added: {response}")


# 6.დაწერეთ პროგრამა რომელსაც არგუმენტად გადაეცემა ქვე-ქსელის
# იდენტიფიკატორი და სამარშუტო ცხრილის იდენტიფიკატორი. პროგრამამ უნდა
# მიაბას სამარშუტო ცხრილი მიწოდებულ ქვე-ქსელს
def associate_route_table_to_subnet(route_table_id, subnet_id):
    response = ec2_client.associate_route_table(
        RouteTableId=route_table_id,
        SubnetId=subnet_id
    )
    print(f"Route table associated: {response}")

# 7.დაწერეთ ინსტრუქცია თუ როგორ შეიძლება ზემოთ მოცემული პროგრამების
# გამოყენებით შევქმნათ VPC ორი ქვე-ქსელით. ქვე-ქსელებიდან ერთი უნდა იყოს
# Public და ერთი უნდა იყოს Private

# 1. ვქმნით ვპც-ს create_vpc_and_add_tags მეთოდის გამოყენებით
# 2. ვქმნით public subnet -ს create_subnet მეთოდის გამოყენებით
# 3. ვქმნით igw-ს და ვაბამთ vpc -ს create_igw_and_attach მეთოდის გამოყენებით
# 4. ვქმნით სამარშრუტო ცხრილს create_route_table მეთოდის გამოყენებით
# 5. ვქმნით მარშრუტს კონკრეტულ სამარშრუტო ცხრილში create_route_table_with_route მეთოდის გამოყენებით
# 6. ვაბამთ სამარშრუტო ცხრილს ჩვენ ფაბლიქ ქვექსელს associate_route_table_to_subnet მეთოდის გამოყენებით
# 7. ვქმნით კიდევ ერთ საბნეტს private-ს,create_subnet მეთოდის გამოყენებით და ვტოვებთ ასე, რადგან private-ა.
