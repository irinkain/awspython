import boto3

ec2_client = boto3.client("ec2")
VPC_ID = 'vpc-0aa2e50ba7c676d6f'
IGW_ID = 'igw-0d4f9e179f55cd51b'
SUB1_ID = 'subnet-0c0d357852dd04109'
SUB2_ID = 'subnet-06145119ecc1b08fb'


def associate_route_table_to_subnet(subnet_id1, subnet_id2):
    route_table_id1 = create_route_tables(VPC_ID, 'public-rtb-1')
    route_table_id2 = create_route_tables(VPC_ID, 'public-rtb-2')
    response1 = ec2_client.associate_route_table(
        RouteTableId=route_table_id1,
        SubnetId=subnet_id1
    )
    response2 = ec2_client.associate_route_table(
        RouteTableId=route_table_id2,
        SubnetId=subnet_id2
    )
    print("Route tables associated successfully")


def create_route_tables(vpc_id, tag):
    response = ec2_client.create_route_table(VpcId=vpc_id)
    route_table = response.get("RouteTable")
    route_table_id = route_table.get("RouteTableId")
    print("Route table id is: ", route_table_id)
    ec2_client.create_tags(
        Resources=[route_table_id],
        Tags=[{"Key": "Name", "Value": tag}, ],
    )
    response = ec2_client.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=IGW_ID,
        RouteTableId=route_table_id,
    )
    return route_table_id


def main():
    associate_route_table_to_subnet


if __name__ == "__main__":
    main()
