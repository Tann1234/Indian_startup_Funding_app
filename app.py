import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout='wide', page_title='StartUp Aanalysis')

df=pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'], errors='coerce')
df['year']=df['date'].dt.year
df['month']=df['date'].dt.month

def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df=df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investors')
    st.dataframe(last5_df)

    col1, col2=st.columns(2)
    with col1:
    # Biggest investments
        big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax=plt.subplots()
        ax.bar(big_series.index, big_series.values)

        st.pyplot(fig)

    with col2:
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sector wise Investments')
        fig1, ax1=plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct='%1.1f%%')

        st.pyplot(fig1)

    col1, col2=st.columns(2)
    with col1:
        # Stage pie
        stage_series=df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Stage Investments')
        fig2, ax2=plt.subplots()
        ax2.pie(stage_series, labels=stage_series.index, autopct='%1.1f%%')

        st.pyplot(fig2)

    with col2:
        # Stage pie
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('City Investments')
        fig3, ax3= plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct='%1.1f%%')

        st.pyplot(fig3)


    #YOY Investment
        year_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('YoY Investment')
        fig4, ax4 = plt.subplots()
        ax4.plot(year_series.index, year_series.values)

        st.pyplot(fig4)

    # Similar Investors
    investor_df = temp_df=df[df['investors'].str.contains(investor)].iloc[0]
    st.subheader('Similar Investors based on Industry')
    inv_df = df[df['vertical'] == investor_df['vertical']]
    st.dataframe(inv_df)

def company_details(startup):
    st.title(startup)

    col3, col4=st.columns(2)
    with col3:
        # Founder
        founder_df=df[df['startup']==startup]['investors'].iloc[0]
        st.subheader('investor details')
        st.write(founder_df)
    with col4:
        # Industry
        industry_df = df[df['startup'] == startup]['vertical'].iloc[0]
        st.subheader('Industry')
        st.write(industry_df)
    col5, col6=st.columns(2)
    with col5:
        # Sub Industry
        subindustry_df = df[df['startup'] == startup]['subvertical'].iloc[0]
        st.subheader('Sub Industry')
        st.write(subindustry_df)

    with col6:
        # Location
        Location_df= df[df['startup'] == startup]['city'].iloc[0]
        st.subheader('Location')
        st.write(Location_df)

    # Founding Rounds
    funding_series = df[df['startup']== startup].groupby(['round', 'investors', 'date', 'city'])['amount'].sum().reset_index().sort_values(by='date', ascending=False)
    st.header('Funding Rounds')
    st.dataframe(funding_series)

    # Similar company
    temp_df=df[df['startup'] == startup].iloc[0]
    st.subheader('Similar Companies based on Industry or location wise')
    sim_df=df[df['vertical']==temp_df['vertical']]

    st.dataframe(sim_df)
def load_overall_analysis():
    st.title('Overall Analysis')

    col1, col2, col3, col4=st.columns(4)
    with col1:
        # total invested amount
        total=round(df['amount'].sum())
        st.metric('Total', str(total) + ' Cr.')

    with col2:
        # max amount infused in a startup
        max_finding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

        st.metric('max_finding', str(max_finding) + ' Cr.')

    # avg ticket size

    with col3:
        avg_finding = df.groupby('startup')['amount'].sum().mean()

        st.metric('avg_finding', str(round(avg_finding)) + ' Cr.')

    # total funded startups
    with col4:
        num_startups=df['startup'].nunique()
        st.metric('Funded Startups', str(num_startups) )

    st.header('MoM grap')
    selected_option=st.selectbox('Select Type', ['Total' , 'Count'])
    if selected_option=='Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig6, ax6 = plt.subplots()
    ax6.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig6)

    # Sector Analysis Pie
    st.header('Sector Analysis Pie')
    selected_box = st.selectbox('Select Type', ['Count', 'Sum'])
    if selected_box == 'Sum':
        df['vertical']=df['vertical'].replace({'ECommerce': 'E-Commerce', 'eCommerce': 'E-Commerce', 'E-commerce' : 'E-Commerce'})
        sector_df=df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
        fig7, ax7 = plt.subplots()
        ax7.pie(sector_df, labels=sector_df.index, autopct='%1.1f%%')
        st.pyplot(fig7)
    else:
        df['vertical']=df['vertical'].replace({'ECommerce': 'E-Commerce', 'eCommerce': 'E-Commerce', 'E-commerce' : 'E-Commerce'})
        count_df=df.groupby('vertical')['amount'].count().sort_values(ascending=False).head(10)
        fig8, ax8= plt.subplots()
        ax8.pie(count_df, labels=count_df.index, autopct='%1.1f%%')
        # ax1.pie(vertical_series, labels=vertical_series.index, autopct='%1.1f%%')
        st.pyplot(fig8)

    # Type of funding
    funding=df['round'].value_counts(ascending=False)
    st.subheader('Funding Rounds')
    st.dataframe(funding)

    # city wise funding
    city_wise=df.groupby('city')['amount'].count().sort_values(ascending=False).head(10)
    st.subheader('City Wise Funding')
    fig9, ax9 = plt.subplots()
    ax9.bar(city_wise.index ,city_wise.values)
    st.pyplot(fig9)

    #Top startups ->year wise -> overall
    yearly_funding = df.groupby(['year', 'startup'])['amount'].sum().reset_index()
    top_startups_per_year=yearly_funding.loc[yearly_funding.groupby('year')['amount'].idxmax()].sort_values('year')
    st.subheader('Top Startups')
    st.dataframe(top_startups_per_year)

    # Top Investors
    investor_df=df.groupby('investors')['amount'].count().sort_values(ascending=False).head(10)
    st.subheader('Top Investors')
    fig10, ax10 = plt.subplots()
    ax10.bar(investor_df.index, investor_df.values)
    st.pyplot(fig10)

    # funding heatmap
    pivot_city = df.pivot_table(values='amount',
                                index='city',
                                columns='year',
                                aggfunc='sum').fillna(0)

    fig2 = px.imshow(pivot_city.head(15),  # show top 15 cities
                     labels=dict(x="Year", y="City", color="Funding (₹)"),
                     title="🏙️ City-wise Funding Heatmap",
                     aspect="auto",
                     color_continuous_scale="Blues")

    st.plotly_chart(fig2, use_container_width=True)

st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option=='Overall Analysis':
        load_overall_analysis()


elif option=='Startup':
    st.title('StartUp Analysis')
    selected_startup=st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        company_details(selected_startup)
else:
    st.title('Investor Analysis')
    selected_investor=st.sidebar.selectbox('Select Investors', sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investors Details')
    if btn2:
       load_investor_details(selected_investor)
