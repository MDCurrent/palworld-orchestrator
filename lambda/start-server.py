import boto3

def lambda_handler(event, context):
    instance_id = 'your-instance-id-here'

    # Initialize the EC2 client
    ec2 = boto3.client('ec2')

    # Check the status of the EC2 instance
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instances = response['Reservations'][0]['Instances']
    instance = instances[0]
    status = instance['State']['Name']

    # If the instance is stopped, start it
    if status == 'stopped':
        print("Starting EC2 instance...")
        # ec2.start_instances(InstanceIds=[instance_id])
        return {
            'statusCode': 200,
            'body': "EC2 instance started"
        }

    # If the instance is already running, just return true
    else:
        print("EC2 instance is already running")
        return {
            'statusCode': 200,
            'body': True
        }