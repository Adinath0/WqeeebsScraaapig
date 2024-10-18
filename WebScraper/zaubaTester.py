import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
def zauba_func(data):
    chrome_options=Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument("--window-size=1,1")
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    driver.get("https://www.zaubacorp.com/")
    driver.minimize_window()
    # print("A")
    input_company = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='searchid']")))
    # print("B")
    search_box=driver.find_element(By.XPATH,'//*[@id="searchid"]')
    search_box.send_keys(data)
    # print("C")
    wait=WebDriverWait(driver,10)
    a=wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/section/div/div[1]/div/section[2]/form/div/div/div[3]/div[1]')))
    # print("D")
    search_box=driver.find_element(By.XPATH,"/html/body/section/div/div[1]/div/section[2]/form/div/div/div[3]/div[1]")
    search_box.click()
    driver.implicitly_wait(10)
    # print("E")
    company_name=driver.find_element(By.XPATH,'//*[@id="title"]').text
    # print("F")
    st.write(f"<h2>Overview of Company - {company_name}</h2>",unsafe_allow_html=True)      
    company_overview=driver.find_element(By.XPATH,'//*[@id="about"]').text
    # print("G")
    st.write(company_overview)
    st.write("<h2>Company Details</h2>",unsafe_allow_html=True)
    table_data=[]
    table_ele = driver.find_element(By.XPATH,'//*[@id="company-information"]/div/div/table/tbody')
    rows=table_ele.find_elements(By.TAG_NAME,'tr')
    for row in rows:
      row_data=[cell.text for cell in row.find_elements(By.TAG_NAME,'td')]
      table_data.append(row_data)
    df=pd.DataFrame(table_data,columns=['Topic','Value'])
    df.index=df.index+1
    st.write(df)
    st.write("<h2>Director details</h2>",unsafe_allow_html=True)
    st.write("<h3>Current Directors & Key Managerial Personnel</h3>",unsafe_allow_html=True)
    # headers=["DIN","Director Name","Designation","Appointment Date"]
    headers=[]
    table_head = driver.find_elements(By.XPATH,'//*[@id="director-information-content"]/div[1]/table/thead/tr/th')
    headers = [i.text for i in table_head]
    
    table_data=[]
    table_body = driver.find_elements(By.XPATH,'//*[@id="director-information-content"]/div[1]/table/tbody/tr')
    i=0
    for i in range(1,len(table_body)+1):
      din=driver.find_element(By.XPATH,f'//*[@id="director-information-content"]/div[1]/table/tbody/tr[{i}]/td[1]').text
      year=driver.find_element(By.XPATH,f'//*[@id="director-information-content"]/div[1]/table/tbody/tr[{i}]/td[4]').text
      name=driver.find_element(By.XPATH,f'//*[@id="director-information-content"]/div[1]/table/tbody/tr[{i}]/td[2]').text
      designation=driver.find_element(By.XPATH,f'//*[@id="director-information-content"]/div[1]/table/tbody/tr[{i}]/td[3]').text
      table_data.append([din,name,designation,year])
    df=pd.DataFrame(table_data,columns=headers)
    df.index=df.index+1
    st.write(df)
    st.write("<h3>Past Directors & Key Managerial Personnel</h3>",unsafe_allow_html=True)
    # headers=["DIN","Director Name","Designation","Appointment Date","Cessation"]
    headers=[]
    table_head = driver.find_elements(By.XPATH,'//*[@id="director-information-content"]/div[2]/table/thead/tr/th')
    headers = [i.text for i in table_head]
    table_data=[]
    table_body = driver.find_elements(By.XPATH,'//*[@id="director-information-content"]/div[2]/table/tbody/tr')
    i=0
    for i in range(1,len(table_body)+1):
      din=driver.find_element(By.XPATH,f'//*[@id="director-information-content"]/div[2]/table/tbody/tr[{i}]/td[1]').text
      year=driver.find_element(By.XPATH,f'//*[@id="director-information-content"]/div[2]/table/tbody/tr[{i}]/td[4]').text
      name=driver.find_element(By.XPATH,f'//*[@id="director-information-content"]/div[2]/table/tbody/tr[{i}]/td[2]').text
      designation=driver.find_element(By.XPATH,f'//*[@id="director-information-content"]/div[2]/table/tbody/tr[{i}]/td[3]').text
      cess=driver.find_element(By.XPATH,f'//*[@id="director-information-content"]/div[2]/table/tbody/tr[{i}]/td[5]').text
      table_data.append([din,name,designation,year,cess])
    df=pd.DataFrame(table_data,columns=headers)
    df.index=df.index+1
    st.write(df)
    # st.write("<h2>Charges (Secured Loans) of Company</h2>",unsafe_allow_html=True)
    # headers=[]
    # table_head = driver.find_elements(By.XPATH,'//*[@id="charges-content"]/div/table/thead/tr/th')
    # headers = [i.text for i in table_head]
    # table_data=[]
    # table_body = driver.find_elements(By.XPATH,'//*[@id="charges-content"]/div/table/tbody/tr')
    # i=0
    # for i in range(1,len(table_body)+1):
    #   table_body1 = driver.find_elements(By.XPATH,f'//*[@id="charges-content"]/div/table/tbody/tr{i}/td')
    #   table_data.append([i.text for i in table_body1])
    #   print(table_data[-1])
    # df=pd.DataFrame(table_data,columns=headers)
    # df.index=df.index+1
    # st.write(df)
    st.write("<h2>Contacts</h2>",unsafe_allow_html=True)
    company_overview=driver.find_elements(By.XPATH,'//*[@id="contact-details-content"]/div[1]/span')
    company_overview1="<br>".join([i.text for i in company_overview])
    st.write(company_overview1,unsafe_allow_html=True)
    #Error for maps
    # iframe=driver.find_element(By.XPATH,'//*[@id="contact-details-content"]/div[2]/iframe')
    # driver.switch_to.frame(iframe)
    # ss=driver.get_screenshot_as_png()
    # image=Image.open(io.BytesIO(ss))
    # st.image(image,use_column_width=True)
    driver.quit()