## PalWorld Server Management

This repository contains two AWS Lambda functions that can be used to manage a PalWorld server.

# Start Server EC2

copy pemfile into your orchestrator ec2 instance 

```scp -i your_pem.pem palworld_server.pem ec2-user@ip_address:/home/ec2-user```

copy the server.py and start_game_server.py

```nohup python3 server.py > output.log 2>&1 &```

set up nginx to reverse proxy the site 

set an A DNS record on your domain to the orchestrator IP

# Check Network Function

The check-network function is triggered by an EventBridge rule that monitors network activity on the PalWorld server. Using Event Bridge Schedule Expression, the check-network function is invoked and checks if it has been more than 15 since the last login, using network activity as a proxy. If it has, the function stops the EC2 instance

# Shell Scripts

Just a couple of small shell scripts I threw into the Palworld Server to help the SSH commands be simpler. nothing crazy there.
