from typing import Any
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re, time, subprocess, pymysql, platform
import pandas as pd
current_datetime = datetime.now()
print(current_datetime)

# log in to ILAP and direct to Part I url
service = Service(executable_path='C:/Users/CCY251/Desktop/pythonProject_Sunny/chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)  #do not close browser
driver = webdriver.Chrome(service=service, options=options)

#Part I item 1
driver.get('http://nmscmpprd61a:8081/n3page.html')
username_input_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "username")))
username_input_box.send_keys("ccy251")
password_input_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "password")))
password_input_box.send_keys("Su7n6n86*")
log_in_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "login")))
log_in_button.click()

wait = WebDriverWait(driver, 15)
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "iframe_bottom"))) # The table is stored within iframes, cannot directly use find_element to locate values
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "iframe_right")))
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "iframe_iframe2")))

input_box = driver.find_element(By.NAME, "10")
input_box.send_keys("Fail")

html_content = driver.page_source
html_table = driver.find_element(By.ID, "myTable")
print(html_table)
rows = html_table.find_elements(By.TAG_NAME, "tr")
row_data = []

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    each_row = []
    for cell in cells:
        each_row.append(cell.text.strip()) # Extract the visible text from the cell
    row_data.append(each_row)
#print(len(rowt(row_data)_data))
#print(row_data)
failed_L3 = []
for i in range(len(row_data)) :
    print(row)
    if row_data[i][0] == '' :
        break
    failed_L3.append(row_data[i])

print(failed_L3)

#Part I item 2
driver.get('https://dc6-ilap-kb-prd.server.ha.org.hk:5601/s/n3/app/dashboards#/view/446a9bb9-ccdc-4d48-8ce5-c18427beaad9?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))')
username_input_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "username")))
username_input_box.send_keys("ccy251")
password_input_box = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "password")))
password_input_box.send_keys("Su7n6n86*")
log_in_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-cf8eum-euiButtonDisplayContent")))
log_in_button.click()
#driver.quit()
time.sleep(8)

dc6_host = 'dc6-ilap-kb-prd.server.ha.org.hk'
dc8_host = 'dc8-ilap-kb-prd.server.ha.org.hk'
Part_I_2_result = ""
def check_ping_status(host):
    command = ['ping', host]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "True"
    except subprocess.CalledProcessError:
        return "False"

if check_ping_status(dc6_host) and check_ping_status(dc8_host) == "True" :
    Part_I_2_result = 'Normal'
else :
    Part_I_2_result = 'Abnormal'

#Part I item 3
try :
    Part_I_3_links = driver.find_elements(By.CLASS_NAME, "lnsTableCell--left")
    Part_I_3_result = []
    for i in range(len(Part_I_3_links)) :
        if Part_I_3_links[i].text == "(empty)" and Part_I_3_links[i - 2].text == "N3":
            Part_I_3_result.append(Part_I_3_links[i - 5].text)
    if len(Part_I_3_result) == 0 :
        Part_I_3_result.append("Normal")
except :
    print("Part_1_3 error")

#Part II item A1
try :
    driver.get('https://dc6-ilap-kb-prd.server.ha.org.hk:5601/s/n3/app/dashboards#/view/fd304b20-1976-11ee-b29b-512c3d826610?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))')
    driver.refresh()
    time.sleep(18)
    Part_II_A1_result = []

    #codes By GPT (start)
    current_scroll = 0
    titles = driver.find_elements(By.CLASS_NAME, "embPanel__titleText")
    for title in titles:
        if title.text.strip() == "EWAN Packet loss Summary":
    # Get the parent panel/container
            panel = title.find_element(By.XPATH, "./ancestor::div[contains(@class, 'embPanel')]")
    # Find the data grid inside this panel
            grid = panel.find_element(By.CLASS_NAME, "euiDataGrid__virtualized")
    # Now extract rows as before
            all_rows = set()
            step = 200  #Set元素不能重複，重複的元素將被自動去除
            last_scroll = -1
            while True:
                rows = grid.find_elements(By.CLASS_NAME, "euiDataGridRow")
                for row in rows:
                    cells = row.find_elements(By.CLASS_NAME, "euiDataGridRowCell")
                    row_data = tuple(cell.text for cell in cells)
                    all_rows.add(row_data)
                driver.execute_script("arguments[0].scrollTop += arguments[1];", grid, step)
                time.sleep(0.1)
                current_scroll = driver.execute_script("return arguments[0].scrollTop;", grid)
                if current_scroll == last_scroll:
                    break
                last_scroll = current_scroll
    #codes By GPT (end)

            Part_II_A1_list = list(all_rows)

            for i in range(len(Part_II_A1_list)):
                if int(Part_II_A1_list[i][-1]) > 10 :
                    Part_II_A1_result.append(Part_II_A1_list[i][-2])
            if len(Part_II_A1_result) == 0 :
                Part_II_A1_result.append("Normal")
except :
    print("Part_II_A1 error")

#Part II item B4
try:
    driver.get("https://dc6-ilap-kb-prd.server.ha.org.hk:5601/s/n3/app/discover#/?_g=(filters:!(),time:(from:now-24h%2Fh,to:now))&_a=(columns:!(device.ip),filters:!(('$state':(store:appState),meta:(alias:'temperature_alert,%20160.7.250.47',disabled:!f,index:f905dee0-0b1e-11ee-8bdb-31d31d6a5163,key:query,negate:!t,type:custom),query:(bool:(must:!((match_phrase:(tags:temperature_alert)),(match_phrase:(device.ip:'160.7.250.47'))))))),index:f905dee0-0b1e-11ee-8bdb-31d31d6a5163,interval:auto,query:(language:lucene,query:'tags%20:%20temperature_alert'),rowsPerPage:100000,sort:!(!('@timestamp',desc)))")
    time.sleep(5)

    grid = driver.find_element(By.CLASS_NAME, "euiDataGrid__virtualized")
    ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    Part_II_B4_result = set()
    last_scroll = -1
    step = 300

    while True:
        cells = grid.find_elements(By.CLASS_NAME, "unifiedDataTable__cellValue")
        for cell in cells:
            text = cell.text.strip()
            if ip_pattern.fullmatch(text):
                Part_II_B4_result.add(text)
        driver.execute_script("arguments[0].scrollTop += arguments[1];", grid, step)
        time.sleep(0.2)
        current_scroll = driver.execute_script("return arguments[0].scrollTop;", grid)
        if current_scroll == last_scroll:
            break
        last_scroll = current_scroll

    if len(Part_II_B4_result) == 0 :
        Part_II_B4_result.append("Normal")
except :
    print("Part_II_B4 error")

#Part II item B6
try:
    driver.get("https://dc6-ilap-kb-prd.server.ha.org.hk:5601/s/n3/app/discover#/?_g=(filters:!(),time:(from:now-6h,to:now))&_a=(columns:!(device.ip),filters:!(('$state':(store:appState),meta:(alias:'temperature_alert,%20160.7.250.47',disabled:!f,index:f905dee0-0b1e-11ee-8bdb-31d31d6a5163,key:query,negate:!t,type:custom,value:'%7B%22bool%22:%7B%22must%22:%5B%7B%22match_phrase%22:%7B%22tags%22:%22temperature_alert%22%7D%7D,%7B%22match_phrase%22:%7B%22device.ip%22:%22160.7.250.47%22%7D%7D%5D%7D%7D'),query:(bool:(must:!((match_phrase:(tags:temperature_alert)),(match_phrase:(device.ip:'160.7.250.47')))))),('$state':(store:appState),meta:(alias:!n,disabled:!f,index:f905dee0-0b1e-11ee-8bdb-31d31d6a5163,key:device.ip,negate:!f,type:exists,value:exists),query:(exists:(field:device.ip)))),index:f905dee0-0b1e-11ee-8bdb-31d31d6a5163,interval:auto,query:(language:lucene,query:'tags%20:%20temperature_alert'),rowsPerPage:100000,sort:!(!('@timestamp',desc)))")

    time.sleep(5)
    grid = driver.find_element(By.CLASS_NAME, "euiDataGrid__virtualized")
    ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    Part_II_B6_result = set()
    last_scroll = -1
    step = 300

    while True:
        cells = grid.find_elements(By.CLASS_NAME, "unifiedDataTable__cellValue")
        for cell in cells:
            text = cell.text.strip()
            if ip_pattern.fullmatch(text):
                Part_II_B6_result.add(text)
        driver.execute_script("arguments[0].scrollTop += arguments[1];", grid, step)
        time.sleep(0.2)
        current_scroll = driver.execute_script("return arguments[0].scrollTop;", grid)
        if current_scroll == last_scroll:
            break
        last_scroll = current_scroll

    if len(Part_II_B6_result) == 0 :
        Part_II_B6_result.append("Normal")
except :
    print("Part_II_B6 error")

print(Part_II_B6_result)
#Part II item A4
#Part_II_A4_connection = pymysql.connect(host = "11.185.1.57",user='root',password = 'nvaix7',)

