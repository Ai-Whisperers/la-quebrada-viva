#!/usr/bin/env python3
"""
Simple local web server for the RV interactive maps.
Serves the interactive_map/ directory on port 8765.

Usage:
    python3 serve_maps.py
    # Then open http://localhost:8765/ in any browser
"""
import http.server
import socketserver
import os
import sys

PORT = 8765
DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)
    
    def end_headers(self):
        # Disable CORS for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Quieter logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format%args}\n")

if __name__ == '__main__':
    print(f'=' * 60)
    print(f'Riverstone Valley Interactive Maps — Web Server')
    print(f'=' * 60)
    print(f'Serving from: {DIR}')
    print(f'URL: http://localhost:{PORT}/')
    print(f'')
    print(f'Pages:')
    print(f'  /                              - index (all 3 maps)')
    print(f'  /interactive_map.html          - master map')
    print(f'  /water_focus_map.html          - water focus')
    print(f'  /vegetation_focus_map.html     - vegetation focus')
    print(f'')
    print(f'Press Ctrl+C to stop')
    print(f'=' * 60)
    
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nServer stopped.')