import scapy.all as scapy
import networkx as nx
import matplotlib.pyplot as plt
import ipaddress
import threading
from datetime import datetime
import time
from collections import defaultdict
import platform
import subprocess
import re


class NetworkScanner:
    def __init__(self):
        self.network_graph = nx.Graph()
        self.devices = {}
        self.scanning = False
        self.local_ip = self.get_local_ip()
        self.network_range = self.get_network_range()

    def get_local_ip(self):
        """Взема локалния IP адрес"""
        try:
            # Създаваме временно сокетче за да вземем локалния IP
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "192.168.1.1"  # fallback

    def get_network_range(self):
        """Определя мрежовия диапазон базирано на локалния IP"""
        try:
            ip = ipaddress.IPv4Address(self.local_ip)
            network = ipaddress.IPv4Network(f"{ip}/24", strict=False)
            return str(network)
        except:
            return "192.168.1.0/24"  # fallback

    def get_gateway_ip(self):
        """Взема IP адреса на рутера/гатуъя"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(["ipconfig"], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                for line in lines:
                    if "Default Gateway" in line:
                        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
                        if ip:
                            return ip[0]
            else:  # Linux/Mac
                result = subprocess.run(["ip", "route"], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                for line in lines:
                    if "default" in line:
                        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
                        if ip:
                            return ip[0]
        except:
            pass
        return self.local_ip  # fallback

    def arp_scan(self, network_range=None):
        """Извършва ARP сканиране на мрежата"""
        if network_range is None:
            network_range = self.network_range

        print(f"🔍 Сканиране на мрежа: {network_range}")

        # Създаваме ARP заявка
        arp_request = scapy.ARP(pdst=network_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request

        # Изпращаме заявката и получаваме отговори
        answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

        devices = []
        for element in answered_list:
            device_info = {
                'ip': element[1].psrc,
                'mac': element[1].hwsrc,
                'vendor': self.get_vendor_from_mac(element[1].hwsrc),
                'hostname': self.get_hostname(element[1].psrc),
                'last_seen': datetime.now(),
                'type': self.classify_device(element[1].hwsrc, element[1].psrc)
            }
            devices.append(device_info)

        return devices

    def get_vendor_from_mac(self, mac_address):
        """Опитва се да определи производителя по MAC адрес"""
        try:
            # База данни с известни OUI (Organizationally Unique Identifier)
            oui_database = {
                "00:1B:44": "Cisco",
                "00:0C:29": "VMware",
                "00:50:56": "VMware",
                "00:1A:11": "Google",
                "00:1D:72": "HP",
                "00:24:81": "Dell",
                "00:26:BB": "Apple",
                "00:1E:C9": "Samsung",
                "00:23:12": "Intel",
                "00:1F:5B": "Netgear",
                "00:22:5F": "Microsoft",
                "00:25:BC": "ASUS",
                "00:1E:65": "TP-Link",
                "00:21:6A": "Linksys",
                "00:1C:B3": "Belkin",
                "00:14:A4": "Raspberry Pi",
                "DC:A6:32": "Raspberry Pi"
            }

            oui = mac_address.upper()[:8]
            return oui_database.get(oui, "Unknown Vendor")
        except:
            return "Unknown"

    def get_hostname(self, ip):
        """Опитва се да получи hostname на устройството"""
        try:
            import socket
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return "Unknown"

    def classify_device(self, mac, ip):
        """Класифицира устройството по тип"""
        vendor = self.get_vendor_from_mac(mac).lower()

        if any(keyword in vendor for keyword in ['cisco', 'netgear', 'tp-link', 'linksys']):
            return "Router/Network"
        elif any(keyword in vendor for keyword in ['vmware', 'virtualbox']):
            return "Virtual Machine"
        elif any(keyword in vendor for keyword in ['apple']):
            return "Apple Device"
        elif any(keyword in vendor for keyword in ['raspberry']):
            return "Raspberry Pi"
        elif ip == self.local_ip:
            return "This Computer"
        else:
            return "Generic Device"

    def continuous_scan(self, interval=60):
        """Непрекъснато сканиране на мрежата"""
        self.scanning = True
        while self.scanning:
            try:
                new_devices = self.arp_scan()
                self.update_network_graph(new_devices)
                time.sleep(interval)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Грешка при сканиране: {e}")
                time.sleep(interval)

    def update_network_graph(self, devices):
        """Обновява мрежовия граф с новите устройства"""
        gateway_ip = self.get_gateway_ip()

        # Добавяме рутера като централен възел
        self.network_graph.add_node(
            gateway_ip,
            type="Router",
            label="Router/Gateway",
            color="red",
            size=500
        )

        # Добавяме всички открити устройства
        for device in devices:
            device_ip = device['ip']

            self.network_graph.add_node(
                device_ip,
                type=device['type'],
                label=f"{device_ip}\n{device['vendor']}",
                mac=device['mac'],
                vendor=device['vendor'],
                hostname=device['hostname'],
                color=self.get_device_color(device['type']),
                size=self.get_device_size(device['type'])
            )

            # Свързваме устройството с рутера
            self.network_graph.add_edge(gateway_ip, device_ip, weight=1)

        self.devices = {device['ip']: device for device in devices}

    def get_device_color(self, device_type):
        """Връща цвят за визуализация спрямо типа на устройството"""
        colors = {
            "Router/Network": "red",
            "This Computer": "blue",
            "Apple Device": "gray",
            "Virtual Machine": "purple",
            "Raspberry Pi": "green",
            "Generic Device": "orange"
        }
        return colors.get(device_type, "yellow")

    def get_device_size(self, device_type):
        """Връща размер за визуализация спрямо типа на устройството"""
        sizes = {
            "Router/Network": 800,
            "This Computer": 600,
            "Apple Device": 400,
            "Virtual Machine": 350,
            "Raspberry Pi": 450,
            "Generic Device": 300
        }
        return sizes.get(device_type, 300)


class NetworkVisualizer:
    def __init__(self, network_scanner):
        self.scanner = network_scanner
        self.fig = None
        self.ax = None

    def visualize_network(self):
        """Визуализира мрежовия граф"""
        if len(self.scanner.network_graph.nodes()) == 0:
            print("❌ Няма данни за визуализация. Първо изпълни сканиране!")
            return

        plt.figure(figsize=(14, 10))

        # Вземаме позициите на възлите
        pos = nx.spring_layout(self.scanner.network_graph, k=2, iterations=50)

        # Вземаме атрибутите за визуализация
        node_colors = []
        node_sizes = []
        labels = {}

        for node in self.scanner.network_graph.nodes():
            node_data = self.scanner.network_graph.nodes[node]
            node_colors.append(node_data.get('color', 'gray'))
            node_sizes.append(node_data.get('size', 300))
            labels[node] = node_data.get('label', node)

        # Рисуваме графа
        nx.draw_networkx_nodes(
            self.scanner.network_graph, pos,
            node_color=node_colors,
            node_size=node_sizes,
            alpha=0.9
        )

        nx.draw_networkx_edges(
            self.scanner.network_graph, pos,
            edge_color='gray',
            width=2,
            alpha=0.6
        )

        nx.draw_networkx_labels(
            self.scanner.network_graph, pos,
            labels=labels,
            font_size=8,
            font_weight='bold'
        )

        # Добавяме легенда
        self._add_legend()

        plt.title("🌐 Визуализация на локалната мрежа\n(Устройства свързани към рутера)",
                  fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def _add_legend(self):
        """Добавя легенда към графиката"""
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Router/Network'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='This Computer'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Raspberry Pi'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='purple', markersize=10,
                       label='Virtual Machine'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=10, label='Apple Device'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='Other Devices')
        ]

        plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1))

    def print_network_info(self):
        """Принтира детайлна информация за мрежата"""
        print("\n" + "=" * 60)
        print("📊 ДЕТАЙЛИ ЗА ЛОКАЛНАТА МРЕЖА")
        print("=" * 60)

        print(f"📍 Локален IP: {self.scanner.local_ip}")
        print(f"🌍 Мрежов диапазон: {self.scanner.network_range}")
        print(f"🔄 Рутер/Gateway: {self.scanner.get_gateway_ip()}")
        print(f"🔍 Открити устройства: {len(self.scanner.devices)}")

        print("\n📋 СПИСЪК С УСТРОЙСТВА:")
        print("-" * 60)

        for ip, device in self.scanner.devices.items():
            print(f"IP: {ip}")
            print(f"  MAC: {device['mac']}")
            print(f"  Производител: {device['vendor']}")
            print(f"  Hostname: {device['hostname']}")
            print(f"  Тип: {device['type']}")
            print(f"  Последно видян: {device['last_seen'].strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 40)


class NetworkMonitorApp:
    def __init__(self):
        self.scanner = NetworkScanner()
        self.visualizer = NetworkVisualizer(self.scanner)
        self.scan_thread = None

    def run_single_scan(self):
        """Изпълнява еднократно сканиране"""
        print("🚀 Стартиране на еднократно сканиране...")
        devices = self.scanner.arp_scan()
        self.scanner.update_network_graph(devices)

        print(f"✅ Открити са {len(devices)} устройства")
        self.visualizer.print_network_info()
        self.visualizer.visualize_network()

    def run_continuous_monitor(self, interval=60):
        """Стартира непрекъснат мониторинг"""
        print(f"🔍 Стартиране на непрекъснат мониторинг (интервал: {interval} секунди)")
        print("Натисни Ctrl+C за спиране...")

        try:
            self.scan_thread = threading.Thread(
                target=self.scanner.continuous_scan,
                args=(interval,)
            )
            self.scan_thread.daemon = True
            self.scan_thread.start()

            # Позволяваме на потребителя да визуализира по всяко време
            while True:
                time.sleep(5)
                choice = input("\n🎮 Натисни 'v' за визуализация, 'q' за изход: ").lower()
                if choice == 'v':
                    self.visualizer.visualize_network()
                elif choice == 'q':
                    self.scanner.scanning = False
                    break

        except KeyboardInterrupt:
            self.scanner.scanning = False
            print("\n⏹️ Мониторингът е спрян")

    def show_menu(self):
        """Показва главното меню"""
        while True:
            print("\n" + "=" * 50)
            print("🌐 МРЕЖОВ ВИЗУАЛИЗАТОР")
            print("=" * 50)
            print("1. Еднократно сканиране и визуализация")
            print("2. Непрекъснат мониторинг")
            print("3. Покажи мрежова информация")
            print("4. Тестово сканиране (ограничен диапазон)")
            print("5. Изход")

            choice = input("Избери опция: ")

            if choice == "1":
                self.run_single_scan()
            elif choice == "2":
                interval = int(input("Интервал на сканиране (секунди) [60]: ") or "60")
                self.run_continuous_monitor(interval)
            elif choice == "3":
                self.visualizer.print_network_info()
            elif choice == "4":
                self.run_test_scan()
            elif choice == "5":
                if self.scanner.scanning:
                    self.scanner.scanning = False
                print("👋 Излизане от програмата...")
                break
            else:
                print("❌ Невалиден избор!")

    def run_test_scan(self):
        """Изпълнява тестово сканиране в ограничен диапазон"""
        test_range = input("Въведи мрежов диапазон [192.168.1.0/24]: ") or "192.168.1.0/24"
        print(f"🔍 Тестово сканиране на {test_range}...")

        devices = self.scanner.arp_scan(test_range)
        self.scanner.update_network_graph(devices)

        print(f"✅ Открити са {len(devices)} устройства")
        self.visualizer.print_network_info()


def main():
    """Основна функция"""
    print("🚀 ИНИЦИАЛИЗИРАНЕ НА МРЕЖОВИЯ ВИЗУАЛИЗАТОР...")

    # Проверка за необходимите библиотеки
    try:
        import scapy.all
        import networkx
    except ImportError as e:
        print(f"❌ Липсващи библиотеки: {e}")
        print("📦 Инсталирай с: pip install scapy networkx matplotlib")
        return

    app = NetworkMonitorApp()
    app.show_menu()


if __name__ == "__main__":
    main()