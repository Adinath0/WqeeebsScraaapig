import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
def tofler_func(data):
    chrome_options=Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    driver.get("https://www.tofler.in/")
    search_box=driver.find_element(By.XPATH,"/html/body/div[3]/div/div/form/div/input")
    search_box.send_keys(data)
    wait=WebDriverWait(driver,10)
    a=wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/ul/li[1]")))
    search_box=driver.find_element(By.XPATH,"/html/body/ul/li[1]")
    search_box.click()
    wait=WebDriverWait(driver,10)
    a=wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="overview"]/div/h2')))
    company_name=driver.find_element(By.XPATH,'//*[@id="overview"]/div/h2').text[11:]
    st.write(f"<h2>Overview of Company - {company_name}</h2>",unsafe_allow_html=True)      
    company_overview=driver.find_elements(By.XPATH,'//*[@id="overview"]/div/p')
    company_overview1="\n".join([i.text for i in company_overview])
    st.write(company_overview1)
    st.write("<h2>Director details</h2>",unsafe_allow_html=True)
    company_director=driver.find_elements(By.XPATH,'//*[@id="overview_directors"]/div/p')
    company_director1="\n".join([i.text for i in company_director])
    st.write(company_director1)
    headers=["Name","Designation","Year"]
    table_data=[]
    table_body = driver.find_element(By.XPATH,'//*[@id="directors-timeline-table"]')
    driver.execute_script("arguments[0].removeAttribute('style');",table_body)
    table_fbody=table_body.find_element(By.TAG_NAME,'tbody')
    table_rows=table_fbody.find_elements(By.TAG_NAME,'tr')
    for i in table_rows:
      table_d=i.find_elements(By.TAG_NAME,'td')
      table_da=[cell.text for cell in table_d[:3]]
      table_data.append(table_da)
    df=pd.DataFrame(table_data,columns=headers)
    df.index=df.index+1
    st.write(df)
    st.write("<h2>Company Network</h2>",unsafe_allow_html=True)
    company_network=driver.find_element(By.XPATH,'//*[@id="companyNetwork"]/div/a/img')
    company_network1=company_network.get_attribute('src')
    st.image(company_network1,use_column_width=True)
    st.write("<h2>Company Finance</h2>",unsafe_allow_html=True)
    finance_button=driver.find_element(By.XPATH,'//*[@id="financials-tab"]')
    finance_button.click()
    driver.implicitly_wait(5)
    table_ele = driver.find_element(By.XPATH,'//*[@id="financial-details-financial-tab"]/div/table/tbody')
    rows=table_ele.find_elements(By.TAG_NAME,'tr')
    table_data=[]
    for row in rows:
      row_data=[cell.text for cell in row.find_elements(By.TAG_NAME,'td')]
      table_data.append(row_data)
    df=pd.DataFrame(table_data,columns=['Topic','Value'])
    df.index=df.index+1
    st.write(df)
    st.write("Note: If all the values in table are 000000, means the data is kept confidential by the company.")