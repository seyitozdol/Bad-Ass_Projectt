import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import seaborn as sns
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objs as go
import plotly.tools as tls


#pip install streamlit-card


warnings.filterwarnings('ignore')

st.set_page_config(page_title="CRM Page - TeamBadass!!!", page_icon=":trident:", layout="wide")


st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

tabs = ["Anasayfa", "Özet", "Grafikler", "Kampanyalar"]

page = st.sidebar.radio("Sayfalar", tabs)

st.sidebar.markdown("""[team Badass](https://media3.giphy.com/media/15BuyagtKucHm/giphy.gif?cid=ecf05e47rn7ztuz2i971hwvwqijy4oirbwmx8jal9bcwjzae&ep=v1_gifs_search&rid=giphy.gif&ct=g)""")

logo = Image.open('goku.png')
st.image(logo)

@st.cache_data
def load_data(x):
    df = pd.read_excel(x)
    return df

df = load_data("main.xlsx")



if page == "Özet":
    startDate = pd.to_datetime(df["Date"]).min()
    endDate = pd.to_datetime(df["Date"]).max()

    date1 = pd.to_datetime(st.date_input("Başlangıç Tarihi", startDate))
    date2 = pd.to_datetime(st.date_input("Bitiş Tarihi", endDate))

    df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()

    total_days = (df['Date'].max() - df['Date'].min()).days + 1
    total_weeks = total_days // 7
    total_months = total_days // 30
    total_years = total_days // 364
    total_customers = df['User ID'].nunique()
    total_sales_tl = df['Sales'].sum()
    total_sales_tl = total_sales_tl.astype(float)
    total_sales_quantity = df['Quantity'].sum()
    total_sales_quantity = total_sales_quantity.astype(float)

    st.title("Data Özeti")
    from streamlit_card import card

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        res = card(
            title="Toplam Gün",
            text=[total_days],
            styles={
                "card": {
                    "width": "200px",
                    "height": "200px",
                    "border-radius": "30px",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",

                },
                "text": {
                    "font-family": "serif",
                    "font-size": "30px",

                }
            },
            image="https://marketplace.canva.com/L8VEE/MAFKUaL8VEE/1/tl/canva-abstract-scene-background-MAFKUaL8VEE.jpg",
            key=1,
        )
    with col2:
        res1 = card(
            title="Toplam Hafta",
            text=[total_weeks],
            styles={
                "card": {
                    "width": "200px",
                    "height": "200px",
                    "border-radius": "30px",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",

                },
                "text": {
                    "font-family": "serif",
                    "font-size": "30px",

                }
            },
            image="https://marketplace.canva.com/L8VEE/MAFKUaL8VEE/1/tl/canva-abstract-scene-background-MAFKUaL8VEE.jpg",
            key=2,
        )
    with col3:
        res2 = card(
            title="Toplam Ay",
            text=[total_months],
            styles={
                "card": {
                    "width": "200px",
                    "height": "200px",
                    "border-radius": "30px",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",

                },
                "text": {
                    "font-family": "serif",
                    "font-size": "30px",

                }
            },
            image="https://marketplace.canva.com/L8VEE/MAFKUaL8VEE/1/tl/canva-abstract-scene-background-MAFKUaL8VEE.jpg",
            key=3,
        )


    with col4:
        res4 = card(
            title="Toplam Müşteri",
            styles={
                "card": {
                    "width": "200px",
                    "height": "200px",
                    "border-radius": "30px",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",

                },
                "text": {
                    "font-family": "serif",
                    "font-size": "30px",

                }
            },
            text=[total_customers],
            image="https://marketplace.canva.com/L8VEE/MAFKUaL8VEE/1/tl/canva-abstract-scene-background-MAFKUaL8VEE.jpg",
            key=5,
        )

    with col5:
        res5 = card(
            title="Toplam Satış Adedi",
            text=[total_sales_quantity],
            image="https://marketplace.canva.com/L8VEE/MAFKUaL8VEE/1/tl/canva-abstract-scene-background-MAFKUaL8VEE.jpg",
            key=6,
            styles={
                "card": {
                    "width": "200px",
                    "height": "200px",
                    "border-radius": "30px",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",

                },
                "text": {
                    "font-family": "serif",
                    "font-size": "30px",

                }
            }
        )
    with col6:
        res6 = card(
            title="Toplam Satış TL",
            text=[total_sales_tl],
            image="https://marketplace.canva.com/L8VEE/MAFKUaL8VEE/1/tl/canva-abstract-scene-background-MAFKUaL8VEE.jpg",
            key=7,
            styles={
                "card": {
                    "width": "200px",
                    "height": "200px",
                    "border-radius": "30px",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",

                },
                "text": {
                    "font-family": "serif",
                    "font-size": "20px",

                }
            }
        )



        # Date sütununu datetime formatına dönüştür
    df['Date'] = pd.to_datetime(df['Date'])

        # Ay bazında grupla
    grouped = df.groupby(df['Date'].dt.to_period("M"))

        # Benzersiz müşteri sayısını hesapla
    monthly_customers = grouped.nunique()['User ID']

        # Toplam satış miktarını hesapla
    monthly_sales = grouped.sum()['Sales']

        # Çizgi grafiği ve bar grafiğini aynı figürde oluştur
    fig = go.Figure()

        # Çizgi grafiği (benzersiz müşteri sayısı)
    fig.add_trace(go.Scatter(x=monthly_customers.index.astype(str), y=monthly_customers.values, mode='lines',
                                 name='Müşteri Sayısı'))

        # Bar grafiği (toplam satış miktarı) - renk skalası olarak 'Sunset' kullanıldı, farklı bir skalayı tercih edebilirsiniz.
    fig.add_trace(go.Bar(x=monthly_sales.index.astype(str), y=monthly_sales.values, name='Toplam Satış', yaxis='y2',
                             marker=dict(color=monthly_sales.values, colorscale='Sunset',
                                         )))

        # Eksenleri ayarla
    fig.update_layout(
            xaxis=dict(title='Ay'),
            yaxis=dict(title='Müşteri Sayısı'),
            yaxis2=dict(title='Toplam Satış TL', overlaying='y', side='right')

    )

    fig.update_layout(
        # Diğer ayarlarınız...
        legend=dict(
            font=dict(
                size=11  # Bu değeri istediğiniz font boyutuna göre ayarlayabilirsiniz.
            )
        )
    )
    fig.update_layout(
        # Diğer ayarlarınız...
        width=1200,  # Grafiğin genişliği
        height=800  # Grafiğin yüksekliği
    )

    st.plotly_chart(fig)

elif page == "Anasayfa":
    st.markdown("<h1 style='text-align:left;'>Nasıl Kullanılır</h1>", unsafe_allow_html=True)
    st.write("""Sol menüden gitmek istediğiniz ilgili alanı seçiniz.""")

    font_size = 30  # İstediğiniz font boyutunu burada belirleyin
    st.markdown(f"<span style='font-size:{font_size}px'>:memo:**Özet:** Bu kısımda başlangıç ve bitiş tarihlerini girdiğinizde, ilgili tarih aralığındaki genel bilgilere ulaşırsınız.</span>",
                unsafe_allow_html=True)

    st.write("""* Toplam Gün Sayısı""")
    st.write("""* Toplam Hafta Sayısı""")
    st.write("""* Toplam Ay Sayısı""")
    st.write("""* Toplam Müşteri Sayısı""")
    st.write("""* Toplam Satış Adedi""")
    st.write("""* Toplam Satış TL""")

    st.write("""\n""")
    st.markdown(
        f"<span style='font-size:{font_size}px'>:bar_chart:**Grafikler:** Bu bölümde, seçilen tarih aralığındaki aşağıdaki grafiklere ulaşırsınız.</span>",
        unsafe_allow_html=True)

    st.write("""* Segment Bazlı Satışlar""")
    st.write("""* Günlük Satışlar""")
    st.write("""* Şehir Bazlı Satışlar""")
    st.write("""* Saat Segmentine Göre Satışlar""")
    st.write("""* Güne Göre Satışlar""")
    st.write("""* Cluster Bazlı Müşteri Sayısı""")
    st.write("""* Hafta İçi ve Hafta Sonu Satış Pie Chart Grafiği""")
    st.write("""* Recency vs Frequency grafiklerine ulaşırsınız""")

    st.markdown(
        f"<span style='font-size:{font_size}px'>:spiral_calendar_pad:**Kampanyalar:** Bu bölümde kullanıcı bazlı önerilen kampanyaları ulaşabilir ve kampanya bazlı genel incelemeler yapabilirsiniz..</span>",
        unsafe_allow_html=True)






elif page == "Kampanyalar":
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col1:
        st.write(' ')

    with col2:
        st.write(' ')

    from streamlit_extras.dataframe_explorer import dataframe_explorer

    df_filtered_columns = df[["User ID"]]

    if st.button("Rastgele Kişi Seç"):
        random_value = df["User ID"].sample(1).iloc[0]
        st.write(f"Rastgele Seçilen Kişi-> : {random_value}")



    filtered_df = dataframe_explorer(df_filtered_columns, case=False)
    st.dataframe(filtered_df, use_container_width=True)

    total_days = (df['Date'].max() - df['Date'].min()).days + 1
    total_weeks = total_days // 7


    selected_user_id = filtered_df["User ID"].iloc[0]

    # Bu "User ID"ye sahip kişinin ana veri seti df içerisindeki "Recency" değerini al
    recency_value = df[df["User ID"] == selected_user_id]["Recency"].iloc[0]
    frequency_value = df[df["User ID"] == selected_user_id]["Frequency"].iloc[0]
    segment = df[df["User ID"] == selected_user_id]["Segment"].iloc[0]
    promosyon_value = df[df["User ID"] == selected_user_id]["Promosyon"].iloc[0]
    cluster_value = df[df["User ID"] == selected_user_id]["Cluster"].iloc[0]

    st.markdown(f"<span style='font-size:34px'><u>**{selected_user_id} :id:'li Kişinin</u>**\n\n<span style='font-size:34px'>:balloon:**Önerilen Promosyon:** {promosyon_value}", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:34px'>:date:**Recency Değeri:** {recency_value}", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:34px'>:shopping_trolley:**Frequency Değeri:** {frequency_value}", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:34px'>:sports_medal:**Segmenti :** {segment}", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:34px'>:checkered_flag:**Cluster'ı :** {cluster_value}", unsafe_allow_html=True)

    st.markdown(f"<span style='font-size:34px; color:orange'>**Kampanya Bazlı İnceleme:**</span>", unsafe_allow_html=True)

    from streamlit_extras.dataframe_explorer import dataframe_explorer


    promosyon_list = list(df["Promosyon"].unique())
    selected_promosyon = st.selectbox('Bir promosyon seçin:', promosyon_list)
    filtered_df2 = df[df["Promosyon"] == selected_promosyon]
    st.write(filtered_df2)
    cluster_counts = filtered_df2['Cluster'].value_counts()

    col1, col2 = st.columns((2))
    with col1:

        fig1 = px.bar(cluster_counts, x=cluster_counts.index, y=cluster_counts.values, title='Cluster Sayıları',
                 labels={'x': 'Cluster', 'y': 'Count'})
        fig1.update_layout(
        xaxis=dict(tickvals=list(range(int(cluster_counts.index.min()), int(cluster_counts.index.max()) + 1))))

    col1.plotly_chart(fig1)
    with col2:

        fig2 = px.scatter(filtered_df2, x='Recency', y='Frequency', title='Recency vs Frequency')
        col2.plotly_chart(fig2)

elif page == "Grafikler":
    startDate = pd.to_datetime(df["Date"]).min()
    endDate = pd.to_datetime(df["Date"]).max()

    date1 = pd.to_datetime(st.date_input("Başlangıç Tarihi", startDate))
    date2 = pd.to_datetime(st.date_input("Bitiş Tarihi", endDate))

    df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()

    col1, col2 = st.columns((2))
    with col1:
        segment_sales = df.groupby('Segment')['Sales'].sum()
        fig1 = px.bar(segment_sales, x=segment_sales.index, y=segment_sales.values, title='Segment Bazlı Satışlar')
        st.plotly_chart(fig1)
    with col2:
        daily_saless = df.groupby('Date')['Sales'].sum()
        fig2 = px.line(daily_saless, x=daily_saless.index, y=daily_saless.values, title='Günlük Satışlar')
        st.plotly_chart(fig2)
    col3, col4 = st.columns((2))
    with col3:
        city_sales = df.groupby('City')['Sales'].sum().sort_values(ascending=False)
        fig3 = px.bar(city_sales, x=city_sales.index, y=city_sales.values, title='Şehir Bazlı Satışlar')
        st.plotly_chart(fig3)
    with col4:
        hourly_sales = df.groupby('Saat_Segment')['Sales'].sum()
        fig4 = px.bar(hourly_sales, x=hourly_sales.index, y=hourly_sales.values, title='Saat Segmentine Göre Satışlar')
        st.plotly_chart(fig4)
    col5, col6 = st.columns((2))
    with col5:
        order_of_days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        daily_sales = df.groupby('Day').sum()['Sales'].reindex(order_of_days)
        fig5 = px.bar(daily_sales, x=daily_sales.index, y=daily_sales.values, title='Güne Göre Satışlar')
        st.plotly_chart(fig5)
    with col6:
        cluster_counts = df['Cluster'].value_counts()
        fig7 = px.bar(cluster_counts, x=cluster_counts.index, y=cluster_counts.values,
                      title='Cluster Bazlı Müşteri Sayısı')
        st.plotly_chart(fig7)
    col7, col8 = st.columns((2))
    with col7:
        weekend_sales = df.groupby('Weekend')['Sales'].sum()
        labels = ['Hafta İçi', 'Hafta Sonu'] if 1 in weekend_sales.index else ['Hafta Sonu', 'Hafta İçi']
        fig9 = px.pie(values=weekend_sales.values, names=labels, title='Hafta Sonu vs Hafta İçi Satışları')
        st.plotly_chart(fig9)
    with col8:
        fig8 = px.scatter(df, x='Recency', y='Frequency', title='Recency vs Frequency')
        st.plotly_chart(fig8)











