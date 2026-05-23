from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException, ReadTimeout
import getpass
import time

def get_userinfo():
    ip = input(f"IP-адрес:")
    username = input(f"Имя пользователя:")
    password = getpass.getpass(f"Пароль:")
    interface = input("Номер порта (в формате gi x/x):")
    vendor = input(f"Вендор Eltex ?(y/n)")
    return ip, username, password, interface, vendor
def get_vendor(vendor):
    if vendor.lower() == "y":
        return "eltex" 
    else:
        return "juniper_junos"
def connect_and_reset(ip, username, password, interface, vendor):
    connection = ConnectHandler(
        device_type = get_vendor(vendor),
        host = ip,
        username = username,
        password = password,
    )
    print(f"Подключение к {get_vendor(vendor)} {ip}:")
    if get_vendor(vendor) == "eltex":
        connection.send_config_set([f"int {interface}", "shutdown", "no shutdown"])
        time.sleep(1)
        IntStatus = connection.send_command(f"show interface status {interface} ")
        print(f"\n \n \n")
        print(f"Результат перезагрузки:\n{IntStatus}")
        time.sleep(2)
        MacTable = connection.send_command(f"show mac address-table interface {interface}")
        print(f"Таблица коммутации:\n{MacTable}")
        connection.disconnect()
    elif get_vendor(vendor) == "juniper_junos":
        connection.send_config_set([f"set interfaces {interface} disable"])
        connection.commit()
        connection.send_config_set([f"delete interfaces {interface} disable"])
        connection.commit(and_quit=True)
        time.sleep(1)
        IntStatus = connection.send_command(f"show interfaces {interface} descriptions")
        print(f"\n \n \n")
        print(f"Результат перезагрузки:\n{IntStatus}")
        time.sleep(2)
        MacTable = connection.send_command(f"show ethernet-switching table interface {interface}")
        print(f"Таблица коммутации:\n{MacTable}")
        connection.disconnect()  
try:
    ip, username, password, interface, vendor = get_userinfo()
    connect_and_reset(ip, username, password, interface, vendor)
except NetmikoTimeoutException as e:
    print(f"Таймаут подключения: {e}")
except NetmikoAuthenticationException as e:
    print(f"Неверный логин или пароль {e}")
except ReadTimeout as e:
    print(f"Устройство не отвечает: {e}")