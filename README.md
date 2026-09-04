# ConsentCast

ConsentCast is a local phishing-awareness simulation for cybersecurity learning and classroom education. It demonstrates why camera-permission prompts and embedded links should be treated carefully, using a clearly identified, consent-based webcam broadcast.

**Author:** Zaim Sheali  
**GitHub:** [zaim-tech](https://github.com/zaim-tech)  
**Instagram:** [@king_zaim001](https://instagram.com/king_zaim001)

## Disclaimer

This project is provided only for authorized cybersecurity awareness, training, and learning. It must not be used to create deceptive phishing pages, impersonate a person or organization, collect images, or access a camera without informed permission.

Use it only on devices, accounts, and networks that you own or are explicitly authorized to test. The author is not responsible for misuse, damage, privacy violations, or illegal activity resulting from this software.

## Installation

Clone the repository first:

```bash
git clone https://github.com/zaim-tech/ConsentCast.git
cd ConsentCast
```

### Windows

Open PowerShell or Command Prompt and run:

```powershell
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirement.txt
py main.py
```

### Linux and macOS

Open a terminal and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirement.txt
python3 main.py
```

### Termux on Android

Install Termux from a trusted source, then run:

```bash
pkg update
pkg install python git
git clone https://github.com/zaim-tech/ConsentCast.git
cd ConsentCast
python -m pip install -r requirement.txt
python main.py
```

### Supported Platforms

ConsentCast supports platforms that can run Python, Flask, and a modern browser:

- Windows 10 or newer
- Linux distributions with Python 3.10 or newer
- macOS with Python 3.10 or newer
- Android through Termux

The local server binds to `127.0.0.1`. Camera permission works in modern browsers such as Chrome, Edge, Firefox, and Safari. Use `localhost` or `127.0.0.1` for camera access because browsers restrict camera permissions on ordinary insecure remote addresses.

## Requirements

- Python 3.10 or newer
- Flask
- Colorama

Install the dependencies:

```bash
pip install -r requirement.txt
```

## Run

Start the launcher:

```bash
python main.py
```

The launcher provides these options:

- `1` starts ConsentCast after asking for the iframe URL.
- `2` installs Cloudflared when it is available for your platform.
- `3` exits the launcher.

After choosing option `1`, enter a valid `http://` or `https://` URL. Then open:

- [Camera page](http://127.0.0.1:5000/) to grant camera permission and start the local broadcast.
- [Live viewer](http://127.0.0.1:5000/cam) to view the broadcast.

The entered URL is displayed in the iframe on the camera page. Some websites prevent iframe embedding with security headers; that is expected browser behavior.

The launcher also offers a localhost-only mode and an optional Cloudflare Tunnel mode. Use a tunnel only in an authorized, controlled awareness exercise because it makes the service reachable beyond your computer.

## Privacy and Safety

- Camera access is requested by the browser and requires user approval.
- Audio is not requested.
- Frames are held in server memory only and are not written to disk.
- The server binds to `127.0.0.1` in local mode.
- Image downloads require an explicit action from the viewer page.

## Prevention Guidance

- Do not grant camera or microphone permission unless you recognize and trust the website.
- Check the address bar for misspellings, unexpected domains, and insecure links.
- Be cautious with urgent messages asking you to open a link, install software, or enable device access.
- Review camera and microphone permissions regularly and revoke unused access.
- Keep your browser, operating system, and security software updated.
- Use multi-factor authentication and report suspicious links.
- If a page unexpectedly requests camera access, close it and visit the organization through its official website.

## Benefits

- Demonstrates how permission prompts can appear in social-engineering scenarios.
- Provides a safe way to practice identifying suspicious links and permission requests.
- Supports demonstrations without recording to disk or requesting audio.
- Helps teams build browser-permission, phishing-reporting, and incident-response awareness.

## Project Files

- `main.py`: launcher, URL prompt, and optional tunnel helper.
- `cam.py`: local Flask server and in-memory MJPEG stream.
- `templates/cam.html`: camera permission and broadcast source page.
- `templates/index.html`: live viewer page.
- `requirement.txt`: Python dependencies.

## Author

Created by Zaim Sheali for responsible cybersecurity education and awareness.
