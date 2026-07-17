import http.server
import socketserver
import os
import datetime

PORT = 8080
LOG_FILE = "logs/allgemein.txt"

class KneipeHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Erlaubt Vercel-Anfragen, Daten an deinen Server zu senden
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        # Antwort für Browser-Sicherheits-Checks
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path.endswith('.js'):
            self.extensions_map['.js'] = 'application/javascript'
        elif self.path.endswith('.html'):
            self.extensions_map['.html'] = 'text/html'
            
        # Logging-Logik
        client_ip = self.client_address[0]
        # Falls die Anfrage von Vercel weitergeleitet wird
        forwarded_for = self.headers.get('X-Forwarded-For')
        if forwarded_for:
            client_ip = forwarded_for.split(',')[0]

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.path in ['', '/', '/index.html', '/api/log']:
            try:
                os.makedirs('logs', exist_ok=True)
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(f"[{timestamp}] Visit from IP: {client_ip} -> {self.path}\n")
            except Exception:
                pass
                
        if self.path == '/api/log':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Logged")
            return

        super().do_GET()

if __name__ == "__main__":
    os.makedirs('logs', exist_ok=True)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), KneipeHandler) as httpd:
        print(f"=== Brommy Kneipe Server running on Port {PORT} ===")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass