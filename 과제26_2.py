import streamlit as st
import plotly.express as px
import seaborn as sns

df = sns.load_dataset('iris')

fig = px.scatter(df, x='sepal_length', y='sepal_width', color='species', title='All Species')

fig.update_layout(
    updatemenus=[
        dict(
            direction="down",
            showactive=True,
            x=0.0,
            xanchor="left",
            y=1.1,
            yanchor="top",
            buttons=list([
                dict(
                    label="All",
                    method="update",
                    args=[{"visible": [True, True, True]}, 
                          {"title": "All Species"}]
                ),
                dict(
                    label="Setosa",
                    method="update",
                    args=[{"visible": [True, False, False]}, 
                          {"title": "Setosa"}]
                ),
                dict(
                    label="Versicolor",
                    method="update",
                    args=[{"visible": [False, True, False]}, 
                          {"title": "Versicolor"}]
                ),
                dict(
                    label="Virginica",
                    method="update",
                    args=[{"visible": [False, False, True]}, 
                          {"title": "Virginica"}]
                )
            ])
        )
    ]
)

st.plotly_chart(fig)