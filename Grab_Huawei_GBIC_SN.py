from netmiko import ConnectHandler

def get_gbic_sn():
    huawei_switch = {
        'device_type': 'huawei',  # Netmiko 专用的华为类型
        'host': '11.42.250.25',
        'username': 'admin',
        'password': 'P@ssw0rd',
        'port': 22,
    }    # 定义设备信息

    try:
        # 2. 连接设备
        net_connect = ConnectHandler(**huawei_switch)
        print("Successfully connected to the switch.")

        # 3. 发送命令 (显示所有光模块的电子标签信息，包含 SN)
        command = "display dev elab"
        output = net_connect.send_command(command)

        barcodes = []      # GBIC SN
        port_ids = []      # GBIC port no.

        descriptions = []  # GBIC type
        model_dict  = {'1300Mb/sec-1310nm-LC-10000(9um/125um SMF)':'Huawei SFP-GE-LX-SM1310 LX GBIC  (No Warranty)',
                       '2100Mb/sec-850nm-LC-275(OM1),550(OM2),1000(OM3)':'Huawei eSFP-GE-SX-MM850 Module (No Warranty)',
                       '1300Mb/sec--nm-RJ45-100(Copper)':'Huawei SFP-1000BaseTX GBIC  (No Warranty)',
                       '40GE-1301nm-LC-10000(9um/125um SMF)': 'Huawei QSFP-40G-LR4 GBIC (60-MW)',
                       '25750Mb/sec-1310nm-LC-10000(9um/125um SMF)': 'Huawei SFP-25G-LR SFP (60MW)',
                       '10300Mb/sec-1310nm-LC-10000(9um/125um SMF)': 'Huawei OSX010000 LR GBIC (No Warranty)',
                       '10300Mb/sec-850nm-LC-30(62.5um/125um OM1),80(50um/125um OM2),300(50um/125um OM3),400(50um/125um OM4)' : 'Huawei OMXD30000 SR GBIC (No Warranty)'}

        lines = output.split('\n')

        #print('CE6863E' in lines[8]) #BoardType is CE6863E-48S6CQ-B

        for index, line in enumerate(lines):
            if '[FAN1]' in line:
                break
            if index >= 26:
                if 'BarCode=' in line:
                    barcode = line.split('BarCode=')[1].strip()
                    if barcode:  # Exclude empty values
                        barcodes.append(barcode)
                        temp = lines[index+2].split('Description=')[1].strip()
                        descriptions.append(model_dict[temp])

                        if '100' in lines[index - 7] and 'CE6863E' in lines[8] :
                            port_id = str(int(lines[index - 7].split('GE1/0/')[1].replace(']','')) + 48)
                        else :
                            port_id = lines[index - 7].split('GE1/0/')[1].replace(']','')
                        if len(port_id) < 2:
                            port_ids.append('0'+ port_id)
                        else :
                            port_ids.append(port_id)

        print("List of BarCodes:", barcodes)
        print("List of Port:", port_ids)
        print(len(port_ids))


        net_connect.disconnect()
        return barcodes, port_ids, descriptions
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

if __name__ == "__main__":
    get_gbic_sn()
