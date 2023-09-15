import http.server
import socketserver
import socket
import netifaces
import os
from datetime import datetime

def get_ip_address(interface_name):
    try:
        return netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0]['addr']
    except (ValueError, KeyError, IndexError):
        return None


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        if self.html_format:
            self.send_header("Content-type", "text/html")
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        
        # Get the IP address
        ip_address = get_ip_address('enX0')   # ec2
        if not ip_address:
          ip_address = get_ip_address('wlan0') # home network etc
        if not ip_address:
            ip_address = socket.gethostbyname(socket.gethostname())
        
        # Get current system time
        current_time = datetime.now().strftime('%H:%M:%S')
        try:
            hn = os.uname()[1]
        except:
            hn = "some windows box"
        
        # Construct the message
        if self.html_format:
            message = f"<h2>This is {hn}, IP {ip_address}</h2>"
            message += f"<p>The current system time is {current_time}</p>"
            message += "<h2>Request:</h2>"
            message += "<p><tt>"
            message += self.requestline
            message += "</tt></p>"
        else:
            message = f"{hn}, IP {ip_address} at {current_time} for {self.requestline}"
        
        self.wfile.write(message.encode('utf-8'))

    # Make sure the server responds to other HTTP methods (e.g., POST, PUT) in the same way
    do_POST = do_GET
    do_PUT = do_GET
    do_DELETE = do_GET
    html_format = False

if __name__ == "__main__":
    PORT = 8000
    Handler = MyHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
