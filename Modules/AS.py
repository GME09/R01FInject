import subprocess
import importlib
import time
import signal
import os
from datetime import datetime, timedelta
from .lolcat import lolcat
def handle_sigint(signum, frame):
    lolcat("  \nYou press ( Ctrl+c )to exit. Input ( R01F ) to Run it again\n")
    os._exit(0)

signal.signal(signal.SIGINT, handle_sigint)

def log(message, log_file):
    with open(log_file, 'a') as file:
        file.write(f"{message}\n")
    print(message)

def create_ssh():
    back = importlib.import_module("modules.mmxsh")

    with open('/etc/xray/domain', 'r') as f:
        domen = f.read().strip()
    with open('/usr/local/etc/xray/org', 'r') as f:
        ISP = f.read().strip()
    with open('/usr/local/etc/xray/city', 'r') as f:
        CITY = f.read().strip()

    print("\033[34m╔═\033[0m\033[31m─────────────────────────────────────\033[0m\033[34m═╗\033[0m")
    print("\033[31m┃\033[0m \033[1;31;44;1m         Create SSH Account          \033[0m\033[31m ┃\033[0m")
    print("\033[34m╚═\033[0m\033[31m─────────────────────────────────────\033[0m\033[34m═╝\033[0m")
    lolcat("\nPress enter to continue, enter (X) to Cancel. Press (Ctrl+c) to Exit.\n")
    print("")

    while True:
        login = input(" \033[93mUsername:\033[0m ").strip()
        if login.lower() == "x":
            print("\033[93mExiting the SSH creation process.\033[0m")
            time.sleep(0.5)
            os.system("clear")
            back.ssh_menu()
            return
        if login == "root":
            os.system("clear")
            print(f" \033[91m Bapak Luu tuh Di root\nOrang Tololl ya... Masukin username dan password pake nama root\033[0m")
            time.sleep(3.0)
            back.ssh_menu()
            return
        if len(login) > 20:
            print("\033[91mUsername is too long! Maximum allowed is 20 characters.\033[0m")
            continue
        if login in [user.split(":")[0] for user in os.popen("cat /etc/passwd").readlines()]:
            print("\033[31mUsername already exists. Please choose a different username.\033[0m")
        else:
            print("\033[32mUsername available\033[0m")
            break

    while True:
        password = input(" \033[93mPassword:\033[0m ").strip()
        if password.lower() == "x":
            print(" \033[93mExiting the SSH creation process.\033[0m")
            time.sleep(0.5)
            os.system("clear")
            back.ssh_menu()
            return
        if password == "root":
            os.system("clear")
            print(f" \033[91m Bapak Luu tuh Di root\nOrang Tololl ya.... Masukin username dan password pake nama root\033[0m")
            time.sleep(3.0)
            back.ssh_menu()
            return
        if not password:
            print(" \033[91mPlease enter a valid password\033[0m")
        else:
            print(" \033[32mPassword Added Successfully\033[0m")
            break

    while True:
        try:
            masaaktif = input(" \033[93mExpired (Days):\033[0m ").strip()
            if masaaktif.lower() == "x":
                print(" \033[93mExiting the SSH creation process.\033[0m")
                time.sleep(0.5)
                os.system("clear")
                back.ssh_menu()
                return
            masaaktif_days = int(masaaktif)
            if masaaktif_days > 10000:
                print(" \033[91mDuration too large! Maximum allowed is 10000 days.\033[0m")
            else:
                print(" \033[32mValid Input\033[0m")
                break
        except ValueError:
            print(" \033[91mPlease enter the number correctly.\033[0m")

    ip = subprocess.getoutput("curl -sS ifconfig.me")
    time.sleep(1)

    expire_date = (datetime.now() + timedelta(days=masaaktif_days)).strftime('%Y-%m-%d')
    subprocess.run(["useradd", "-e", expire_date, "-s", "/bin/false", "-M", login])

    try:
        subprocess.run(f"echo '{login}:{password}' | chpasswd", shell=True, check=True)
        print("\033[32mPassword set successfully!\033[0m")
    except subprocess.CalledProcessError:
        print("\033[31mFailed to set password\033[0m")
        return

    exp = subprocess.getoutput(f"chage -l {login} | grep 'Account expires' | awk -F': ' '{{print $2}}'")
    os.system("clear")
    log_file = f"/etc/xraylog/log-ssh-{login}.txt"
    log(f"### {login} {exp}", "/etc/qos/ssh/sshadmin.txt")

    log("\033[34m╒══════════════════════════╕\033[0m", log_file)
    log("  \033[0;33;44;1m    SSH Account Detail    \033[0m", log_file)
    log("\033[31m╘══════════════════════════╛\033[0m", log_file)
    log(f" \033[92mUsername    :\033[0m\033[93m {login}\033[0m", log_file)
    log(f" \033[92mPassword    :\033[0m\033[93m {password}\033[0m", log_file)
    log(f" \033[92mSsh Akun    :\033[0m\033[93m {domen}:isiport@{login}:{password}\033[0m", log_file)
    log("\033[34m════════════════════════\033[0m", log_file)
    log(f" \033[92mIP          :\033[0m\033[93m {ip}\033[0m", log_file)
    log(f" \033[92mHost        :\033[0m\033[93m {domen}\033[0m", log_file)
    log(f" \033[92mISP         : \033[0m\033[93m{ISP}\033[0m", log_file)
    log(" \033[92mOpenSSH     :\033[0m\033[93m 22\033[0m", log_file)
    log(" \033[92mDropbear    :\033[0m\033[93m 109, 69, 143\033[0m", log_file)
    log(" \033[92mSSH WS      :\033[0m\033[93m 80, 8880, 8080, 2082, 2095\033[0m", log_file)
    log(" \033[92mSSH SSL WS  :\033[0m\033[93m 443, 8443, 2083, 2053, 2096\033[0m", log_file)
    log(" \033[92mSSL/TLS     :\033[0m\033[93m 222, 777\033[0m", log_file)
    log(" \033[92mUDPGW       :\033[0m\033[93m 7100-7900\033[0m", log_file)
    log(" \033[92mUDP COSTUM  :\033[0m\033[93m 1-65535, 10000-10105\033[0m", log_file)
    log("\033[31m════════════════════════\033[0m", log_file)
    log(f" \033[93mExpired On  :\033[0m \033[91m{exp}\033[0m", log_file)
    log(f" \033[93mYour Add Days :\033[0m \033[91m{masaaktif_days} \033[0m\033[93mDays\033[0m", log_file)
    log("\033[34m════════════════════════\033[0m", log_file)
    log(" \033[92m𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔 𝐅𝐎𝐑 𝐔𝐒𝐈𝐍𝐆 𝐑𝟎𝟏𝐅 𝐓𝐔𝐍𝐍𝐄𝐋𝐈𝐍𝐆\033[0m", log_file)

    lolcat("\nPress enter to continue, enter (X) to Cancel. Press (Ctrl+c) to Exit.\n")
    while True:
        action = input(" \033[93mInput Options: \033[0m").strip()
        if action.lower == "x":
          print(" \033[93mExiting the SSH creation process.\033[0m")
          time.sleep(0.5)
          os.system("clear")
          back.ssh_menu()
          break
        elif action == "":
           os.system("clear")
           create_ssh()
           break
        else:
           print(" \033[91mPlease enter 'x' to exit or press Enter to return.\033[0m")