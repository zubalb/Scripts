#!/usr/bin/env python3
import time

def get_userinfo():
    print("Привет ! Я помогу тебе создать конфиг управления для коммутаторов типа Eltex MES 2XXX !\n"
         "Какой коммутатор ставим, 23xx или 24xx ?")
    model = input("Выберите модель(23 или 24):")
    MgmtVlan = input("Введите номер vlan управления(Цифру):")
    Uplink_input = input("Укажи оптический и медный\nПример: (te1/0/1, gi1/0/24)")
    ports = Uplink_input.split(",")
    Fiber_port = ports[0].strip()
    Copper_port = ports[1].strip()
    MgmtAddress = input("Укажи адрес управления в формате A.B.C.D X.X.X.X:")
    DefaultRoute = input("Укажи маршрут по умолчанию:")
    return model, MgmtVlan, MgmtAddress, DefaultRoute, Fiber_port, Copper_port
def get_model(model):
    if model in ("23", "2324", "2124", "2300"):
        return "MES 23XX"
    elif model in ("24", "2424"):
        return "MES 24XX"
    else:
        print("Неизвестная модель, ошибка.")
        return "Error"
def get_config(model, MgmtVlan, MgmtAddress, DefaultRoute, Fiber_port, Copper_port):
    if get_model(model) == "MES 23XX":
        print(f"\n \n \n")
        print(f"Вот конфиг управления для MES 23XX:\n \n")
        print(f"""
vlan database
vlan {MgmtVlan}
exit
!
interface {Copper_port}
switchport mode trunk
switchport trunk allowed vlan add {MgmtVlan}
exit
!
interface {Fiber_port}
switchport mode trunk
switchport trunk allowed vlan add {MgmtVlan}
exit
!    
!
interface vlan {MgmtVlan}
ip address {MgmtAddress}
exit
ip default-gateway {DefaultRoute}
!
""")
    elif get_model(model) == "MES 24XX":
        print(f"\n \n \n")
        print(f"Вот конфиг управления для MES 24XX:\n \n")
        print(f"""
vlan {MgmtVlan}
vlan active
!
interface {Copper_port}
switchport mode general
switchport general allowed vlan add {MgmtVlan}   
!
interface {Fiber_port}
switchport mode general
switchport general allowed vlan add {MgmtVlan}
! 
interface vlan {MgmtVlan}
ip address {MgmtAddress}
! 
ip route 0.0.0.0 0.0.0.0 {DefaultRoute}
""")
model, MgmtVlan, MgmtAddress, DefaultRoute, Fiber_port, Copper_port = get_userinfo()
get_config(model, MgmtVlan, MgmtAddress, DefaultRoute, Fiber_port, Copper_port)