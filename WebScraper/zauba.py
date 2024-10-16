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
    input_company = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='searchid']")))
    search_box=driver.find_element(By.XPATH,'//*[@id="searchid"]')
    search_box.send_keys(data)
    wait=WebDriverWait(driver,10)
    a=wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/section/div/div[1]/div/section[2]/form/div/div/div[3]/div[1]')))
    search_box=driver.find_element(By.XPATH,"/html/body/section/div/div[1]/div/section[2]/form/div/div/div[3]/div[1]")
    search_box.click()
    driver.implicitly_wait(10)
    company_name=driver.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/section/div[3]/section/div[1]/h1').text
    st.write(f"<h2>Overview of Company - {company_name}</h2>",unsafe_allow_html=True)      
    company_overview=driver.find_element(By.XPATH,'/html/body/div[6]/div/div[1]/section/div[3]/section/div[2]/div[1]').text
    company_overview=company_overview[:company_overview.index("Company Details")]
    st.write(company_overview)
    st.write("<h2>Company Details</h2>",unsafe_allow_html=True)
    table_frow = driver.find_element(By.XPATH,'//*[@id="block-system-main"]/div[2]/div[1]/div[1]/div[2]/table/thead/tr')
    table_data=[]
    row_data=[cell.text for cell in table_frow.find_elements(By.TAG_NAME,'td')]
    table_data.append(row_data)
    table_ele = driver.find_element(By.XPATH,'//*[@id="block-system-main"]/div[2]/div[1]/div[1]/div[2]/table/tbody')
    rows=table_ele.find_elements(By.TAG_NAME,'tr')
    for row in rows:
      row_data=[cell.text for cell in row.find_elements(By.TAG_NAME,'td')]
      table_data.append(row_data)
    df=pd.DataFrame(table_data,columns=['Topic','Value'])
    df.index=df.index+1
    st.write(df)
    st.write("<h2>Director details</h2>",unsafe_allow_html=True)
    headers=["DIN","Director Name","Designation","Appointment Date"]
    table_data=[]
    table_body = driver.find_elements(By.XPATH,'//*[@id="block-system-main"]/div[2]/div[1]/div[7]/table/tbody/tr')
    i=0
    for i in range(1,len(table_body)+1):
      if(i%2==0):
        continue
      j=i//2+1
      din=driver.find_element(By.XPATH,f'//*[@id="package{j}"]/td[1]').text
      year=driver.find_element(By.XPATH,f'//*[@id="package{j}"]/td[4]').text
      name=driver.find_element(By.XPATH,f'//*[@id="package{j}"]/td[2]').text
      designation=driver.find_element(By.XPATH,f'//*[@id="package{j}"]/td[3]').text
      table_data.append([din,name,designation,year])
    df=pd.DataFrame(table_data,columns=headers)
    df.index=df.index+1
    st.write(df)
    st.write("<h2>Contacts</h2>",unsafe_allow_html=True)
    company_overview=driver.find_elements(By.XPATH,'//*[@id="block-system-main"]/div[2]/div[1]/div[5]/div/div[1]/p')
    company_overview1="<br>".join([i.text for i in company_overview])
    st.write(company_overview1,unsafe_allow_html=True)
    #Error for maps
    # iframe=driver.find_element(By.XPATH,'//*[@id="block-system-main"]/div[2]/div[1]/div[5]/div/div[2]/iframe')
    # driver.switch_to.frame(iframe)
    # ss=driver.get_screenshot_as_png()
    # image=Image.open(io.BytesIO(ss))
    # st.image(image,use_column_width=True)
    driver.quit()