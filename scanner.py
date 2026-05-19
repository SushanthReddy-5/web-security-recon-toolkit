import requests
import socket

target = input("Enter target URL: ")

try:
    response = requests.get(target, timeout=5)

    print("\n[+] Website Status Code:", response.status_code)

    headers = response.headers

    score = 0

    if "X-Frame-Options" not in headers:
        print("[!] Missing X-Frame-Options Header")
    else:
        print("[+] X-Frame-Options Found")
        score += 2

    if "Content-Security-Policy" not in headers:
        print("[!] Missing CSP Header")
    else:
        print("[+] CSP Header Found")
        score += 3

    if "Strict-Transport-Security" not in headers:
        print("[!] HSTS Header Missing")
    else:
        print("[+] HSTS Enabled")
        score += 3

    if "Server" in headers:
        print("[+] Server:", headers["Server"])
        score += 1

    if "X-Powered-By" in headers:
        print("[+] Technology:", headers["X-Powered-By"])
        score += 1

    print(f"\n[+] Security Score: {score}/10")

except Exception as e:
    print("[-] Website Request Error:", e)

print("\n[+] Checking Common Endpoints...\n")

endpoints = [
    "/admin",
    "/login",
    "/dashboard",
    "/backup"
]

for endpoint in endpoints:

    try:
        url = target + endpoint

        r = requests.get(url, timeout=3)

        if r.status_code == 200:
            print(f"[FOUND] {url}")

    except:
        pass

print("\n[+] Scanning Common Ports...\n")

host = target.replace("https://", "").replace("http://", "").split("/")[0]

ports = [21, 22, 80, 443, 3306]

for port in ports:

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((host, port))

        if result == 0:

            print(f"[OPEN] Port {port}")

            try:
                banner = s.recv(1024).decode().strip()

                if banner:
                    print(f"[BANNER] {banner}")

            except:
                pass

        s.close()

    except:
        pass