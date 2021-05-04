from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

species = input('Art: ')
try:
    os.mkdir(
        'C:/Development/AI/ai-dataanalys-BBA-ta-suniL/AI Grunder/Projekt/images/' + species)
except:
    pass
searches = []
i = 1
while True:
    search = input('Sökord ' + str(i) + ': ')
    if search == '':
        break
    searches.append(search)
    i += 1
number = int(input('Antal bilder: '))

print(searches)

for s in searches:
    driver = webdriver.Chrome('C:\Development\chromedriver.exe')
    driver.get('https://www.google.com/')

    driver.find_element_by_xpath('//*[@id="zV9nZe"]/div').click()
    box = driver.find_element_by_xpath(
        '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    box.send_keys(s)
    box.send_keys(Keys.ENTER)
    driver.find_element_by_xpath(
        '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()

    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')
        try:
            driver.find_element_by_xpath(
                '//*[@id="islmp"]/div/div/div/div/div[4]/div[2]/input').click()
            time.sleep(2)
        except:
            pass
        if new_height == last_height:
            break
        last_height = new_height

    for i in range(1, number):
        try:
            driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').screenshot(
                './images/'+species+'/'+s+'('+str(i)+').png')
        except:
            pass
