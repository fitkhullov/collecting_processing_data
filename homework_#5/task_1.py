from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exc
from pymongo import MongoClient
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from time import sleep

ip = '127.0.0.1'
port = 27017
client = MongoClient(ip, port)

db = client['mvideo']
products = db.products

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome('chromedriver.exe')
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.mvideo.ru/')
sleep(5)
driver.execute_script('window.scrollTo(0, 1700)')

wait = WebDriverWait(driver, 5)
button = wait.until(exc.element_to_be_clickable((By.XPATH, '//*[@class="page-carousel-padding ng-star-inserted"]//button[@class="tab-button ng-star-inserted"]')))
button.click()

while True:
    try:
        button = wait.until(exc.element_to_be_clickable((By.XPATH, '//mvid-shelf-group/*/div[2]/button[2]')))
        button.click()
    except (ElementNotInteractableException, TimeoutException):
        break

elements = driver.find_elements(By.XPATH, "//mvid-shelf-group/mvid-carousel/div[1]//div[@class='title']")
product = {'name': None,
           'link': None,
           'price': None,
           '_id': None
           }

for x in elements:
    link = x.find_element(By.TAG_NAME, 'a').get_attribute('href')
    driver.execute_script(f'window.open("{link}", "_blank")')
    driver.switch_to.window(driver.window_handles[1])
    #wait.until(exc.element((By.XPATH, "//button[@class='button button--with-icon ng-star-inserted']")))
    sleep(4)
    name = driver.find_element(By.XPATH, '//h1[@class="title"]').text
    price = driver.find_element(By.XPATH, '//span[@class="price__main-value"][1]').text
    product['name'], product['link'], product['price'], product['_id'] = name, link, price, link.replace('https://www.mvideo.ru/products/', '')
    if not products.find_one({'link': link}):
        products.insert_one(product)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
driver.quit()
