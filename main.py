import requests
import json
import concurrent.futures
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# User input for target URL
TARGET_URL = input(Fore.CYAN + "Enter the target URL (e.g., http://example.com/): " + Style.RESET_ALL).strip()
URLS_FILE = "urls.txt"
OUTPUT_FILE = "correct.json"
THREADS = 50  # Number of concurrent requests

# Load URLs from file
with open(URLS_FILE, "r") as file:
    urls = [line.strip() for line in file if line.strip()]

# Store valid URLs
valid_urls = []

def check_url(url):
    full_url = f"{TARGET_URL}{url}"
    try:
        response = requests.get(full_url, timeout=5)
        if response.status_code == 200:
            print(Fore.GREEN + f"[+] Found: {full_url}" + Style.RESET_ALL)
            return full_url
        else:
            print(Fore.YELLOW + f"[-] {full_url} -> {response.status_code}" + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[!] Error requesting {full_url}: {e}" + Style.RESET_ALL)
    return None

# Use multithreading for faster execution
with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
    results = list(executor.map(check_url, urls))

# Filter out None values
valid_urls = [url for url in results if url]

# Save results to JSON
with open(OUTPUT_FILE, "w") as file:
    json.dump(valid_urls, file, indent=4)

print(Fore.CYAN + f"\n[*] Done! Valid URLs saved to {OUTPUT_FILE}" + Style.RESET_ALL)