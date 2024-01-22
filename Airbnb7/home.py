import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

def plot_rating(df,hover_data,x):
    fig = px.scatter_mapbox(df, 
                            lat='latitude1', 
                            lon='longitude1', 
                            color=x,
                            color_continuous_scale="Viridis",
                            range_color=(20, 100),
                            mapbox_style="carto-positron",
                            opacity=1, 
                            hover_data=hover_data,
                            labels={'name1':'Name','host_name1':'Host Name','price1':'Price','rating1':'Rating'},
                            center={"lat": -2, "lon": 45},
                            zoom=0)


    st.plotly_chart(fig)

def metrics_plot(df):
    num=df['rating1'].mean()
    df['rating1']=df['rating1'].fillna(num)
    df_max1=df['rating1'].max()
    df_min1=df['rating1'].min()
    df_max=pd.read_sql("select name1 from airbnb3 where rating1=%s" %(df_max1),conn)
    df_min=pd.read_sql("select name1 from airbnb3 where rating1=%s" %(df_min1),conn)
    df_not_count=pd.read_sql("select count(name1) from airbnb3 where rating1!=%s and rating1!=%s" %(df_max1,df_min1),conn)
    df_max_count=pd.read_sql("select name1 from airbnb3 where rating1>%s" %(num),conn)
    df_min_count=pd.read_sql("select name1 from airbnb3 where rating1<=%s" %(num),conn)
    df_max_count1=df_max_count['name1'].count()
    df_min_count1=df_min_count['name1'].count()
    col1,col2,col3=st.columns(3)
    col1.metric("Average Rating",num)
    fig1,ax=plt.subplots()
    ax.pie([df_max_count1,df_min_count1],labels=['>average','<=average'],autopct='%1.1f%%')
    col2.pyplot(fig1)
    col3.metric("Count of places",len(df))
    col4,col5,col6=st.columns(3)
    col4.metric("Maximum Rating",df['rating1'].max())
    max_list=col5.selectbox("Places withMaximum Rating",df_max['name1'].values)
    list=pd.read_sql("select * from airbnb3 where name1='%s'" %(max_list),conn)
    st.dataframe(list)
    col6.metric("Count of places with Maximum Rating",len(df_max))
    #col5.metric("Place with Maximum Rating",df_max['name1'].values[0])
    col7,col8,col9=st.columns(3)
    col7.metric("Minimum Rating",df['rating1'].min())
    col8.selectbox("Places withMinimum Rating",df_min['name1'].values)
    col9.metric("Count of places with Minimum Rating",len(df_min))

def price_plot(df):
    num=df['price'].mean()
    df['price']=df['price'].fillna(num)
    df_max1=df['price'].max()
    df_min1=df['price'].min()
    average=df['price'].mean()
    df_max=pd.read_sql("select name1 from airbnb3 where price=%s" %(df_max1),conn)
    df_min=pd.read_sql("select name1 from airbnb3 where price=%s" %(df_min1),conn)
    df_not_count=pd.read_sql("select count(name1) from airbnb3 where price=%s and price!=%s" %(df_max1,df_min1),conn)
    df_max_count=pd.read_sql("select name1 from airbnb3 where price>%s" %(average),conn)
    df_min_count=pd.read_sql("select name1 from airbnb3 where price<=%s" %(average),conn)
    df_max_count1=df_max_count['name1'].count()
    df_min_count1=df_min_count['name1'].count()
    col1,col2,col3=st.columns(3)
    col1.metric("Average Price",df['price'].mean())
    fig1,ax=plt.subplots()
    ax.pie([df_max_count1,df_min_count1],labels=['>average','<=average'],autopct='%1.1f%%')
    col2.pyplot(fig1)
    col3.metric("Count of places",len(df))
    col4,col5,col6=st.columns(3)
    col4.metric("Maximum Price",df['price'].max())
    
    max_list=col5.selectbox("Maximum Price",df_max['name1'].values)
    list=pd.read_sql("select * from airbnb3 where name1='%s'" %(max_list),conn)
    st.dataframe(list)
    col6.metric("Count of places with Maximum Price",len(df_max))
    #col5.metric("Place with Maximum Rating",df_max['name1'].values[0])
    col7,col8,col9=st.columns(3)
    col7.metric("Minimum Price",df['price'].min())
    min_list=col8.selectbox("Minimum Price",df_min['name1'].values)
    list=pd.read_sql("select * from airbnb3 where name1='%s'" %(min_list),conn)
    st.dataframe(list)
    col9.metric("Count of places with Minimum Price",len(df_min))

def overall_report():
    country_count=pd.read_sql("select count(*) as cou,country1,avg(price) as pri,avg(rating1) as rat from airbnb3 group by country1",conn)
    st.write("Country count")
    st.bar_chart(country_count,x="country1",y="cou")
    st.write("Average rating")
    st.bar_chart(country_count,x="country1",y="rat")
    st.write("Average price")
    st.bar_chart(country_count,x="country1",y="pri")

def country_wise():
    cont=pd.read_sql("select country1 as cnt,avg(rating1) as rat from airbnb3 group by country1",conn)
    cntry=st.sidebar.selectbox("Select a country",cont['cnt'].values)
    choice2=st.sidebar.selectbox("Select a choice",["Price","Rating","Amenities","Reviews"])
    if choice2=="Price":
        price2=pd.read_sql("select * from airbnb3 where country1='%s' order by price asc" %(cntry),conn)
        st.dataframe(price2)
    elif choice2=="Rating":
        rating2=pd.read_sql("select * from airbnb3 where country1='%s' order by rating1 desc" %(cntry),conn)
        st.dataframe(rating2)
    elif choice2=="Amenities":
        amnet=pd.read_sql("select distinct name1 from amenities3",conn)
        amnty=st.sidebar.selectbox("Choose an amenity",amnet['name1'].values)
        amenities2=pd.read_sql("select airbnb3.id1,airbnb3.name1,amenities3.name1 as amenity,description1,host_id1,host_name1,price,rating1,location1,city1,state1,country1 from airbnb3,amenities3 where airbnb3.id1=amenities3.id1 and country1='%s' and amenities3.name1='%s'" %(cntry,amnty),conn)
        st.dataframe(amenities2)
    elif choice2=="Reviews":
        txt=st.sidebar.text_input("Enter the location id",value="10006546")
        rev=pd.read_sql("Select reviews3.id1,name1,reviewer_id1,reviewer_name1,comment1,description1,host_id1,host_name1,price,rating1 from reviews3,airbnb3 where reviews3.id1=airbnb3.id1 and airbnb3.id1=%s" %(txt),conn)
        retrieve=st.sidebar.button("Retrieve reviews")
        if retrieve:
            st.dataframe(rev)
    #price2=pd.read_sql("")
conn=create_engine("mysql+mysqlconnector://root:mypass@localhost:3306/airbnb17")
df=pd.read_sql("select latitude1,longitude1,rating1,name1,host_name1,price from airbnb3",conn)

df_amenities=pd.read_sql("select amenities3.name1 as amenity,airbnb3.name1 from amenities3,airbnb3 where amenities3.id1=airbnb3.id1",conn)
df_reviews=pd.read_sql("select name1,reviewer_name1,reviewer_id1,comment1 from reviews3,airbnb3 where airbnb3.id1=reviews3.id1",conn)
df1=pd.read_sql("select * from airbnb3",conn)

#st.write(df_not_count['name1,df_max_count['count(name1)'],df_min_count['count(name1)'])
choice=st.sidebar.selectbox("Select",["Home","Plot Rating","Plot Price","View Details","Overall Report","Country Wise Report"])
if choice=="Home":
    st.title("Airbnb Dashboard")
    st.write("Welcome to Airbnb dashboard")
elif choice=="Plot Rating":
    metrics_plot(df)
    #col8.metric("Place with Minimum Rating",df_min['name1'].values)
    hover_data=['name1','host_name1','price','rating1']
    x='rating1'
    plot_rating(df,hover_data,x)
elif choice=="Plot Price":
    price_plot(df)
    hover_data=['name1','host_name1','price','rating1']
    x='price'
    plot_rating(df,hover_data,x)
elif choice=="View Details":
    st.write("Location Details")
    st.dataframe(df1)
    st.write("Amenities Details")
    st.dataframe(df_amenities)
    st.write("Reviews Details")
    st.dataframe(df_reviews)
elif choice=="Overall Report":
    overall_report()
elif choice=="Country Wise Report":
    country_wise()