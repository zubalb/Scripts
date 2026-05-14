from netmiko import ConnectHandler
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
    num_port = int(input("Введите последнюю цифру номера порта:"))
    if vendor == "cisco":
        return (f"interface GigabitEthernet0/{num_port}")
    elif vendor == "huawei":
        return (f"interface GigabitEthernet0/0/{num_port}")
    else:
        return "Неизвестный вендор:"
    
def connect_and_reset(device, command):
    connection = ConnectHandler(
        device_type=get_device_type(device['vendor']),
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
            print(f"IP: {device['ip']} | Порт: {get_command(device['vendor'])} | Вендор: {get_device_type(device['vendor'])} | Пользователь: {device['username']}")
except FileNotFoundError:
    print("Error! Файл не найден!")
except json.JSONDecodeError as e:
    print(f"Неизвестная ошибка {e}")