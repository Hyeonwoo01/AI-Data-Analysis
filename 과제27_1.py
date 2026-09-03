import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=1000, key="stock_refresh")

engine = create_engine('sqlite:///stocks.db')

def load_data():
    with engine.connect() as conn:
        query = "SELECT * FROM stocks ORDER BY timestamp DESC LIMIT 200"
        df = pd.read_sql(query, conn)
        return df.iloc[::-1].reset_index(drop=True)

try:
    df = load_data()
    
    if not df.empty:
        st.title("Real-Time Stock Dashboard")
        
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        price_change = latest['price'] - prev['price']
        volume_change = latest['volume'] - prev['volume']
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Latest Price", f"${latest['price']:.2f}")
        col2.metric("Latest Volume", f"{int(latest['volume'])}")
        
        col3.metric("Price Change", f"${abs(price_change):.2f}", f"{price_change:.2f}")
        col4.metric("Volume Change", f"{abs(int(volume_change))}", f"{int(volume_change)}")
        
        fig = make_subplots(
            rows=2, cols=1, 
            shared_xaxes=True,
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3]
        )
        
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['price'], mode='lines', name='Price', line=dict(color='#FF4B4B')), 
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(x=df['timestamp'], y=df['volume'], name='Volume', marker_color='#1f77b4'), 
            row=2, col=1
        )
        
        fig.update_layout(
            title_text="Stock Price and Volume",
            height=600,
            showlegend=False,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.info("데이터베이스가 비어 있습니다. `fake_stock.py`를 먼저 실행해주세요.")
        
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")