#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import smtplib
import time
import csv


# In[2]:


# User Agent
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}


# In[3]:





# In[4]:


def getDetails():
    URL = input('Enter 99acres Property URL: ')
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    name = soup.select_one('#bedWash').getText()
    description = soup.select_one('#description').getText()
    address = soup.select_one('.component__pdDescAdd').getText().replace("\n", "")
    price = soup.select_one('#pdPrice').getText()
    product_images = soup.select('.slider img')
    product_overview = soup.select('#FactTableComponent li')
    additional_details = soup.select('#AdditionalDetailsComponent li')
    furnishingDetails = soup.select('#features li')
        
    
    with open(name+'.csv', 'w', newline='', encoding='utf-8') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(['Property Information'])
        filewriter.writerow(['Name', name])
        filewriter.writerow(['Description', description])
        filewriter.writerow(['Address', address])
        filewriter.writerow(['Price', price])
        
        filewriter.writerow('')
        filewriter.writerow(['Product Images'])
        for image in product_images:
            filewriter.writerow([image['data-src']])
        
        filewriter.writerow('')
        filewriter.writerow(['Property Overview'])
        for overview in product_overview:
            title = overview.find('div', {'class':'component__head'}).getText()
            details = overview.find('div',{'class':'component__details'}).getText()
            filewriter.writerow([title, details])
        
        filewriter.writerow('')
        filewriter.writerow(['Additional Information'])
        for info in additional_details:
            firstchild = info.select('span:first-child')
            lastchild = info.select('span:last-child')
            if(lastchild):
                filewriter.writerow([firstchild[0].getText(), lastchild[0].getText()])
            else:
                alternate_lastchild = info.select('span#Prop_Id')
                filewriter.writerow([firstchild[0].getText(), alternate_lastchild[0].getText()])
        
        
        filewriter.writerow('')
        filewriter.writerow(['Furnishing Details'])
        for furnishing in furnishingDetails:
            filewriter.writerow([furnishing.getText()])
        
        
        print('scrapped')
    
while True:   
    getDetails()

