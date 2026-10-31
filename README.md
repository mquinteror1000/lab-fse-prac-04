# Practica 04 FSE

### Objetivo

Al finalizar la práctica el alumno será capaz de:

- Configurar la Raspberry Pi como un punto de acceso inalámbrico.

- Conectar dispositivos móviles a la red local generada.

- Utilizar la aplicación Pytphox  para exponer los datos de sensores mediante una interfaz HTTP.

- Desarrollar un programa que obtenga y grafique datos de varios teléfonos celulares.

- Controlar periféricos conectados a la Raspberry Pi mediante mediciones de sensores remotos.

#### Lista de materiales

- Raspberry Pi 3B+

- Laptop

- Servomotor SG90

- Buzzer activo

- Fuente de alimentación 3.3-5V USB

- Protoboard

- Cables y jumpers requeridos

## Desarrollo

[actividad-1-generar-grafico](actividad-01-generar-grafico.md)

## 1. Preparación del entorno

### 1.1 Poner la Raspberry en modo AP

Se pone en modo AP para que se puedan conectar los teléfonos. sin embargo adelante veremos como se pierden muchos paquetes debido a la latencia.

Verificar el estado del wifi (que no esté bloqueado por hardware o software)

```shellsession
alumno@raspberrypi:~ $ rfkill list wifi
1: phy0: Wireless LAN
    Soft blocked: no
    Hard blocked: no
alumno@raspberrypi:~ $ nmcli radio wifi
enabled
alumno@raspberrypi:~ $ nmcli connection show 
NAME                UUID                                  TYPE      DEVICE     
practica-04         cfa1810c-57ba-4a13-89c5-ac207b0b0745  wifi      wlan0      
Wired connection 1  b1064703-8a8c-3a70-865e-7ff2ace45283  ethernet  eth0       
tailscale0          79922c2f-7940-4f2f-b84e-f7f284d47703  tun       tailscale0 
lo                  98745f94-28f7-4529-b651-035dac755033  loopback  lo         
H. Cuadra 7         ae5b3dd5-69a6-4531-83fe-366b25af941a  wifi      --         
.:PC Puma FI:.      0b74aa95-69ef-42cd-8858-821461142a0e  wifi      --  
```

Para este propósito nos importa editar la conexión **practica-04**

Se elige nmtui debido a que requiere recordar menos parámetros y es interactivo, lo que es una desventaja si se quiere automatizar, en ese caso se usaria nmcli para aplicar las mismas configuraciónes

```shellsession
alumno@raspberrypi:~ $ sudo nmcli connection edit practica-04

===| nmcli interactive connection editor |===

Editing existing '802-11-wireless' connection: 'practica-04'

Type 'help' or '?' for available commands.
Type 'print' to show all the connection properties.
Type 'describe [<setting>.<prop>]' for detailed property description.

You may edit the following settings: connection, 802-11-wireless (wifi), 802-11-wireless-security (wifi-sec), 802-1x, ethtool, match, ipv4, ipv6, hostname, tc, proxy
nmcli> set wifi.ssid embebidos-equipo-05
nmcli> set wifi-sec.psk "VIVA_lahispanidad."
nmcli> set wifi-sec.key-mgmt wpa-psk 
nmcli> save 
Connection 'practica-04' (cfa1810c-57ba-4a13-89c5-ac207b0b0745) successfully updated.
nmcli> q
alumno@raspberrypi:~ $
```

finalmente se levanta la conexión

```shellsession
alumno@raspberrypi:~ $ sudo nmcli connection up practica-04 
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/6)
```

### 1.1 Agregar la Raspberry a una Tailnet

En la práctica se observó que la conexión wifi genera la perdida de muchos paquetes, por lo que la solución que se encontró, fue agregar los teléfonos y la tarjeta a una VPN.

```shellsession
curl -fsSL https://tailscale.com/install.sh | sh
```

después de instalar  agregar el nodo a la tailnet

```shellsession
alumno@raspberrypi:~ $ sudo tailscale up
alumno@raspberrypi:~ $ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether b8:27:eb:d3:b8:48 brd ff:ff:ff:ff:ff:ff
    inet 172.1.7.74/16 brd 172.1.255.255 scope global dynamic noprefixroute eth0
       valid_lft 4746sec preferred_lft 4746sec
    inet6 fe80::46b0:ee71:6d57:c5e6/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether b8:27:eb:86:ed:1d brd ff:ff:ff:ff:ff:ff
    inet 192.168.4.1/24 brd 192.168.4.255 scope global noprefixroute wlan0
       valid_lft forever preferred_lft forever
    inet6 fe80::c50e:e5e3:60f8:8c70/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
5: tailscale0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1280 qdisc pfifo_fast state UNKNOWN group default qlen 500
    link/none 
    inet 100.88.117.21/32 scope global tailscale0
       valid_lft forever preferred_lft forever
    inet6 fd7a:115c:a1e0::5d30:7516/128 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::97d7:f9a5:39f2:2025/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
```

Una operación equivalente haremos en cada teléfono.
