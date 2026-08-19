from netmiko import ConnectHandler
import re

def get_lldp_nei():
    cisco_L2 = {
        'device_type': 'cisco_ios',  # Netmiko 专用的华为类型
        'host': '160.41.161.247',
        'username': 'n3support',
        'password': 'Nvaix789',
        'port': 22,
    }    # 定义设备信息

    try:
        # 2. 连接设备
        net_connect = ConnectHandler(**cisco_L2)

        # 3. 发送命令 (显示所有光模块的电子标签信息，包含 SN)
        command = "show conf"
        commmand = "show lldp nei"
        show_conf_output = net_connect.send_command(command)
        show_lldp_output = net_connect.send_command(commmand)

        descriptions = []      # Description

        lines = show_conf_output.split('\n')

        interfaces_with_descriptions = {}

        for i, line in enumerate(lines):  #code from VScopilot
            if line.startswith('interface GigabitEthernet'):
                # Check if next item is a description
                if i + 1 < len(lines) and lines[i + 1].startswith(' description'):
                    interface_name = line.replace('interface ', '')
                    description = lines[i + 1].replace(' description ', '')
                    interfaces_with_descriptions[interface_name] = description

        print("List of descriptions:", interfaces_with_descriptions)

        lldp_lines = show_lldp_output.split('\n')
        start_idx = next(i for i, line in enumerate(lldp_lines) if 'Device ID' in line)
        data_lines = [line.strip() for line in re.findall(r'^([A-Za-z0-9\-\.]+\s+(?:Gi|Te).+)$', show_lldp_output, re.MULTILINE)]

        # Get data as list of dictionaries
        data_list = []
        for line in data_lines:
            parts = line.split()
            data_list.append({'Local Interface': parts[1],'Device ID': parts[0]})

        # Sort by Local Interface
        sorted_list = sorted(data_list, key=lambda x: x['Local Interface'])

        result = []
        for item in sorted_list:
            result.append({item['Local Interface']: item['Device ID']})
        print("List of LLDP neighbors:",result)

        # Extract device IDs from both (show conf & show lldp nei)
        dict_values = set(interfaces_with_descriptions.values())
        list_values = set(val for item in result for val in item.values())

        print('')
        # Check which ones match
        matches = dict_values & list_values  # Intersection
        print(f"Matching device IDs: {matches}")

        # Check which ones are missing
        missing_in_list = dict_values - list_values
        print(f"Missing in list: {missing_in_list}")

        net_connect.disconnect()

    #
    except Exception as e:
         print(f"Error: {e}")
         return None, None, None

if __name__ == "__main__":
    get_lldp_nei()
