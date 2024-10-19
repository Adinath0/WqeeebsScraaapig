import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from IPython.display import Image,display

def tofler_func(data,flag):
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
    try:  
      company_overview=driver.find_elements(By.XPATH,'//*[@id="overview"]/div/p')
      company_overview1="\n".join([i.text for i in company_overview])
      st.write(company_overview1)
    except Exception:
      st.write("Company Overview not available")
    finally:
      st.write("<h2>Director details</h2>",unsafe_allow_html=True)
      try:
        company_director=driver.find_elements(By.XPATH,'//*[@id="overview_directors"]/div/p')
        company_director1="\n".join([i.text for i in company_director])
        st.write(company_director1)
      except Exception:
        st.write("Director details not available")
      finally:
        try:
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
        except Exception:
          st.write("Director details table not available")
        finally:
          st.write("<h2>Company Network</h2>",unsafe_allow_html=True)
          try:
            company_network=driver.find_element(By.XPATH,'//*[@id="companyNetwork"]/div/a/img')
            company_network1=company_network.get_attribute('src')
            st.image(company_network1,use_column_width=True)
          except Exception:
            st.write("Company Network not available")
          finally:
            st.write("<h2>Company Finance</h2>",unsafe_allow_html=True)
            try:
              finance_button=driver.find_element(By.XPATH,'//*[@id="financials-tab"]')
              finance_button.click()
              driver.implicitly_wait(5)
              table_ele = driver.find_element(By.XPATH,'//*[@id="financial-details-financial-tab"]/div/table/tbody')
              rows=table_ele.find_elements(By.TAG_NAME,'tr')
              table_data=[]
              for row in rows[:len(rows)-1]:
                row_data=[cell.text for cell in row.find_elements(By.TAG_NAME,'td')]
                sec_td=row.find_elements(By.TAG_NAME,'td')[1]

                try:
                  print('A')
                  sec_td=row.find_elements(By.TAG_NAME,'td')[1]
                  print('B')
                  sec_v = sec_td.find_element(By.TAG_NAME,'i')
                  print('C')
                  class_val = sec_v.get_attribute('class').split()
                  print(class_val)
                  if 'fa-caret-up' in class_val:
                    row_data.append('<img src="positive.png">')
                  elif 'fa-caret-down' in class_val:
                    row_data.append('<img src="negative.png">')
                except Exception:
                  print("D")
                  row_data.append('')
                finally:
                  print("E")
                  table_data.append(row_data)
                  continue
              print(table_data)
              df=pd.DataFrame(table_data,columns=['Topic','Value','Profit or Loss'])
              df.index=df.index+1
              print(df["Value"])
              c2=0
              #st.write(df,unsafe_allow_html=True)
              for i in df["Value"]:
                if(i=='000000'):
                  c2+=1
              if(c2==0):
                st.write(df,unsafe_allow_html=True)
              else:
                st.write("Table not made public on the website by the company")
              #st.write("Note: If all the values in table are 000000, means the data is kept confidential by the company.")
            except Exception:
              st.write("Company Finance not available")
            finally:
              if(flag==1):
                return company_name