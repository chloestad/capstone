import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, engine, text
import matplotlib.pyplot as plt
import requests

# @st.cache_data
@st.experimental_memo
def load_data(response_json):
    try:
        data = pd.json_normalize(response_json, "result")
        return data
    except Exception as e:
        print(e)

# -------------------------- Customers --------------------------
response_customers = requests.get("https://api-dot-titanium-vim-377008.oa.r.appspot.com/api/customer")
response_json_customers = response_customers.json()

customers_data = load_data(response_json_customers)

age_data = customers_data.loc[:,['age', 'customer_id']]
st.write("## Customer Ages data")
st.dataframe(age_data)

# Plot a histogram of the age data
st.write("### Histogram of Customer Ages")
fig, ax = plt.subplots()
pd.DataFrame.hist(age_data, bins=20, ax=ax)
st.pyplot(fig)

# -------------------------- Articles --------------------------
response_articles = requests.get("https://api-dot-titanium-vim-377008.oa.r.appspot.com/api/articles")
response_json_articles = response_articles.json()

articles_data = load_data(response_json_articles)
st.write("## Articles data")
st.dataframe(articles_data)

# -------------------------- Transactions --------------------------
response_transactions= requests.get("https://api-dot-titanium-vim-377008.oa.r.appspot.com/api/transactions")
response_json_transactions = response_transactions.json()

transactions_data = load_data(response_json_transactions)
st.write("## Transactions data")
st.dataframe(transactions_data)