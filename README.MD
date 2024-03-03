## PalWorld Server Management

This repository contains two AWS Lambda functions that can be used to manage a PalWorld server.

# Start Server Function

The start-server function starts the PalWorld server when invoked via API Gateway. It takes a single parameter, the Docker image to use for the server.

# Check Network Function

The check-network function is triggered by an EventBridge rule that monitors network activity on the PalWorld server. Using Event Bridge Schedule Expression, the check-network function is invoked and checks if it has been more than an hour since the last login. If it has, the function stops the EC2 instance


