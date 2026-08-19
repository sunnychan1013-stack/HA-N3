import pyodbc
from Grab_Huawei_GBIC_SN import get_gbic_sn

conn_str = "DSN=hs_prod;Trusted_Connection=Yes;"

#try:
    # 執行連線
barcodes, port_ids, descriptions = get_gbic_sn()
#test_GBIC = 'P5J0ZV12'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
BarCode_in_NCS = []

cursor.execute("SELECT SerialNo FROM hs_prod.dbo.EquipModule")

row = cursor.fetchall()

for a in barcodes :
    for i in range(len(row)):   #loop in NCS
        if a == row[i][0]:      #loop in display result
            BarCode_in_NCS.append(row[i][0]) #
    #if (len(BarCode_in_NCS) > 0):
      #  print(f'test GBIC : {a} in NCS')

print('GBIC found in NCS' + BarCode_in_NCS)

#except Exception as e:
  #  print(f"❌ 連線失敗：{e}")
    #print("請檢查：1. 是否在公司網路內 2. Windows 帳號是否有權限 3. ODBC DSN 名稱是否正確")
