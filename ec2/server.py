from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Import your existing function for starting the game server
from start_game_server import lambda_handler

# Define a custom request handler
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set response headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Call your existing Lambda handler function
        response = lambda_handler({}, None)

        # Write the response back to the client
        self.wfile.write(json.dumps(response).encode('utf-8'))

# Define the server address and port
server_address = ('', 8000)  # Use an empty string for the hostname to listen on all available interfaces
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

# Start the server
print('Starting server...')
httpd.serve_forever()
