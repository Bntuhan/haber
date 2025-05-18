import streamlit as st
import xml.etree.ElementTree as et
import sqlitecloud
import sqlite3
import requests
from datetime import date
from google import genai
from pydantic import BaseModel
from fonksiyonlar import trendgetir
diller=["TR","DE","IT","KR","NL","DK","FR"]

guncelle=st.sidebar.button("Haberleri Güncelle")
for dil in diller:
    trendgetir(dil)
    

ara=st.text_input("Haber İçinde Arama Yap")

conn=sqlitecloud.connect('sqlitecloud://cyql96oxhk.g3.sqlite.cloud:8860/chinook.sqlite?apikey=VCgODu4MWtgTc4FfUmMWQwdhrYpj0WRs9vhFtNIgEB4')
c=conn.cursor()

if len(ara)>1:
    c.execute(f"SELECT * FROM haberler WHERE baslik LIKE '%{ara}%' ORDER BY trend_id DESC LIMIT 99 ")

else:
    c.execute("SELECT * FROM haberler ORDER BY trend_id DESC LIMIT 99")
    
haberler=c.fetchall()

if len(haberler)==0:
    st.warning(f" {ara} sorgusu ile ilgili Herhangi Bir Haber bulunamadı")

for i in range(0,len(haberler),3):
    col1,col2,col3=st.columns(3)

    with col1:
        st.image(haberler[i][3])
        st.write(haberler[i][1])
        st.link_button("Habere Git",haberler[i][2])
    with col2:
        if i+1 < len(haberler):
            st.image(haberler[i+1][3])
            st.write(haberler[i+1][1])
            st.link_button("Habere Git",haberler[i+1][2])
        else:
            pass

    with col3:
        if i+2 < len(haberler):
            st.image(haberler[i+2][3])
            st.write(haberler[i+2][1])
            st.link_button("Habere Git",haberler[i+2][2])
        else:
            pass
