import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df = sns.load_dataset('iris')

st.write("1. matplotlib")

fig1, ax1 = plt.subplots()
ax1.scatter(df['sepal_length'], df['sepal_width'], label='Sepal', color='blue', s=15)
ax1.set_title('Iris Sepal Dimensions')
ax1.set_xlabel('Sepal Length')
ax1.set_ylabel('Sepal Width')
ax1.legend()

st.pyplot(fig1)

# ──────────────────────────────────────────────────────────
st.write("2. seaborn")

fig2, axes = plt.subplots(2, 1, figsize=(7, 9))

sns.histplot(data=df, x='petal_length', kde=True, bins=20, ax=axes[0])
axes[0].set_title('Petal Length Distribution')

sns.boxplot(data=df, x='species', y='petal_length', color='tab:blue', ax=axes[1])
axes[1].set_title('Petal Length by Species')

plt.tight_layout()
st.pyplot(fig2)

# ──────────────────────────────────────────────────────────
st.write("3. plotly")

fig3 = px.scatter(df, x='sepal_length', y='sepal_width', color='species', title='Interactive Iris Sepal Scatter Plot')
st.plotly_chart(fig3)

fig4 = px.line(df, x='sepal_length', y='sepal_width', color='species', title='Interactive Iris Sepal Line Chart')
st.plotly_chart(fig4)