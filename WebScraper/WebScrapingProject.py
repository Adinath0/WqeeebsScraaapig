import streamlit as st
from tofler import tofler_func
from zauba import zauba_func
import time
flag=0
file=open('auto_data.txt','r+')
data=file.readlines()
all_stocks=[i.title().replace(" Pvt.","").replace(" Ltd.","").replace(" Ltd","").replace(" Pvt","").strip() for i in data]
all_stocks.append("")
all_stocks.append("Other Option")
all_stocks=list(sorted(set(all_stocks)))
st.set_page_config("Data Scraper Project")
st.markdown("""
<style>
.css-d1b1ld.edgvbvh6
{
  visibility:hidden;
}
.css-1v8iw7l.eknhn3m4
{
  visibility:hidden;
}
#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.stAppViewBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div.stForm.st-emotion-cache-4uzi61.e10yg2by1 > div > div > div > div:nth-child(2) > div > div > div > div > svg
{
  visibility:hidden;
}

</style>
""",unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>Data Scraping Website</h1>",unsafe_allow_html=True)
form1 = st.form("Details")
comp = form1.radio("From which site do you want to access the data?",["Tofler","Zauba"])
data = form1.selectbox("Enter the company name : (If name is not listed in the list, then write 'Other Option')",options=all_stocks,placeholder="Type Here...")
submit = form1.form_submit_button("Submit")
form2 = st.form("Details2")
process1=st.empty()
process2=st.empty()
process1.markdown("<h3 style='text-align:center;'>Demo of How The Website Works</h3>",unsafe_allow_html=True)
process2.video("demo.mp4")
while submit:
  if(data=='Other Option' or data==''):
    flag=1
    data = form1.text_input("Enter company name here: ",)
  else:
    process2.text("")
    process1.text("")
    if comp=="Tofler":
      st.write("Fetching details from "+comp)
      try:
        ret = tofler_func(data,flag)
        if(flag==1):
          re_li=["Ltd.","Ltd","Limited","Private","Pvt.","Pvt","Llp"]
          for j in re_li:
            s=ret.title().replace(j,"")
          s.strip()
          s=s.split()
          s=s[:min(len(s),2)]
          s=" ".join(s)
          if(s not in all_stocks):
            f=open("auto_data.txt","a")
            f.write(s+"\n")
            f.close()
      except Exception:
        st.write("""The site landed onto an error while handling the request.
                    Kindly search again.
                    If still the error pertains, then the company might not be listed on the particular website.
                    Try searching for some other company.
                 """)
    elif comp=="Zauba":
      st.write("Fetching details from "+comp)
      try:
        ret = zauba_func(data,flag)
        if(flag==1):
          re_li=["Ltd.","Ltd","Limited","Private","Pvt.","Pvt"]
          for j in re_li:
            s=ret.title().replace(j,"")
          if(s not in all_stocks):
            f=open("auto_data.txt","a")
            f.write(s+"\n")
            f.close()
      except Exception:
        st.write("""The site landed onto an error while handling the request.
                    Kindly search again.
                    If still the error pertains, then the company might not be listed on the particular website.
                    Try searching for some other company.
                 """)
    break