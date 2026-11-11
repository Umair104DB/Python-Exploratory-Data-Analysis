import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
st.set_page_config(page_title='EDA Workbench',page_icon='🔎',layout='wide')
st.title('🔎 Exploratory Data Analysis Workbench')
df=pd.read_csv(Path(__file__).parent/'data/sales_100_rows.csv',parse_dates=['date'])
up=st.file_uploader('Optional: upload your own CSV',type='csv')
if up:
    try: df=pd.read_csv(up)
    except Exception as e: st.error(f'Unable to read CSV: {e}')
a,b,c=st.columns(3); a.metric('Rows',len(df)); b.metric('Columns',len(df.columns)); c.metric('Missing cells',int(df.isna().sum().sum()))
st.subheader('Dataset preview'); st.dataframe(df.head(20),use_container_width=True)
st.subheader('Data types and quality'); st.dataframe(pd.DataFrame({'dtype':df.dtypes.astype(str),'missing':df.isna().sum(),'unique':df.nunique()}),use_container_width=True)
st.subheader('Numerical summary'); st.dataframe(df.describe(include='all').transpose(),use_container_width=True)
num=df.select_dtypes('number')
if not num.empty:
    col=st.selectbox('Choose a numeric column',num.columns)
    fig,ax=plt.subplots(); num[col].dropna().hist(ax=ax,bins=20); ax.set_title(f'Distribution of {col}'); st.pyplot(fig)
    st.write('Correlation matrix'); st.dataframe(num.corr(numeric_only=True).round(2),use_container_width=True)
st.download_button('Download cleaned CSV',df.drop_duplicates().to_csv(index=False).encode(),file_name='cleaned_data.csv',mime='text/csv')
