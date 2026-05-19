from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
import getpass
import json

def get_device_type(vendor):
    if vendor == "cisco":
        return  "cisco_ios_telnet"
    elif vendor == "huawei":
        return "huawei_telnet"
    else:
        return "Неизвестный вендор"

def get_command(vendor):
    num_port = input("Укажите номер порта в формате (x/x):")
    if vendor == "cisco":
        return (f"interface FastEthernet{num_port}")
    elif vendor == "huawei":
        return (f"interface GigabitEthernet{num_port}")
    else:
        return "Неизвестный вендор:"
    
def connect_and_reset(device, command):
    connection = ConnectHandler(
        device_type=get_device_type(device['vendor']),
        port=device['telnet_port'],
        host= device['ip'],
        username=device['username'],
        password=device['password'],
    )
    print(f"Подключился к: {device['ip']}")
    connection.send_config_set([command, "shutdown", "no shutdown"])
    connection.disconnect()
try:
    with open("devices.json", "r") as file:
        data = json.load(file)
    for device in data:
            command = get_command(device['vendor'])
            connect_and_reset(device, command)
except FileNotFoundError:
    print("Error! Файл не найден!")
except json.JSONDecodeError as e:
    print(f"Неизвестная ошибка {e}")
except NetmikoTimeoutException as e:
    print(f"Таймаут подключения: {e}")
except NetmikoAuthenticationException as e:
    print(f"Неверный логин или пароль {e}")