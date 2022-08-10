# -*- coding: utf-8 -*-
"""
Created on May 3, 2022
@author: Felipe Matheus
"""
import requests
import json
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def initWebDriver(url):
    option = Options()
    option.headless = True
    driver = webdriver.Chrome(options=option, executable_path="C:\\chromedriver.exe")
    driver.maximize_window()
    driver.get(url)
    time.sleep(5)
    
    return driver

def getCotacaoScot(url):
    driver = initWebDriver(url)
    
    data = driver.find_element_by_xpath("//div[@class='conteudo_centro']//thead")
    data = data.get_attribute('outerHTML')
    data = BeautifulSoup(data, 'html.parser')
    data = data.find("th")
    data = data.get_text()
    data = data[17:27]
    
    tabela = driver.find_element_by_xpath("//div[@class='conteudo_centro']//table")
    tabela = tabela.get_attribute('outerHTML')
    tabela = BeautifulSoup(tabela, 'html.parser')
    tabela = tabela.find(name='table')
    tabela = pd.read_html(str(tabela))[0]
    tabela = tabela.loc[2:33]
    tabela = tabela.drop(tabela.columns[[2,4,5,6,7,8,9]], axis=1)
    tabela.columns = ['região', 'à vista', '30 dias']
    tabela["à vista"] = pd.to_numeric(tabela["à vista"])/100
    tabela["30 dias"] = pd.to_numeric(tabela["30 dias"])/100
    
    tabela.insert(0, 'data', data)
    
    return(tabela)

boi = getCotacaoScot("https://www.scotconsultoria.com.br/cotacoes/boi-gordo")

dados = boi.head(1)
dados = dados["data"].to_string(index=False)
dados = {'data': dados}
requests.patch(f'{firebase_db}/boi/data/.json', data=json.dumps(dados))

for x in range(2, 34):    
    dados = boi.loc[x]["à vista"]
    dados = {'d0': dados}

    dados = boi.loc[x]["30 dias"]
    dados = {'d30': dados}

if not os.path.exists('cotacao_boi_gordo.csv'):
    boi.to_csv('cotacao_boi_gordo.csv', encoding='utf-8', index=False, mode='w', header=True)

else:
    date_last_saved = pd.read_csv('cotacao_boi_gordo.csv').tail(1)
    date_last_saved = date_last_saved["data"].to_string(index=False)

    date_today = boi.head(1)
    date_today = date_today["data"].to_string(index=False)
    
    if not date_today == date_last_saved:
        boi.to_csv('cotacao_boi_gordo.csv', encoding='utf-8', index=False, mode='a', header=False)

vaca = getCotacaoScot("https://www.scotconsultoria.com.br/cotacoes/vaca-gorda")

dados = vaca.head(1)
dados = dados["data"].to_string(index=False)
dados = {'data': dados}
requests.patch(f'{firebase_db}/vaca/data/.json', data=json.dumps(dados))

for x in range(2, 34):    
    dados = vaca.loc[x]["à vista"]
    dados = {'d0': dados}

    dados = vaca.loc[x]["30 dias"]
    dados = {'d30': dados}

if not os.path.exists('cotacao_vaca_gorda.csv'):
    vaca.to_csv('cotacao_vaca_gorda.csv', encoding='utf-8', index=False, mode='w', header=True)

else:
    date_last_saved = pd.read_csv('cotacao_vaca_gorda.csv').tail(1)
    date_last_saved = date_last_saved["data"].to_string(index=False)

    date_today = vaca.head(1)
    date_today = date_today["data"].to_string(index=False)
    
    if not date_today == date_last_saved:
        vaca.to_csv('cotacao_vaca_gorda.csv', encoding='utf-8', index=False, mode='a', header=False)

"""
def getCotacaoCanalRural(url):
    driver = initWebDriver(url)
    
    data = driver.find_element_by_xpath("//div[@class='table-container']//span")
    data = data.get_attribute('outerHTML')
    data = BeautifulSoup(data, 'html.parser')
    data = data.b
    data = data.get_text()

    tabela = driver.find_element_by_xpath("//div[@class='table-container']//table")
    tabela = tabela.get_attribute('outerHTML')
    tabela = BeautifulSoup(tabela, 'html.parser')
    tabela = tabela.find(name='table')
    tabela = pd.read_html(str(tabela))[0]
    tabela = tabela[['PRAÇA', 'À VISTA', '30 DIAS']]
    tabela.columns = ['região', 'à vista', '30 dias']

    driver.close()
    
    return(data, tabela)
"""
