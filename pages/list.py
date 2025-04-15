import streamlit as st 
import pandas as pd
import base64
import datetime
from pages.add_items import lines




sort_items = sorted(lines)

with st.sidebar:
  selected = st.multiselect("Pick items",sort_items)
  if selected:
    pd.DataFrame(selected)
    
def download_link(object_to_download, download_filename, download_link_text):
  
  if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
  b64 = base64.b64encode(object_to_download.encode()).decode()

  return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
    
df = pd.DataFrame(selected)
st.write(df)

filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

if st.button('Download file'):
    tmp_download_link = download_link(df, 'Item-list_' + filename +'.txt', 'Click here to download your file!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)

    
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color:  #181818;color:white;;
}
</style>""", unsafe_allow_html=True)

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #abc2cf;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    [data-testid=stMain] {
      background-color:#817499;
    }
    [data-testid=stHeader] {
      
      background-color:#180245
    }
    </style>
    """,
    unsafe_allow_html=True
)
