#Scraper 1 Flipkart

import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
import time

#Path for chrome driver in local machine
#Change it accordingly
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
#driver1 = webdriver.Chrome(PATH)
url = "https://www.flipkart.com"

def get_url(search_term):
	template = 'https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
	search_term = search_term.replace(' ','+')
	return template.format(search_term)

data_list = []
rank = 0

#First 5 pages
for page in range(1, 6):
	print('Processing page no: ', page, ' ****************************************************************************************')
	url = get_url('shoes')
	extension = '&page=' + str(page)
	url += extension
	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'html.parser')

	#for every row
	results = soup.find_all('div',{'class': '_1AtVbE col-12-12'})

	#for every element
	#results = soup.find_all('div',{'class': '_1xHGtK _373qXS'})

	for result in results:
		next_div = result.find_all('div',{'class': '_13oc-S'})

		#items = next_div.find_all('div')
		for item in next_div:
			divs = item.find_all('div', {'style': 'width:25%'})
			divs2 = item.find_all('div', {'style': 'width:100%'})

			#for 4 elements in a row
			if len(divs) == 4:
				for div_tab in divs:
					element_list = []
					rank = rank + 1
					element_list.append(rank)
					element_list.append(div_tab.get('data-id'))
					#for title
					atags = div_tab.find_all('a')
					for a in atags:
						if a.get('title'):
							product_url = 'https://www.flipkart.com' + a.get('href')
							break
					driver.get(product_url)
					soup1 = BeautifulSoup(driver.page_source, 'html.parser')
					results = soup1.find('div',{'class': '_3_L3jD'})
					spantag = results.find_all('span')
					if len(spantag) >=2:
						element_list.append(spantag[0].text)
						element_list.append(spantag[1].text)
					
					results2 = soup1.find('span',{'class': 'b7864- _2Z07dN'})
					if len(results2) >= 1:
						element_list.append(1)	#product is flipkart assured
					else:
						element_list.append(0)

					seller_list = []

					litag = soup1.find_all('li', {'class': '_38I6QT'})

					#featured seller
					sellertag = soup1.find_all('div',{'id': 'sellerName'})
					for tag in sellertag:
						seller_info = []
						spantag = tag.find('span')
						seller_name = spantag.find('span')
						seller_info.append(seller_name.text)
						#print(seller_name.text)	#featured seller name
						seller_rating = spantag.find('div')
						seller_info.append(seller_rating.text)
						#print(seller_rating.text)	#featured seller rating
						seller_list.append(seller_info)

					#for other sellers
					if len(litag) > 0:
						for lis in litag:
							a_tag = lis.find('a')
							seller_url = 'https://www.flipkart.com' + a_tag.get('href')
							driver.get(seller_url)
							soup2 = BeautifulSoup(driver.page_source, 'html.parser')
							print(soup2.text)
							#results3 = soup2.find_all('div',{'class': '_2Y3EWJ'})
							#for each in results3:
							#	print(each.text)


					element_list.append(seller_list)

					data_list.append(element_list)


			#for 1 element in a row
			elif len(divs2) == 1:
				for div_tab in divs2:
					a = div_tab.find('a')
					print(a.text)
					product_url = 'https://www.flipkart.com' + a.get('href')
					driver.get(product_url)
					#driver.back()







			#ad = item.find('span')
#			a = item.find('a')
#			print(a.text)
#			print('\nHey\n')

			#atag = item.find_all('a')
			#for a in atag:
			#	print(a.text)