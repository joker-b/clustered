import boto3
import logging

# Configure logging
logging.basicConfig(filename='instance_log.txt', level=logging.INFO)

# Define regions, availability zones, and other configurations
regions = ["eu-west-1", "us-east-1", "us-east-2", "us-west-1"]
zones = ["a", "b", "c"]
ami_ids = {"eu-west-1": "ami-xxxxxx", "us-east-1": "ami-yyyyyy", "us-east-2": "ami-zzzzzz", "us-west-1": "ami-aaaaaa"}
vpc_ids = {"eu-west-1": "vpc-xxxxxx", "us-east-1": "vpc-yyyyyy", "us-east-2": "vpc-zzzzzz", "us-west-1": "vpc-aaaaaa"}
sg_ids = {"eu-west-1": "sg-xxxxxx", "us-east-1": "sg-yyyyyy", "us-east-2": "sg-zzzzzz", "us-west-1": "sg-aaaaaa"}
subnet_ids = {"eu-west-1a": "subnet-xxxxxx", "eu-west-1b": "subnet-yyyyyy", "eu-west-1c": "subnet-zzzzzz", ...}
snapshot_ids = {"eu-west-1": "snap-xxxxxx", "us-east-1": "snap-yyyyyy", "us-east-2": "snap-zzzzzz", "us-west-1": "snap-aaaaaa"}

def launch_instances(region, zone, cluster_name):
    ec2 = boto3.client('ec2', region_name=region)
    ami_id = ami_ids[region]
    sg_id = sg_ids[region]
    subnet_id = subnet_ids[region + zone]

    try:
        response = ec2.run_instances(
            ImageId=ami_id,
            MinCount=4,
            MaxCount=4,
            InstanceType='m7i.large',
            KeyName='my-key',
            SecurityGroupIds=[sg_id],
            SubnetId=subnet_id,
            Placement={
                'AvailabilityZone': region + zone,
                'GroupName': cluster_name,
                'Tenancy': 'default'
            },
            EfaSpecifications=[{'Enabled': True}]
        )

        instance_ids = [instance['InstanceId'] for instance in response['Instances']]
        logging.info(f"Launched instances {instance_ids} in {region}{zone}")

        # Attach EBS volume to the first instance
        snapshot_id = snapshot_ids[region]
        volume_response = ec2.create_volume(
            AvailabilityZone=region + zone,
            SnapshotId=snapshot_id
        )
        volume_id = volume_response['VolumeId']

        ec2.attach_volume(
            VolumeId=volume_id,
            InstanceId=instance_ids[0],
            Device='/dev/sdf'
        )

        # Log instance details
        for instance_id in instance_ids:
            instance_details = ec2.describe_instances(InstanceIds=[instance_id])
            public_ip = instance_details['Reservations'][0]['Instances'][0]['PublicIpAddress']
            private_ip = instance_details['Reservations'][0]['Instances'][0]['PrivateIpAddress']
            logging.info(f"Instance {instance_id}: Public IP - {public_ip}, Private IP - {private_ip}")

        return True

    except Exception as e:
        logging.error(f"Failed to launch instances in {region}{zone}: {e}")
        return False

# Main loop
for region in regions:
    for zone in zones:
        for cluster in ['A', 'B', 'C', 'D']:
            cluster_name = f"cluster{cluster}"
            if launch_instances(region, zone, cluster_name):
                print(f"Successfully launched instances for {cluster_name} in {region}{zone}")
                break  # Remove this line if you want to continue in other regions/zones after a successful launch

