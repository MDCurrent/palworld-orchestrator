import boto3
import time

def lambda_handler(event, context):
    instance_id = 'your-instance-id-here'

    # Create a client object for EC2
    ec2 = boto3.client('ec2')
    
    # Create a CloudWatch client
    cloudwatch = boto3.client('cloudwatch')

    # Define the time range for which we want to check network activity
    start_time = int(time.time()) - 3600 # 1 hour ago
    end_time = int(time.time()) # current time

    # Get the network interfaces for the instance
    response = ec2.describe_instances(InstanceIds=[instance_id])
    
    # Get the status of EC2 instance
    instances = response['Reservations'][0]['Instances']
    instance = instances[0]
    status = instance['State']['Name']
            
    if status == 'stopped':
        return {
            'statusCode': 200,
            'body': "EC2 instance already stopped"
        }

    
    # Retrieve network metrics for the past 1 hour
    response = cloudwatch.get_metric_statistics(
        MetricName='NetworkOut',
        Namespace='AWS/EC2',
        Dimensions=[{
            'Name': 'InstanceId',
            'Value': instance_id
        }],
        StartTime=start_time,
        EndTime=end_time,
        Period=300, # 5 minutes
        Statistics=['Average']
    )
    # Extract the average network usage for the past 1 hour
    average_usage = response['Datapoints'][-1]['Average']
    print(f'average_usage: {average_usage}')
    
    # Check if the average network usage is below a certain threshold (e.g., 10%)
    if average_usage < 10:
        print("Network activity has been low for 1 hour")
        # Take appropriate action here, such as sending an alert or scaling resources
        response = ec2.stop_instances(InstanceIds=[instance_id])
        return {
            'statusCode': 200,
            'body': f'Instance stopped due to lack of network activity'
        }
    else:
        print("Network activity is within normal limits")
        return {
                'statusCode': 200,
                'body': f'Instance has had network activity in the last hour'
            }
