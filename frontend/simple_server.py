#!/usr/bin/env python3
"""
Simple HTTP server to serve static HTML with proper cache control headers
This eliminates all React development server caching issues
"""

import http.server
import socketserver
import os
import sys
from urllib.parse import urlparse

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add cache control headers to prevent caching
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        # Always serve index.html for any route (SPA behavior)
        if self.path == '/' or not os.path.exists('.' + self.path):
            self.path = '/index.html'
        
        # Add timestamp to prevent browser caching
        if self.path.endswith('.html') or self.path.endswith('.js') or self.path.endswith('.css'):
            self.path += f'?t={int(__import__("time").time())}'
        
        return super().do_GET()

    def log_message(self, format, *args):
        # Custom log format
        sys.stderr.write(f"[{self.date_time_string()}] {format % args}\n")

if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', 3000))
    
    # Change to the directory containing index.html
    os.chdir('/app/public')
    
    with socketserver.TCPServer(("0.0.0.0", PORT), NoCacheHTTPRequestHandler) as httpd:
        print(f"Server running at http://0.0.0.0:{PORT}")
        print("Serving static files with no-cache headers")
        httpd.serve_forever()
