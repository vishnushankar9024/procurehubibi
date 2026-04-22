# procurehubibi

A minimal Node.js development baseline for this repository.

## Prerequisites

- Node.js 20+ (or any version that supports current Express release)
- npm

## Setup

1. Install dependencies:
   - `npm install`
2. Start the app:
   - `npm run dev`

The server listens on `http://localhost:3000` by default.

## Available endpoints

- `GET /` returns a JSON welcome message.
- `GET /health` returns `{"status":"ok"}`.
