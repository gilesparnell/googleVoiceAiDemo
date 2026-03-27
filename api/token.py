"""
POST /api/token — Mints a short-lived ephemeral token for the Gemini Live API.

The browser calls this endpoint, receives a token, and connects
directly to Gemini via WebSocket. The real API key never leaves the server.
"""

import json
import os
import datetime
from http.server import BaseHTTPRequestHandler
from google import genai


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-live-preview")


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            client = genai.Client(
                api_key=GEMINI_API_KEY,
                http_options={"api_version": "v1alpha"},
            )

            now = datetime.datetime.now(tz=datetime.timezone.utc)

            token = client.auth_tokens.create(
                config={
                    "uses": 1,
                    "expire_time": now + datetime.timedelta(minutes=30),
                    "new_session_expire_time": now + datetime.timedelta(minutes=2),
                    "http_options": {"api_version": "v1alpha"},
                }
            )

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "token": token.name,
                        "model": GEMINI_MODEL,
                        "expires_in_seconds": 1800,
                    }
                ).encode()
            )

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": str(e)}).encode()
            )

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        """Health check."""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(
            json.dumps({"status": "ok", "model": GEMINI_MODEL}).encode()
        )
