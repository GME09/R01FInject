import os
import re
import time
import uuid
import importlib
from .lolcat import lolcat
from datetime import datetime, timedelta
import base64
from colorama import Fore, Back, Style, init
init(autoreset=True)
import signal
import json

def handle_sigint(signum, frame):
    lolcat("  \nYou press ( Ctrl+c )to exit. Input ( R01F ) to Run it again\n")
    os._exit(0)

signal.signal(signal.SIGINT, handle_sigint)

def log(message, log_file):
    with open(log_file, 'a') as file:
        file.write(f"{message}\n")
    print(message)
    
def green(text):
    print(f"\033[32;1m{text}\033[0m")

def red(text):
    print(f"\033[31;1m{text}\033[0m")

os.system("clear")

def setup_user():
    back = importlib.import_module("modules.tt")
    with open('/etc/xray/domain') as f:
        domain = f.read().strip()
    with open('/usr/local/etc/xray/org') as f:
        ISP = f.read().strip()
    with open('/usr/local/etc/xray/city') as f:
        CITY = f.read().strip()
    print(f"{Fore.BLUE}{Style.BRIGHT}╔═{Fore.RED}─────────────────────────────────────{Fore.BLUE}═╗")
    print(f"{Fore.RED}┃{Fore.BLUE}         Create a TROJAN account       {Fore.RED} ┃")
    print(f"{Fore.BLUE}╚═{Fore.RED}─────────────────────────────────────{Fore.BLUE}═╝")
    lolcat("Type ( x ) to exit/cancel\n")
    print("")
    user = ""
    while True:
        user = input(" \033[93mUsername: \033[0m").strip()
        if user == "x":
            print(f"\033[93mExiting the TROJAN create process.\033[0m")
            time.sleep(0.5)
            os.system('clear')
            back.trojan_menu()
            return None, None, None
        if len(user) > 20:
            print("\033[91mUsername is too long! Maximum allowed is 20 characters.\033[0m")
            continue
        elif re.match(r'^[a-zA-Z0-9_]+$', user):
            if os.system(f"grep -qw '### {user}' /etc/qos/xray/xrayall.txt") == 0:
                print(f"\033[93m Try again Use another Username.\033[0m \033[91m{user}\033[0m \033[93malready exists\033[0m")
            else:
                print(f" \033[92mConfirmed\033[0m")
                break
        else:
            print(f"\033[91mInvalid username format.\033[0m")
    user_uuid = ""
    while True:
        user_uuid = input(" \033[93mUuid (pass) [Leave blank to auto-generate]: \033[0m").strip()
        if user_uuid == "x":
            print(f"\033[93mExiting the TROJAN create process.\033[0m")
            time.sleep(0.5)
            os.system('clear')
            back.trojan_menu()
            return None, None, None
        if user_uuid == "":
            print("\033[92m UUID is empty. Automatically generate UUID...\033[0m")
            user_uuid = str(uuid.uuid4())
            print(f"\033[92m Automatically generated UUID: {user_uuid}\033[0m")
        if len(user_uuid) <= 7:
            print("\033[91m UUID/pass must be more than 7 characters.\033[0m")
            continue
        try:
            with open('/etc/qos/xray/uuid.txt', 'r') as file:
                existing_uuids = file.read().splitlines()
            if user_uuid in existing_uuids:
                print("\033[91m UUID already exists, please enter a different UUID.\033[0m")
                continue
            print(f"\033[92mUUID/PASS confirmed.\033[0m")
            break
        except FileNotFoundError:
            print("\033[91m If there is an error please contact dev/Community \033[0m")
            break
        except Exception as e:
            print(f"\033[91mIf there is an error please contact dev/Community: {e}\033[0m")
            break
    Quota = ""
    exittol = False
    while not exittol:
        Quota = input(" \033[93mQuota (Limit): \033[0m").strip()
        if Quota == "":
            while True:
                lolcat(f"\nAre you sure to add User {user} with Unlimited Quota? \n")
                opsi = input(f"\033[93mSelect Y to continue, select N to cancel (Y/N):\033[0m").strip()
                if opsi.lower() == "y":
                    Quota = "unlimited"
                    exittol = True
                    print(f" \033[92m Add Unlimited Quota to User {user}\033[0m")
                    break
                elif opsi.lower() == "n":
                    print("\033[93m Cancel User to unlimited\033[0m")
                    break
                else:
                    print("\033[91m What do you do, choose the option that is ordered\033[0m")
        elif Quota.lower() == "x":
            print(f"\033[93mExiting the VMESS create process.\033[0m")
            time.sleep(0.5)
            os.system('clear')
            back.vmess_menu()
            exittol = True
            return None, None, None, None
        elif not re.match(r'^\d+$', Quota):
            print(f"\033[91mPlease enter a valid number.\033[0m")
        else:
            print(f"\033[92mQuota Added: {Quota} GB\033[0m")
            break
    masaaktif = ""
    while True:
        masaaktif = input(" \033[93mExpired (Days): \033[0m").strip()
        if masaaktif == "x":
            print(f"\033[93mExiting the TROJAN create process.\033[0m")
            time.sleep(0.5)
            os.system('clear')
            back.trojan_menu()
            return None, None, None
        elif not re.match(r'^\d+$', masaaktif):
            print(f"\033[91mPlease enter the number correctly.\033[0m")
        else:
            masaaktif_days = int(masaaktif)
            if masaaktif_days > 10000:
                print("\033[91mDuration too large! Maximum allowed is 10000 days.\033[0m")
            else:
                print(f"\033[92mAdded.\033[0m")
                break
    return user, Quota, masaaktif, user_uuid
def trojan_main():
    back = importlib.import_module("modules.tt")
    user, Quota, masaaktif, user_uuid = setup_user()
    uuid_file = '/etc/qos/xray/uuid.txt'
    uuid_dir = os.path.dirname(uuid_file)
    tr_dir = '/etc/qos/xray/trojan.txt'
    all = '/etc/qos/xray/xrayall.txt'
    usage1 = f"/etc/qos/usage/{user}"
    with open('/etc/xray/domain') as f:
        domain = f.read().strip()
    with open('/usr/local/etc/xray/org') as f:
        ISP = f.read().strip()
    with open('/usr/local/etc/xray/city') as f:
        CITY = f.read().strip()
    if user:
        with open('/etc/xray/domain') as f:
            domain = f.read().strip()
        if not os.path.exists(usage1):
            with open(usage1, 'w') as file:
                pass
        if Quota.strip().lower() == "unlimited":
            quota1 = "unlimited"
        elif Quota.isdigit():
            quota1 = str(int(Quota) * 1024 * 1024 * 1024)
        else:
            print("erorororro")
        with open(usage1, "w") as file:
            file.write(quota1)
        hariini = datetime.now()
        masaaktif = int(masaaktif)
        expdate = hariini + timedelta(days=masaaktif)
        expiration_date = expdate.strftime("%Y-%m-%d:%H")
        try:
            if not os.path.exists(uuid_dir):
                print(f"\033[92m Subdirectory does not exist. Creating subdirectory...\033[0m")
                os.makedirs(uuid_dir, exist_ok=True)
            with open(uuid_file, 'a') as file:
                file.write(f"{user_uuid}\n")
        except FileNotFoundError:
            print(f"\033[91mIf there is an error please contact dev/Community.\033[0m")
        except Exception as e:
            print(f"\033[91mIf there is an error please contact dev/Community: {e}\033[0m")
        try:
            if not os.path.exists(tr_dir):
                print(f"\033[92m Subdirectory does not exist. Creating subdirectory...\033[0m")
                os.makedirs(tr_dir, exist_ok=True)
            with open(tr_dir, 'a') as pile:
                pile.write(f"### {user} {expiration_date}\n")
            with open(all, 'a') as f:
                f.write(f"### {user} {expiration_date}\n")
        except FileNotFoundError:
            print(f"If there is an error please contact dev/Community")
        except Exception as e:
            print(f"If there is an error please contact dev/Community : {e}")
        configpath = '/etc/xray/config.json'
        with open(configpath, 'r') as fil3:
            config = json.load(fil3)
        truser = {
            "password": user_uuid,
            "email": user,
            "quota": quota1,
            "expiry": expiration_date
        }
        trgrpc = {
            "password": user_uuid,
            "email": user,
            "expiry": expiration_date
        }
        for inbound in config['inbounds']:
            if inbound['protocol'] == 'trojan':
                inbound['settings']['clients'].append(truser)
                break
        for inbound in config['inbounds']:
            if inbound['protocol'] == 'trojan':
                if inbound['streamSettings']['network'] in ['grpc']:
                    inbound['settings']['clients'].append(trgrpc)
                    break
        with open(configpath, 'w') as gme:
            json.dump(config, gme, indent=2)
        print("\033[91mHa ha ha\033[0m")
        time.sleep(0.5)
        os.system("clear")
        trojan_link1 = (f"trojan://{user_uuid}@{domain}:443?path=/trojan-ws&security=tls&encryption=none&type=ws&sni={domain}&host={domain}#${user}")
        trojan_link2 = (f"trojan://{user_uuid}@{domain}:80?path=/trojan-ws&encryption=none&type=ws&host={domain}#${user}")
        trojan_link3 = (f"trojan://{user_uuid}@{domain}:443?mode=gun&security=tls&encryption=none&type=grpc&serviceName=trojan-grpc&sni=isi_bug#{user}")
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Format Open Clash</title>
</head>
<body style="background: linear-gradient(to bottom right, red 50%, white 50%); color: white; font-family: Arial, sans-serif; text-align: center; padding: 50px;">
    <h1 style="font-size: 3em;"><big>GME VPN TUNNLING</h1>
    <h style="font-size: 1em;">Clik here!!</h>
    <a href="https://wa.me/6281227984353" style="text-decoration: none;">
        <button style="background-color: #3498db; color: white; padding: 20px 30px; border: none; border-radius: 50px; cursor: pointer;">
            <h1><big>Order Vpn</h1>
        </button>
    </a>
    <h1 style="font-size: 1em;">Format Open Clash</h1>
    <div style="margin-top: 50px; background-color: #333; padding: 50px; border-radius: 5px;">
        <pre style="white-space: pre-wrap; word-wrap: break-word; text-align: left; font-size: 8px;">
# Format trojan WS TLS
- name: {user}
  type: trojan
  server: {domain}
  port: 443
  uuid: {user_uuid}
  alterId: 0
  cipher: auto
  udp: true
  tls: true
  skip-cert-verify: true
  servername: {domain}
  network: ws
  ws-opts:
    path: /trojan
    headers:
      Host: {domain}
        </pre>
    </div>
    <div style="margin-top: 20px; background-color: #333; padding: 20px; border-radius: 5px;">
        <pre style="white-space: pre-wrap; word-wrap: break-word; text-align: left; font-size: 8px;">
# Format trojan WS Non TLS
- name: {user}
  type: trojan
  server: {domain}
  port: 80
  uuid: {user_uuid}
  alterId: 0
  cipher: auto
  udp: true
  tls: false
  skip-cert-verify: false
  servername: {domain}
  network: ws
  ws-opts:
    path: /trojan
    headers:
      Host: {domain}
        </pre>
    </div>
    <div style="margin-top: 20px; background-color: #333; padding: 20px; border-radius: 5px;">
        <pre style="white-space: pre-wrap; word-wrap: break-word; text-align: left; font-size: 8px;">
# Format trojan gRPC
- name: {user}
  server: {domain}
  port: 443
  type: trojan
  uuid: {user_uuid}
  alterId: 0
  cipher: auto
  network: grpc
  tls: true
  servername: {domain}
  skip-cert-verify: true
  grpc-opts:
    grpc-service-name: trojan-grpc
        </pre>
    </div>
</body>
</html>"""
        output_path = f"/var/www/html/trojan-{user}.html"
        with open(output_path, 'w') as file:
            file.write(html_content)
        os.system("systemctl restart xray > /dev/null 2>&1")
        os.system("service cron restart > /dev/null 2>&1")
        log_file = f"/etc/xraylog/log-trojan-{user}.txt"
        separator_blue = f"\033[94m━════════════━\033[0m"
        separator_red = f"\033[91m━════════════━\033[0m"
        log(f" {separator_blue} ", log_file)
        log(" DETAIL TROJAN ACCOUNT ", log_file)
        log(f" {separator_red} ", log_file)
        log(f" \033[93mRemarks        :\033[0m \033[92m{user}\033[0m ", log_file)
        log(f" \033[93mQuota          :\033[0m \033[92m{Quota} GB\033[0m ", log_file)
        log(f" \033[93mDomain         :\033[0m \033[92m{domain}\033[0m ", log_file)
        log(f" \033[93mISP            :\033[0m \033[92m{ISP}\033[0m ", log_file)
        log(f" \033[93mRegion         :\033[0m \033[92m{CITY}\033m ", log_file)
        log(f" \033[93mPort TLS/gRPC  :\033[0m \033[92m443, 8443, 2053, 2083, 2087, 2096\033[0m ", log_file)
        log(f" \033[93mPort none TLS  :\033[0m \033[92m80, 2082, 8880, 8080, 2095, 2086, 2052\033[0m ", log_file)
        log(f" \033[93mpasswod       :\033[0m \033[92m{user_uuid}\033[0m ", log_file)
        log(f" \033[93mSecurity       :\033[0m \033[92mauto\033[0m ", log_file)
        log(f" \033[93mNetwork        :\033[0m \033[92mws\033[0m ", log_file)
        log(f" \033[93mPath           :\033[0m \033[92m/trojan-ws\033[0m ", log_file)
        log(f" \033[93mService Name   :\033[0m \033[92m/trojan-grpc\033[0m ", log_file)
        log(f" {separator_blue} ", log_file)
        log(f" \033[93mLink TLS       :\033[0m \033[92m{trojan_link1}\033[0m ", log_file)
        log(f" {separator_red} ", log_file)
        log(f" \033[93mLink none TLS  :\033[0m \033[92m{trojan_link2}\033[0m ", log_file)
        log(f" {separator_blue} ", log_file)
        log(f" \033[93mLink gRPC      :\033[0m \033[92m{trojan_link3}\033[0m ", log_file)
        log(f" {separator_red} ", log_file)
        log(f" \033[93mFormat OpenClash :\033[0m \033[92mhttps://{domain}:81/trojan-{user}\033[0m ", log_file)
        log(f" {separator_blue} ", log_file)
        log(f" \033[93mExpired On     :\033[0m \033[92m{expiration_date}\033[0m", log_file)
        log(f" \033[93mExpiry date\033[0m \033[91m{masaaktif}\033[0m \033[93mdays from\033[0m \033[92m{expiration_date}\033[0m", log_file)
        log(f" {separator_red} ", log_file)
        log(f" 𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔 𝐅𝐎𝐑 𝐔𝐒𝐈𝐍𝐆 𝐑𝟎𝟏𝐅 𝐓𝐔𝐍𝐍𝐄𝐋𝐈𝐍𝐆", log_file)
        lolcat("\n Press Enter to return to create account or type 'x' to exit...\n")
        while True:
            action = input(" \033[93mInput Options:\033[0m ").strip().lower()
            if action == "x":
                print(f"\033[93mExiting the TROJAN create process.\033[0m")
                time.sleep(0.5)
                os.system("clear")
                back.trojan_menu()
                break
            elif action == "":
                os.system("clear")
                trojan_main()
                break
            else:
                print("\033[91mPlease enter 'x' to exit or press Enter to return.\033[0m")