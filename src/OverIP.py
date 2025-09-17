import os
import json
import subprocess
import socket as skmng

def logo_print():
    os.system("clear")
    print("▄▖      ▄▖▄▖")
    print("▌▌▌▌█▌▛▘▐ ▙▌")
    print("▙▌▚▘▙▖▌ ▟▖▌ ")
    print()           

def name_request():
    name = input("Insert your Name: ")
    return name

def user_select():
    with open("src/config/config.json", "r") as us:
        data = json.load(us)
    
    print("Memorized Users:\n")
    for i in range(len(data["users"])):
        user = data["users"][i]
        print(f"{user['Name']}: {user['Ip-Number']}")

    sel_user = input("\nWrite the name of the Receiver: ")
    
    for user in data["users"]:
        if user["Name"] == sel_user:
            return user["Ip-Number"]

def classes_select():
    with open("src/config/config.json", "r") as cl:
        data = json.load(cl)

    print("Memorized Classes:\n")
    for i in range(len(data["classes"])):
        cls = data["classes"][i]
        print(f"{cls['Name']}: {cls['Ip']}")
    
    sel_cls = input("\nWrite the name of the Class: ")

    logo_print()
    number = user_select()

    for cls in data["classes"]:
        if(cls["Name"] == sel_cls):
            return f"{cls["Ip"]}{number}"

def port_request():
    port = input("Insert the requested Port: ")
    return port

def subprocess_launch(port):
    
    proc = subprocess.Popen([
        "xterm",
        "-T", "OverIP Listener",
        "-bg", "black",
        "-fg", "white",
        "-fa", "Monospace",
        "-fs", "10",
        "-e", "bash", "-c", f"while true; do nc -l -p {port}; done"
    ])
    return proc

def message_launch(ip, port, name):
    message = input("Message: ")

    if message == "EXIT":
        return 0

    full_message = f"{name}: {message}\n"

    with skmng.socket(skmng.AF_INET, skmng.SOCK_STREAM) as socket_tcp:
        socket_tcp.connect((ip, int(port)))
        socket_tcp.sendall(full_message.encode())

    return 1

def main():
    logo_print()

    ip = classes_select()
    logo_print()
    port = port_request()
    logo_print()
    name = name_request()
    logo_print()

    listener_proc = subprocess_launch(port)

    message_launch(ip, port, name)

    while True:
        if message_launch(ip, port, name) == 0:
            listener_proc.terminate()
            break

while True:
    main()
