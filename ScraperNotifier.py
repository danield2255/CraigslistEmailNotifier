import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import bs4 as bs
from bs4 import BeautifulSoup, element

#input own email and password
emailAddress = #enter email
emailPass = #enter pass

links = []
#Can choose to use chrome if phantomjs is not functional
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument('--no-sandbox')
option.add_argument('headless')
#option.add_argument("--no-startup-window")
#wd = webdriver.Chrome("dependencies/chromedriver", options = option)
wd = webdriver.PhantomJS("dependencies/phantomjs")
url = #INPUT: Enter the particular craigslist site desired in quotes
wd.get(url)

#selects the 'gigs' subgroup to search in
gigsButton = wd.find_element_by_xpath('//*[@id="ggg"]/h4/a')
gigsButton.click()
time.sleep(2)

searchBar = wd.find_element_by_xpath('//*[@id="query"]')
search_val = #INPUT:enter the value of what you would like to search for
searchBar.send_keys(search_val)
searchBar.send_keys(Keys.ENTER)
time.sleep(2)

soup = bs.BeautifulSoup(wd.page_source, "html.parser")
listings = soup.find_all("a", attrs = {'class':"result-title hdrlnk"})
for listing in listings:
    text = listing.text
    #Makes sure only looking at results in desired location
    links.append(listing)

#Compose the email message
msg = EmailMessage()
msg["Subject"] = "Update of Craigslist Listing"
msg["From"] = emailAddress
msg["To"] = emailAddress
#put in the content of text in the email
content = #INPUT: content
total = ""
for item in links:
    total = total + str(item) + "<br><br>"


msg.set_content(MIMEText(content + total, "html"))


#this will work if the email you are trying to send from is a gmail, will need to change the input parameter otherwise
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(emailAddress, emailPass)
    smtp.send_message(msg)
