import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_HOST = os.getenv('DB_HOST', '')
DB_PORT = os.getenv('DB_PORT', '')
DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', '')

try:
    db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(db_url)
except Exception as e:
    st.error("DB 연결 설정 오류. 환경변수를 확인해주세요.")

@st.cache_data
def load_stock_list():
    with engine.connect() as conn:
        query = "SELECT id, name FROM tb_stock"
        return pd.read_sql(query, conn)

@st.cache_data
def load_stock_price(stock_id):
    with engine.connect() as conn:
        query = f"""
            SELECT p.created_at, p.price, s.name 
            FROM tb_price p
            JOIN tb_stock s ON p.stock_id = s.id
            WHERE p.stock_id = {stock_id}
            ORDER BY p.created_at ASC
        """
        df = pd.read_sql(query, conn)
        return df.tail(1000)

st.title("주식 종목 데이터 조회")

try:
    stocks_df = load_stock_list()
    
    if not stocks_df.empty:
        selected_stock_name = st.selectbox("조회할 종목을 선택하세요", stocks_df['name'])
        
        selected_stock_id = stocks_df[stocks_df['name'] == selected_stock_name]['id'].values[0]
        
        price_df = load_stock_price(selected_stock_id)
        
        if not price_df.empty:
            st.write(f"### {selected_stock_name} 상세 정보")
            price_df = price_df.rename(columns={'created_at': 'Time'})
            st.line_chart(data=price_df, x='Time', y='price')
            
            with st.expander("원본 데이터 보기"):
                st.dataframe(price_df)
        else:
            st.info(f"{selected_stock_name}의 가격 데이터가 아직 없습니다.")
            
    else:
        st.warning("종목 목록이 비어있습니다.")
        
except Exception as e:
    st.error(f"데이터베이스 연결 또는 쿼리 실행 중 오류가 발생했습니다: {e}")