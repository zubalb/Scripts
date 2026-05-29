from netmiko import ConnectHandler
import os
import sys

ip = sys.argv[1]
interface =sys.argv[2]

def connect_and_reset():
    connection = ConnectHandler(
        device_type = "eltex", 
        host = ip,
        username = os.environ.get("log"),
        password = os.environ.get("pass"),
    )
    print(f"Подключение к {ip}:")
    SetIntActive = connection.send_command(f"set int active {interface}")
    IntStatus = connection.send_command(f"show interface status {interface}")
    print(f"Разблокировал: \n {IntStatus}")

connect_and_reset()