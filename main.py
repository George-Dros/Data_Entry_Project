import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


GOOGLE_DOC_FILE = "create your google doc file to inoput the data"
URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22mapBounds%22%3A%7B%22west%22%3A-122.63417281103516%2C%22east%22%3A-122.23248518896484%2C%22south%22%3A37.67155587510679%2C%22north%22%3A37.87888168056233%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22schu%22%3A%7B%22value%22%3Afalse%7D%2C%22sche%22%3A%7B%22value%22%3Afalse%7D%2C%22schm%22%3A%7B%22value%22%3Afalse%7D%2C%22schh%22%3A%7B%22value%22%3Afalse%7D%2C%22schp%22%3A%7B%22value%22%3Afalse%7D%2C%22schr%22%3A%7B%22value%22%3Afalse%7D%2C%22schc%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22customRegionId%22%3A%223bc8f64877X1-CR1di0egyqh2pj9_1as7c7%22%7D"
chrome_driver_path = "your chrome driver location"

headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"

}
response = requests.get(URL, headers=headers)
page = response.text
soup = BeautifulSoup(page, "html.parser")

prices = soup.findAll(class_="srp__sc-16e8gqd-1 jLQjry")
prices_per_month = [price.getText().split("+")[0] for price in prices]

addresses = soup.find_all("a", class_="StyledPropertyCardDataArea-c11n-8-85-1__sc-yipmu-0 gdfTyO property-card-link")
addresses_listings = [address.getText() for address in addresses]

links = [address.get("href") for address in addresses]

links_listings = []

for link in links:
    if link.find("https:") == -1:
        link = "https://www.zillow.com" + link
    links_listings.append(link)


s = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=s,options=options)
driver.maximize_window()

time.sleep(4)

for i in range(len(links_listings)):
    driver.get(GOOGLE_DOC_FILE)
    time.sleep(1)
    write_price = driver.find_element("xpath",'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    write_price.send_keys(prices_per_month[i])
    time.sleep(1)
    write_address = driver.find_element("xpath",'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    write_address.send_keys(addresses_listings[i])
    time.sleep(1)
    write_link = driver.find_element("xpath",'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    write_link.send_keys(links_listings[i])
    time.sleep(1)

    button = driver.find_element("xpath", '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    button.click()







