import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class CodespaceRequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/log':
            # Dein bestehender Visit-Logger Code bleibt hier!
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Logged")

    def do_POST(self):
        if self.path == '/api/bewertung':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            neue_bewertung = json.loads(post_data.decode('utf-8'))
            
            # Pfad zur bewertungen.js
            filepath = 'components/bewertungen.js'
            
            # Standardliste falls Datei leer oder kaputt ist
            aktuelle_bewertungen = []
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Wir extrahieren das JSON-Array aus dem Export-String
                    try:
                        json_str = content.split('=', 1)[1].strip().rstrip(';')
                        aktuelle_bewertungen = json.loads(json_str)
                    except:
                        aktuelle_bewertungen = []

            # Neue Bewertung vorne anfügen
            aktuelle_bewertungen.insert(0, neue_bewertung)
            
            # Datei neu schreiben
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"export const bewertungenListe = {json.dumps(aktuelle_bewertungen, ensure_ascii=False, indent=4)};")
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Erfolgreich gespeichert")

# Server starten
if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), CodespaceRequestHandler)
    print("Server läuft auf Port 8080...")
    server.serve_forever()