# Cyber Station 

import customtkinter as ctk
from bs4 import BeautifulSoup
import requests
import urllib.parse
import re
from collections import deque
import threading
import time
import ctypes
import sys
import platform
import os
sys_type = platform.system()

if sys_type == "Windows":
    # Ensure the script runs as administrator
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

elif sys_type == "Linux":
    # Ensure the script runs with sudo
    if os.geteuid() != 0:  
        print("Error", "This script must be run as root. Please run with sudo.")
        sys.exit()

elif sys_type == "Darwin":  
    # Ensure the script runs with sudo
    if os.geteuid() != 0:
        print("Error", "This script must be run as root. Please run with sudo.")
        sys.exit()

else:
    print("Unknowen System Type...")



class EmailScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Extractor")
        self.root.geometry("800x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.running = False  # Flag to control threads
        self.start_time = None
        self.threads = []

        # Input Fields
        self.url_label = ctk.CTkLabel(root, text="Target URL:")
        self.url_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.url_entry = ctk.CTkEntry(root, width=400, placeholder_text="Enter the target URL")
        self.url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.threads_label = ctk.CTkLabel(root, text="Number of Threads:")
        self.threads_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.threads_entry = ctk.CTkEntry(root, width=100, placeholder_text="10")
        self.threads_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.urls_label = ctk.CTkLabel(root, text="Max URLs to Scan:")
        self.urls_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.urls_entry = ctk.CTkEntry(root, width=100, placeholder_text="100")
        self.urls_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.output_label = ctk.CTkLabel(root, text="Output HTML File:")
        self.output_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.output_entry = ctk.CTkEntry(root, width=300, placeholder_text="emails.html")
        self.output_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Configure grid columns for equal button sizes
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        
        # Buttons
        self.start_button = ctk.CTkButton(root, text="Start", command=self.start_scraper)
        self.start_button.grid(row=4, column=0, padx=10, pady=20, sticky="ew")
        
        self.stop_button = ctk.CTkButton(root, text="Stop", command=self.stop_scraper)
        self.stop_button.grid(row=4, column=1, padx=10, pady=20, sticky="ew")
        
        self.clear_button = ctk.CTkButton(root, text="Clear Screen", command=self.clear_screen)
        self.clear_button.grid(row=4, column=2, padx=10, pady=20, sticky="ew")


        # Execution Log
        self.log_box = ctk.CTkTextbox(root, width=780, height=300, wrap="word", fg_color="#2b2b2b", text_color="#ffffff")
        self.log_box.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Timer
        self.timer_label = ctk.CTkLabel(root, text="Execution Time: 0s")
        self.timer_label.grid(row=6, column=0, columnspan=2, pady=10)

        # Scraper Data
        self.urls = deque()
        self.scraped_urls = set()
        self.emails = set()
        self.lock = threading.Lock()

    def start_scraper(self):
        # Get user input
        target_url = self.url_entry.get().strip()
        num_threads = int(self.threads_entry.get().strip())
        max_urls = int(self.urls_entry.get().strip())
        output_file = self.output_entry.get().strip()
        if not output_file.endswith(".html"):
            output_file += ".html"

        if not target_url or not num_threads or not max_urls:
            self.log("[Error] Please fill in all fields.")
            return

        # Reset and prepare for scraping
        self.running = True
        self.urls = deque([target_url])
        self.scraped_urls = set()
        self.emails = set()
        self.start_time = time.time()

        self.log(f"[Info] Starting with URL: {target_url}")

        # Start threads
        self.threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self.process_url, args=(max_urls, output_file), daemon=True)
            thread.start()
            self.threads.append(thread)

        # Periodically check and update the timer and the GUI
        self.update_timer()

        # Start the progress log
        self.log("[Info] Scraping started...")

    def stop_scraper(self):
        self.running = False
        self.log("[Info] Stopping scraper...")
        for thread in self.threads:
            thread.join(timeout=1)

    def process_url(self, max_urls, output_file):
        while self.running:
            try:
                # Check if there are URLs to process or if we reached the max limit
                with self.lock:
                    if len(self.scraped_urls) >= max_urls:
                        self.running = False
                        break
                    if not self.urls:
                        self.log("[Info] No more URLs to process.")
                        break  # Stop if no more URLs to process
                
                    url = self.urls.popleft()
                    self.scraped_urls.add(url)

                self.log(f"[Processing] {url}")

                # Send HTTP request
                try:
                    response = requests.get(url, timeout=5)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    self.log(f"[Error] {url}: {e}")
                    continue

                # Find emails
                new_emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", response.text))
                with self.lock:
                    self.emails.update(new_emails)

                # Parse links
                soup = BeautifulSoup(response.text, "html.parser")
                for anchor in soup.find_all("a", href=True):
                    link = urllib.parse.urljoin(url, anchor["href"])

                    # Ignore invalid or non-clickable links like '#'
                    if link.startswith('#') or 'javascript' in link.lower():
                        continue

                    self.log(f"[Found Link] {link}")  # Debug statement to log found links
                    with self.lock:
                        if link not in self.urls and link not in self.scraped_urls:
                            self.urls.append(link)

            except Exception as e:
                self.log(f"[Error] {e}")
                continue

        # Once scraping is done, save emails to HTML
        if not self.running:  # Ensure we save when scraper stops
            self.save_emails_to_html(output_file)

    def save_emails_to_html(self, output_file):
        # Generate HTML content with a better design
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Extracted Emails</title>
            <style>
                body {{
                    background-color: #181818;
                    color: #E8E8E8;
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                }}
                h1 {{
                    text-align: center;
                    margin-top: 20px;
                    font-size: 32px;
                }}
                .container {{
                    display: flex;
                    justify-content: center;
                    flex-wrap: wrap;
                    margin-top: 30px;
                }}
                .email {{
                    background-color: #333;
                    color: #fff;
                    border-radius: 5px;
                    padding: 10px;
                    margin: 10px;
                    width: 300px;
                    text-align: center;
                    font-size: 18px;
                    transition: background-color 0.3s ease;
                }}
                .email:hover {{
                    background-color: #555;
                }}
            </style>
        </head>
        <body>
            <h1>Extracted Emails</h1>
            <div class="container">
                {"".join(f"<div class='email'>{email}</div>" for email in sorted(self.emails))}
            </div>
        </body>
        </html>
        """
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        self.log(f"[Info] Emails saved to {output_file}")

    def update_timer(self):
        if self.running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.configure(text=f"Execution Time: {elapsed}s")
            self.root.after(1000, self.update_timer)

    def log(self, message):
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")

    def clear_screen(self):
        """Clear the log box and reset the timer."""
        self.log_box.delete(1.0, "end")  # Clear log box
        self.timer_label.configure(text="Execution Time: 0s")  # Reset the timer


# Run the GUI
root = ctk.CTk()
app = EmailScraperApp(root)
root.mainloop()
