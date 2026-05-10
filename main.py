ip_address = "192.168.1.1"
port_num = 24
vendor = "cisco"

devices = [
    {"ip": "192.168.1.1", "vendor": "cisco"},
    {"ip": "192.168.1.2", "vendor": "huawei"},
    {"ip": "192.168.1.3", "vendor": "mikrotik"},
]
for device in devices:
    if device["vendor"] == "cisco":
        command = "interface GigabitEthernet0/1"
    elif device["vendor"] == "huawei":
        command = "interface GigabitEthernet0/0/1"
    else:
        command = "Неизвестный вендор"
    if command is not None:
        print(f"Устройство: {device['vendor']} | IP: {device['ip']} | Команда: {command}")