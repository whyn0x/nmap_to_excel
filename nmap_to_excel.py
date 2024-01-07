import xml.etree.ElementTree as ET
import pandas as pd

def parse_nmap_output(nmap_file_path, output_file_path):
    tree = ET.parse(nmap_file_path)
    root = tree.getroot()

    data = []
    for host in root.findall('host'):
        ip = host.find('address').get('addr')
        hostname = host.find('hostnames/hostname').get('name') if host.find('hostnames/hostname') is not None else None
        for port in host.iter('port'):
            port_number = port.get('portid')
            state = port.find('state').get('state')
            service = port.find('service')
            if service is not None:
                service_name = service.get('name')
                version = service.get('product')
                if service.get('version'):
                    version += ' ' + service.get('version')
            else:
                service_name = None
                version = None
            data.append([ip, hostname, port_number, state, service_name, version])

    df = pd.DataFrame(data, columns=["IP", "Host", "Port", "State", "Service", "Version"])
    df.to_excel(output_file_path, index=False)
    print(f"File saved at {output_file_path}")

nmap_file_path = input("Enter the path of the nmap output in XML: ")
output_file_path = input("Enter the path of the output result table: ")

parse_nmap_output(nmap_file_path, output_file_path)
