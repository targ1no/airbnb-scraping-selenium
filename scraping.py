# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('window-size=400,800')

# Iniciando Chrome 
browser = webdriver.Chrome(options=options)
url = 'https://www.airbnb.com.br/'
browser.get(url) 

property_list = []

# Interação/navegação com o site
sleep(3)
button_where = browser.find_element(By.TAG_NAME, 'button')
button_where.click()

sleep(2)
input_search = browser.find_element(By.TAG_NAME, 'label')
input_search.click()

sleep(3)
input_text = browser.find_element(By.ID, '/homes-1-input')
input_text.send_keys('Recife')
input_text.submit()

sleep(2)
next_button = browser.find_element(By.CLASS_NAME, '_1ku51f04')
next_button.click()

sleep(2)
next_button2 = browser.find_elements(By.TAG_NAME, 'button')[-1]
next_button2.click()

sleep(3)

# Pegando html pelo Selenium e transformando em obj. BS
page_content = browser.page_source 
site = BeautifulSoup(page_content, 'html.parser')

sleep(2)

# Raspando dados da pesquisa
properties = site.findAll('div', attrs={'itemprop': 'itemListElement'})

for _property in properties:
    
    prop_url = _property.find('meta', attrs={'itemprop': 'url'})
    prop_url = prop_url['content']

    prop_name = _property.find('div', attrs={'class': 't1jojoys dir dir-ltr'})

    prop_desc = _property.find('meta', attrs={'itemprop': 'name'})
    prop_desc = prop_desc['content']

    night_prop_price = _property.find('span', attrs={'class': '_tyxjp1'})

    # Adicionando resultado na lista
    property_list.append([prop_url, prop_name.text, prop_desc, night_prop_price.text])

# Salvando resultado no Excel
property_list = pd.DataFrame(property_list, columns=['URL', 'Prop Name', 'Prop Desc', 'Price'])
property_list.to_excel('properties.xlsx', index=False)

print(property_list)