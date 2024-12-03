import os,requests,random
os.environ['WDM_PROGRESS_BAR'] = str(0)
import traceback,sys,time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import whisper
import warnings
from bs4 import BeautifulSoup as bs
import smtplib
from email.message import EmailMessage

driver=None
# Record the start time
import datetime
start_time = datetime.datetime.now()
warnings.filterwarnings("ignore")
model = whisper.load_model("base")

headers = {
        "accept": "*/*",
        "accept-language": 'en-US,en;q=0.9',
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.70 Safari/537.36"
        }
# free ssl proxy collect function

def get_sslproxies():
    retray=0
    while retray<3:
        try:
            urls = 'https://www.sslproxies.org/'
            res = requests.get(urls,headers=headers,timeout=10)
            soups = bs(res.text, 'html.parser')
            table_htmls=soups.find('div',attrs={'class':'table-responsive fpl-list'})
            tables = table_htmls.find('table')
            tbodys=tables.find('tbody')
            table_rows=tbodys.find_all('tr')
            proxie = []
            for rows in table_rows:
                column = rows.find_all('td')
                proxys = {'ip': column[0].text, 'port': column[1].text, 'code': column[2].text,
                        'country': column[3].text, 'anonymity': column[4].text, 'google': column[5].text,
                        'https': column[6].text, 'last_checked': column[7].text}
                proxie.append(proxys)
            proxies_lists=[]
            for lists in proxie:
                # if lists["https"]=="yes":
                #     proxies_lists.append(f"https://{lists['ip']}:{lists['port']}")
                # else:
                if lists["anonymity"]=="elite proxy":
                    proxies_lists.append(f"{lists['ip']}:{lists['port']}")
                    
            return proxies_lists
        except:
            retray+=1
            continue
    if retray>3:
        return None

def verify_proxy():
    proxy_lists=get_sslproxies()
    if proxy_lists is None:
        return None
    veryfy_proxy_lists=[]
    for proxy_ip in proxy_lists:
        url="https://ipinfo.io/json"
        proxies=f'http://{proxy_ip}'
        try:
            response=requests.get(url,headers=headers,proxies={"http": proxies},timeout=3)
            if response.status_code==200:
                veryfy_proxy_lists.append(proxy_ip)
        except:
            pass
    if len(veryfy_proxy_lists)==0:
        return proxy_lists
    else:
        return veryfy_proxy_lists

def real_proxy_list():
    good_proxy_lists=[]
    real_proxy_lists=get_sslproxies()
    if real_proxy_lists is None:
        return None
    
    for good_proxy in real_proxy_lists:
        try:
            response = requests.get("https://www.vfsglobal.com/", proxies={"http": good_proxy, "https": good_proxy}, timeout=5)
            if response.status_code == 200:
                good_proxy_lists.append(good_proxy)
            else:
                pass
        except:
            pass

    # Save the valid proxies to a file
    if good_proxy_lists:  # Only save if there are valid proxies
        with open("valid_proxies.txt", "w") as file:
            file.write("\n".join(good_proxy_lists))  # Write proxies line by line
    else:
        print("No valid proxies found.")

    return True
            
if __name__=="__main__":
    try:
        real_proxy_list()
    except:
        sys.stderr = open('error.log', 'a+',encoding='utf-8')
        traceback.print_exc()
        sys.stderr.close()
        pass