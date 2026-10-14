import http.server
import socketserver
import urllib.request
import json
import os
import sys

PORT = 5173
OLLAMA_HOST = "http://127.0.0.1:11434"

class VaultAuditHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/health':
            try:
                with urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=5) as resp:
                    models_data = json.loads(resp.read().decode('utf-8'))
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "status": "online",
                        "ollama": True,
                        "models": [m['name'] for m in models_data.get('models', [])]
                    }).encode('utf-8'))
            except Exception as e:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "offline_ollama",
                    "ollama": False,
                    "error": str(e)
                }).encode('utf-8'))
            return

        # Default static file routing
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/extract':
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_body.decode('utf-8'))
                prompt = data.get('prompt', '')
                model = data.get('model', 'llama3.2:3b')

                system_prompt = (
                    "You are VaultAudit AI, an expert zero-knowledge accounting & receipt auditor. "
                    "Analyze the provided invoice, receipt, or billing document text. "
                    "Output strictly valid JSON matching this schema with no markdown code fences, comments, or extra text:\n"
                    "{\n"
                    '  "merchant": "string",\n'
                    '  "invoice_number": "string or null",\n'
                    '  "date": "YYYY-MM-DD or string",\n'
                    '  "total_amount": 0.00,\n'
                    '  "currency": "USD, EUR, GBP, INR, etc.",\n'
                    '  "tax_amount": 0.00,\n'
                    '  "category": "Software / SaaS, Travel, Hardware, Meals & Entertainment, Office Supplies, Freelance Contractor, Cloud Hosting, Legal / Professional, Utilities, or Other",\n'
                    '  "line_items": [\n'
                    '    {"description": "item name", "quantity": 1, "unit_price": 0.00, "total": 0.00}\n'
                    '  ],\n'
                    '  "payment_method": "Credit Card, Bank Wire, PayPal, Apple Pay, Cash, or Other",\n'
                    '  "tax_deductible": true,\n'
                    '  "confidence_score": 0.98,\n'
                    '  "audit_notes": "1-2 sentence concise justification of tax deductibility and expense classification"\n'
                    "}"
                )

                ollama_payload = {
                    "model": model,
                    "system": system_prompt,
                    "prompt": f"Extract financial details from this document:\n\n{prompt}",
                    "stream": False,
                    "format": "json",
                    "options": {
                        "temperature": 0.1
                    }
                }

                req = urllib.request.Request(
                    f"{OLLAMA_HOST}/api/generate",
                    data=json.dumps(ollama_payload).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req, timeout=120) as resp:
                    resp_data = json.loads(resp.read().decode('utf-8'))
                    ollama_raw_response = resp_data.get('response', '{}')

                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "success": True,
                        "raw": ollama_raw_response,
                        "model": model,
                        "eval_duration_ms": resp_data.get('eval_duration', 0) // 1000000
                    }).encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": False,
                    "error": str(e)
                }).encode('utf-8'))
            return

        super().do_POST()

def run_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), VaultAuditHandler) as httpd:
        print(f"VaultAudit Server running securely at http://localhost:{PORT}")
        sys.stdout.flush()
        httpd.serve_forever()

if __name__ == '__main__':
    run_server()
