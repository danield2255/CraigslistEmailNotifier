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

emailAddress = os.environ.get('music_email_user')
emailPass = os.environ.get('music_email_pass')

links = []
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument('--no-sandbox')
#option.add_argument("--no-startup-window")
wd = webdriver.Chrome("../../Documents/chromedriver", options = option)
wd.get("https://slo.craigslist.org/")
gigsButton = wd.find_element_by_xpath('//*[@id="ggg"]/h4/a')
gigsButton.click()
time.sleep(2)
print(wd.current_url)
searchBar = wd.find_element_by_xpath('//*[@id="query"]')
searchBar.send_keys("music")
searchBar.send_keys(Keys.ENTER)
time.sleep(2)
print(wd.current_url)
soup = bs.BeautifulSoup(wd.page_source, "html.parser")
listings = soup.find_all("a", attrs = {'class':"result-title hdrlnk"})
for listing in listings:
    text = listing.text
    #Makes sure only looking at results in desired location
    links.append(listing)





msg = EmailMessage()
msg["Subject"] = "Update of Craigslist Listing"
msg["From"] = emailAddress
msg["To"] = emailAddress
content = "This is your update of live music wanted in slo:"
total = ""
for item in links:
    #cur = item.format(link = item.get("href"), text = item.text)
    total = total + str(item) + "<br><br>"
print(total)

msg.set_content(MIMEText(content + total, "html"))



with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(emailAddress, emailPass)
    smtp.send_message(msg)