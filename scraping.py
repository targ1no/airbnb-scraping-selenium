# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('window-size=400,800')
 
browser = webdriver.Chrome(options=options)
url = 'https://www.airbnb.com.br/'
browser.get(url)

sleep(2)

class Scrappy:

    def init(self):
        self.input_texting()
        self.choosing_in_calendar()
        self.qtt_people()
        sleep(2)
        self.scraping_datas()


    def input_texting(self):

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

    def choosing_in_calendar(self):

        sleep(2)
        next_button = browser.find_element(By.CLASS_NAME, '_1ku51f04')
        next_button.click()

    def qtt_people(self):

        sleep(2)
        next_button2 = browser.find_elements(By.TAG_NAME, 'button')[-1]
        next_button2.click() 

    def scraping_datas(self):

        try:

            next_page = browser.find_element(By.CLASS_NAME, '_1bfat5l')
            while next_page:

                page_content = browser.page_source 
                site = BeautifulSoup(page_content, 'html.parser')  

                property_list = []

                properties = site.findAll('div', attrs={'itemprop': 'itemListElement'})

                for _property in properties:
            
                    prop_url = _property.find('meta', attrs={'itemprop': 'url'})
                    prop_url = prop_url['content']

                    prop_name = _property.find('div', attrs={'class': 't1jojoys dir dir-ltr'})

                    prop_desc = _property.find('meta', attrs={'itemprop': 'name'})
                    prop_desc = prop_desc['content']

                    night_prop_price = _property.find('span', attrs={'class': '_tyxjp1'})

                    property_list.append([prop_url, prop_name.text, prop_desc, night_prop_price.text])

                # Saving in Excel with Pandas
                property_list = pd.DataFrame(property_list, columns=(['Url', 'Nome', 'Descrição', 'Preço']))
                property_list.to_csv('properties.csv', sep=';', mode='a', index=False)

                browser.execute_script("window.scrollTo(0, '12000');")

                sleep(2)

                next_page.click()

                sleep(2)

                print(property_list)

        except:
            print('Não temos mais páginas.')

start_scrappy = Scrappy()
start_scrappy.init()
