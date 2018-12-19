from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
from datetime import datetime
from time import sleep

'''
Name
Market cap
price
24 hr change
1 hr change
volume
hourly sentiment
1hr price projection
accuracy
'''

def clean_dollar(string):
	string = string.replace('$', '')
	string = string.replace(',', '')
	return float(string)


def clean_percent(string):
	string = string.replace('%','')
	return float(string)


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('test-type')

driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver.get('https://google.com')
sleep(2)
driver.get('https://thetie.io/coins')
sleep(8)
# open layout settings
test = driver.find_element_by_xpath('//span[@id="coin-intro-step3"]/a')
test.click()
sleep(2)
# add 1hr price change
test = driver.find_element_by_xpath('//input[@data-name="1Hr Price Change"]').click()
sleep(2)
# save layout
test = driver.find_element_by_id('save_columns_selector').click()
sleep(2)
# click on filter for sentiment
driver.find_element_by_id('coin-intro-step7').click()
sleep(2)
# input data
test = driver.find_element_by_xpath('//td[@data-column="15"]/div/input')
test.send_keys('75')
sleep(2)

df2 = []

# Coins displayed
results = driver.find_elements_by_xpath('//tbody[@aria-live="polite"]/tr[@class=""]')

for row in results:

	# Coin symbol
	symbol = row.find_element_by_xpath('td[2]').text
	# Coin name
	name = row.find_element_by_xpath('td[3]').text
	# mcap
	mcap = row.find_element_by_xpath('td[4]').text
	mcap = clean_dollar(mcap)
	# price
	price = row.find_element_by_xpath('td[5]').text
	# 24hr change
	day_change = row.find_element_by_xpath('td[6]').text
	day_change = clean_percent(day_change)
	# 1hr change
	hour_change = row.find_element_by_xpath('td[7]').text
	hour_change = clean_percent(hour_change)
	# volume
	volume = row.find_element_by_xpath('td[10]').text
	volume = clean_dollar(volume)
	# hourly sentiment
	hour_sent = row.find_element_by_xpath('td[16]').text
	hour_sent = float(hour_sent[:hour_sent.find(' ')])
	# Hr price prediction
	hour_pred = row.find_element_by_xpath('td[23]').text
	hour_pred = clean_percent(hour_pred)
	# Accuracy
	accuracy = row.find_element_by_xpath('td[25]').text
	accuracy = clean_percent(accuracy)

	df2.append([
				datetime.now(),
				symbol,
				name,
				mcap,
				price,
				day_change,
				hour_change,
				volume,
				hour_sent,
				hour_pred,
				accuracy
	])

# ------------------
df2 = pd.DataFrame(
		df2,
		columns=[
				 'date',
				 'symbol',
				 'name',
				 'mcap',
				 'price',
				 'day_change',
				 'hour_change',
				 'volume',
				 'hour_sent',
				 'hour_pred',
				 'accuracy'
				 ]
	)

try:
	df1 = pd.read_csv('data.csv')
	df1 = df1.append(df2)
	df1.to_csv('data.csv', index=False)
except:
	df2.to_csv('data.csv', index=False)

driver.close()
