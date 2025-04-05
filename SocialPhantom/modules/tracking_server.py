from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import json
import logging
from typing import Dict

class TrackingRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, tracking_data: Dict, *args, **kwargs):
        self.tracking_data = tracking_data
        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            path = urlparse(self.path).path
            if path.startswith('/track/'):
                email = path.split('/')[2]
                if email in self.tracking_data:
                    self.tracking_data[email]['opened'] = True
                    self.tracking_data[email]['open_time'] = datetime.now()
                    self.log_message(f"Email opened by {email}")
                
                # Return transparent 1x1 pixel
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\x0f\x04\x00\x09\xfb\x03\xfd\x00\x00\x00\x00IEND\xaeB`\x82')
            else:
                self.send_error(404)
        except Exception as e:
            self.log_error(f"Tracking error: {e}")
            self.send_error(500)

def run_tracking_server(tracking_data: Dict, port: int = 8000):
    def handler(*args, **kwargs):
        return TrackingRequestHandler(tracking_data, *args, **kwargs)
    
    server = HTTPServer(('localhost', port), handler)
    logging.info(f"Starting tracking server on port {port}")
    server.serve_forever()
