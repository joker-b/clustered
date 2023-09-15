import http.server
import socketserver
import socket
from datetime import datetime

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        
        # Get the IP address
        ip_address = socket.gethostbyname(socket.gethostname())
        
        # Get current system time
        current_time = datetime.now().strftime('%H:%M:%S')
        
        # Construct the message
        message = f"This is IP {ip_address}, the current system time is {current_time}"
        
        self.wfile.write(message.encode('utf-8'))

    # Make sure the server responds to other HTTP methods (e.g., POST, PUT) in the same way
    do_POST = do_GET
    do_PUT = do_GET
    do_DELETE = do_GET

if __name__ == "__main__":
    PORT = 8000
    Handler = MyHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
