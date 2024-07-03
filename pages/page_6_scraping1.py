from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import streamlit as st
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")


#Open new browser window
driver = webdriver.Chrome(options=chrome_options)

#Browser goes to auth_url
driver.get('http://example.com')

# #Sets up waiting until the second url to copy the new url
# wait = WebDriverWait(driver, 170)
# wait.until(EC.url_contains("code="))
# url = driver.current_url

#closes window
driver.close()
st.write('done')