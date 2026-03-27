# Voice AI Agent — Gemini 3.1 Flash Live on Vercel

Real-time voice AI agent using **Gemini 3.1 Flash Live** deployed on **Vercel**. A drop-in replacement for Go High Level voice AI at a fraction of the cost.

## Architecture

```
Browser Mic → WebSocket → Gemini 3.1 Flash Live API
                 ↑
         Ephemeral Token
                 ↑
        Vercel Serverless Function (/api/token)
            (keeps API key safe)
```

The browser connects **directly** to Gemini's Live API using short-lived ephemeral tokens. Your Gemini API key never leaves the server.

## Deploy to Vercel

1. Push this repo to GitHub
2. Go to [vercel.com](https://vercel.com) → New Project → Import `googleVoiceAiDemo`
3. Add environment variable: `GEMINI_API_KEY` = your key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
4. Deploy

## Features

- Real-time voice conversation via Gemini 3.1 Flash Live
- Function calling (appointment booking, lead capture, call transfer)
- Audio transcription of both sides
- Ephemeral token auth (API key never exposed to browser)
- Works on mobile browsers

## Project Structure

```
├── api/
│   └── token.py          # Serverless function: mints ephemeral tokens
├── public/
│   └── index.html         # Voice agent UI (connects to Gemini directly)
├── vercel.json            # Vercel routing config
├── requirements.txt       # Python dependencies
└── README.md
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | From Google AI Studio |
| `GEMINI_MODEL` | No | Default: `gemini-3.1-flash-live-preview` |

## Customisation

Edit the `SYSTEM_PROMPT` and `TOOLS` in `public/index.html` to match your client's business. The mock tool handlers (`executeTool` function) should be replaced with real API calls to your booking/CRM system.

## Cost

~$0.02-0.04/min for Gemini API usage. No platform fees. You own everything.

## License

MIT
