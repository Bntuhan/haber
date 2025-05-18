import streamlit as st
import xml.etree.ElementTree as et
import sqlitecloud
import sqlite3
import requests
from datetime import date
from google import genai
from pydantic import BaseModel
from fonksiyonlar import trendgetir

diller=["TR","DE","IT","KR","FR","NL","DK"]

guncelle=st.sidebar.button("Haberleri Güncelle")

if guncelle:
    for dil in diller:
        trendgetir(dil)

dilsecimi=st.multiselect("Ülke Seç",diller)
ara=st.text_input("Haber İçinde Arama Yap")

conn=sqlitecloud.connect('sqlitecloud://cyql96oxhk.g3.sqlite.cloud:8860/chinook.sqlite?apikey=VCgODu4MWtgTc4FfUmMWQwdhrYpj0WRs9vhFtNIgEB4')
c=conn.cursor()
placeholders = ','.join('?' for _ in dilsecimi)
query = f"SELECT * FROM haberler WHERE dil IN ({placeholders}) ORDER BY trend_id DESC LIMIT 99"
c.execute(query, dilsecimi)

if len(ara) > 1:
    if len(dilsecimi) > 0:
        placeholders = ','.join(['?'] * len(dilsecimi))
        query = f"SELECT * FROM haberler WHERE baslik LIKE ? AND dil IN ({placeholders}) ORDER BY trend_id DESC LIMIT 99"
        params = [f"%{ara}%"] + dilsecimi
        c.execute(query, params)
    else:
        c.execute("SELECT * FROM haberler WHERE baslik LIKE ? ORDER BY trend_id DESC LIMIT 99", (f"%{ara}%",))
else:
    if len(dilsecimi) > 0:
        placeholders = ','.join(['?'] * len(dilsecimi))
        query = f"SELECT * FROM haberler WHERE dil IN ({placeholders}) ORDER BY trend_id DESC LIMIT 99"
        c.execute(query, dilsecimi)
    else:
        c.execute("SELECT * FROM haberler ORDER BY trend_id DESC LIMIT 99")
else:
    if len(dilsecimi) > 0:
        placeholders = ','.join('?' for _ in dilsecimi)
        query = f"SELECT * FROM haberler WHERE dil IN ({placeholders}) ORDER BY trend_id DESC LIMIT 99"
        c.execute(query, dilsecimi)
    else:
        c.execute("SELECT * FROM haberler ORDER BY trend_id DESC LIMIT 99")
