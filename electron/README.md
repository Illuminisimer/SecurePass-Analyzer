# Electron Frontend

This folder contains the Electron frontend scaffold for the SecurePass Analyzer application.

## Setup

1. Install packages:
   ```bash
   cd electron
   npm install
   ```
2. Start the Electron app:
   ```bash
   npm start
   ```

## Notes

- The Electron UI calls the backend API at `http://127.0.0.1:8000/api`.
- Start the backend before launching Electron.
- The frontend currently supports user login/register, vault creation, entry creation, and password decryption dialogs.
