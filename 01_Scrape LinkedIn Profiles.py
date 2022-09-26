#!/usr/bin/env python
# coding: utf-8

# In[35]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass

# Get userID, pwd and skill.

email=input("Please enter LinkedIn username: ")
print("Please enter LinkedIn password: ")
pwd=getpass.getpass()
skill=input("Enter the most important skill needed for this job role: ")

# Prepare LinkedIn URL for link to people with the requested skills

keywords=skill.split(" ")
skill_link = "https://www.linkedin.com/search/results/people/?geoUrn=%5B%22115702354%22%5D&keywords="

for k in range(len(keywords)):
    if(k==0):
        skill_link += keywords[k]
    else:
        skill_link += ("%20" + keywords[k])
 

# Get the browser object

browser = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\chromedriver.exe')

# Open Login URL

browser.get("https://www.linkedin.com/login")
browser.maximize_window()

# Sign in to LinkedIn

try:
    elt = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID,'username')))
    elt.send_keys(email)
    elt = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID,'password')))
    elt.send_keys(pwd)
    elt.send_keys(Keys.RETURN)
except Exception as e:
    print("ERROR: " , e)
 

# Inside Linkedin, go to the "search results page" where you can see people with the requested skill

browser.get(skill_link)

try:
    # Wait for link to load
    time.sleep(5)

    # Find all elements where there is a profile link
    elts = browser.find_elements(By.CLASS_NAME,'app-aware-link')
    links=[]
    for we in elts:
        if(("View" in (we.text)) and ("profile" in (we.text))):
            links.append(we.get_attribute("href"))
   

    # For each profile link, click on profile, click on More > Save to PDF to save their resume to default Downloads OS location

    for l in links:
        browser.get(l)
        time.sleep(2)
        elt=WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH,'''/html[1]
        /body[1]/div[6]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[1]/div[2]/div[3]/div[1]/div[3]
        /button[1]''')))
        time.sleep(1)
        elt.click()
        elt=WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,'''/html[1]
        /body[1]/div[6]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[1]/div[2]/div[3]/div[1]/div[3]
        /div[1]/div[1]/ul[1]/li[3]/div[1]/span[1]''')))
        time.sleep(1)
        elt.click()
        time.sleep(20)
       
    # Once downloads are complete, quit browser
    browser.quit()
       
except Exception as e:
    print("ERROR: ",e)

