from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException, ReadTimeout
import getpass
import json
import time

def get_device_type(vendor):
    if vendor == "cisco":
        return  "cisco_ios_telnet"
    elif vendor == "huawei":
        return "huawei_telnet"
    else:
        raise ValueError(f"Неизвестный вендор: {vendor} ")

def get_command(vendor):
    num_port = input("Укажите номер порта в формате (x/x):")
    if vendor == "cisco":
        return (f"interface GigabitEthernet{num_port}"), num_port
    elif vendor == "huawei":
        return (f"interface GigabitEthernet{num_port}"), num_port
    else:
        return "Неизвестный вендор:", num_port
def connect_and_reset(device, command, num_port):
    connection = ConnectHandler(
        device_type=get_device_type(device['vendor']),
        port=device['telnet_port'],
        host= device['ip'],
        username=device['username'],
        password=device['password'],
    )
    print(f"Подключился к: {device['ip']}")
    connection.send_config_set([command, "shutdown", "no shutdown"])
    time.sleep(3)
    IntStatus = connection.send_command(f"show interface GigabitEthernet{num_port} description")
    print(f"Результат перезагрузки:\n{IntStatus}")
    time.sleep(3)
    MacTable = connection.send_command(f"show mac address-table interface GigabitEthernet{num_port}")
    print(f"Таблица коммутации:\n{MacTable}")
    connection.disconnect()
try:
    with open("devices.json", "r") as file:
        data = json.load(file)
    for device in data:
            command, num_port = get_command(device['vendor'])
            start = time.time()
            connect_and_reset(device, command, num_port)
            end = time.time()
            print(f"Время на выполнение с учётом timeout: {end-start:.2f} сек")
except FileNotFoundError:
    print("Error! Файл не найден!")
except json.JSONDecodeError as e:
    print(f"Неизвестная ошибка {e}")
except NetmikoTimeoutException as e:
    print(f"Таймаут подключения: {e}")
except NetmikoAuthenticationException as e:
    print(f"Неверный логин или пароль {e}")
except ReadTimeout as e:
    print(f"Устройство не отвечает: {e}")
    
