import boto3
import time
import paramiko

def lambda_handler(event, context):

    instance_id = 'i-palworldInstanceId'

    # Initialize the EC2 client
    ec2 = boto3.client('ec2', 'us-east-1')

    # Check the status of the EC2 instance
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instances = response['Reservations'][0]['Instances']
    instance = instances[0]
    status = instance['State']['Name']

    # If the instance is stopped, start it
    if status == 'stopped':
        print("Starting EC2 instance...")
        ec2.start_instances(InstanceIds=[instance_id])
        
        while True:
            response = ec2.describe_instances(InstanceIds=[instance_id])
            state = response['Reservations'][0]['Instances'][0]['State']['Name']
            if state == 'running':
                time.sleep(10)
                break
            time.sleep(10)
        
        print(response['Reservations'][0]['Instances'][0]['PublicIpAddress'])
        ip_address = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        
        private_key = paramiko.Ed25519Key.from_private_key_file('palworld_server.pem')

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address, username='ubuntu', pkey=private_key)
        # Execute commands sequentially
        try:
            #Update the game
            stdin, stdout, stderr = ssh.exec_command("./update_palworld.sh")
            stdout_lines = stdout.readlines()
            stderr_lines = stderr.readlines()
            print("update command stdout:", stdout_lines)
            print("update command stderr:", stderr_lines)

            # Start game server with nohup
            stdin, stdout, stderr = ssh.exec_command("./start_palworld.sh", timeout=2)
            
            # Close SSH connection
            ssh.close()

            print("Ok we actually started the server")
            
            return {
                'statusCode': 200,
                'body': f'Palworld started- IP: {ip_address}:8211'
            }
        except Exception as e:
            print("Error:", e)
            return {
                'statusCode': 500,
                'body': 'Error starting game server'
            }

    # If the instance is already running, just return the 
    else:
        ip_address = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        print("EC2 instance is already running")
        return {
            'statusCode': 200,
            'body': f'Palworld is running- IP: {ip_address}:8211'
        }