import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, engine, text
import matplotlib.pyplot as plt
import requests
from streamlit_option_menu import option_menu
import datetime
import altair as alt
from statistics import mean
from PIL import Image 
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth 
import authenticator
import os

# ---------------------------------------------------- AUTH LOGIN ----------------------------------------------------
# Get the current working directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Build the path to your credentials.yaml file
credentials_path = os.path.join(current_directory, 'credentials.yaml')

with open(credentials_path) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error('Username/password is incorrect')

if authentication_status == None:
    st.warning('Please enter your username and password')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'You are logged in as **{username}**')

    # @st.cache_data
    @st.experimental_memo
    def load_data(response_json):
        try:
            data = pd.json_normalize(response_json, "result")
            return data
        except Exception as e:
            print(e)

    # Topbar navigation menu
    selected = option_menu(
        menu_title = None, 
        options = ["Home","Customers", "Articles", "Transactions"],
        icons = ["house","people-fill", "upc-scan", "bag-check-fill"],
        default_index = 0,
        orientation = "horizontal"
    )

    logo = Image.open('logo.png')

    # ---------------------------------------------------- HOME PAGE ----------------------------------------------------
    # If statement to enter the home page.
    if selected == "Home":
        # st.image(logo, width=100)
        st.title(f"Welcome to the {selected} page")
        st.write("""Welcome to my streamlit application for H&M data. 
        In this app you will find a dashboard for each dataframe: Customers, Articles and Transactions.
        If you navigate through the top bar menu, you'll find a dashbord corresponding to every dataframe. 
        In each dashbord, there is a sidebar with filters that you can use to look for every detail and
        adapt the vizualizations to your liking. Hope you like it! ⭐""")

    # ---------------------------------------------------- CUSTOMERS ----------------------------------------------------
    # If statement to enter the customers page.
    if selected == "Customers":
        st.write(f"**Welcome to the {selected} page**")
        st.write("""In this section of the app, you can see the Customers dashboard. There are
        four vizualizations of the data: Number of customers by age, Total amount spent by customers 
        by age, Average amount spent by customers per aga and the Percentage spent by customers per 
        age group. Notice that on the sidebar you can filter through the ages.""")

        # ----------------------------- Creating and adding filter sidebar -----------------------------
        st.sidebar.image(logo, width=100)
        # Add side bar for filters.
        st.sidebar.write("## Filters for the Customers data")

        # Age range filter.
        age_filtered_lst = st.sidebar.slider(
            'Select a range of ages',
            15, 100, (15, 100))
        
        # Create variables for age upper and lower bound.
        age_lb = age_filtered_lst[0]
        age_ub = age_filtered_lst[1]

        # ------------------------- Retrieving data from API endpoint -------------------------
        # Customer by age data.
        response_customers_age = requests.get("https://api-dot-titanium-vim-377008.oa.r.appspot.com/api/customers/ages", headers = {"Authorization": "Bearer 69fyX4eByCpWGHnmztRS"})
        response_json_customers_age = response_customers_age.json()
        customers_data_age = load_data(response_json_customers_age)

        # Amount spent by customers by age.
        response_customers_age_spent = requests.get("https://api-dot-titanium-vim-377008.oa.r.appspot.com/api/customers/ages/spent", headers = {"Authorization": "Bearer 69fyX4eByCpWGHnmztRS"})
        response_json_customers_age_spent = response_customers_age_spent.json()
        customers_data_spent_age = load_data(response_json_customers_age_spent)

        # ---------------------------------- Merging the data ----------------------------------
        # Merging both dataframes retrieved to get the mean spent by age.
        customers_ages_merged = pd.merge(customers_data_age, customers_data_spent_age, on='age')
        customers_ages_merged['avg_spent'] = customers_ages_merged['spent'] / customers_ages_merged['number_customers']
        # st.dataframe(customers_ages_merged)

        # ---------------------------------- Plotting the data ----------------------------------
        st.write('# Customers data visualization')
        # st.dataframe(customers_data_age)

        st.write(f'### Number of customers by age between {age_lb} and {age_ub}')

        customers_ages_filtered = customers_data_age[(customers_data_age['age'] >= age_lb) & (customers_data_age['age'] <= age_ub)]

        # st.dataframe(customers_ages_filtered)
        chart_customers_ages = alt.Chart(customers_ages_filtered).mark_bar(color='#cd071e').encode(
            x=alt.X('age', axis=alt.Axis(title='Age')),
            y=alt.Y('number_customers', axis=alt.Axis(title='Number of customers'))
            )
        st.altair_chart(chart_customers_ages, use_container_width=True)

        # --------------------------------------------------
        st.write(f'### Total amount spent by customers per age between {age_lb} and {age_ub}')
        # st.dataframe(customers_data_spent_age)

        customers_ages_spent_filtered = customers_data_spent_age[(customers_data_spent_age['age'] >= age_lb) & (customers_data_spent_age['age'] <= age_ub)]
        
        chart_customers_spent_ages = alt.Chart(customers_ages_spent_filtered).mark_bar(color='#cd071e').encode(
            x=alt.X('age', axis=alt.Axis(title='Age')),
            y=alt.Y('spent', axis=alt.Axis(title='Amount spent'))
            )
        st.altair_chart(chart_customers_spent_ages, use_container_width=True)

        # --------------------------------------------------
        st.write(f'### Average amount spent by customers per age between {age_lb} and {age_ub}')
        # st.dataframe(customers_ages_merged)

        customers_ages_spent_avg_filtered = customers_ages_merged[(customers_ages_merged['age'] >= age_lb) & (customers_ages_merged['age'] <= age_ub)]
        
        chart_customers_spent_avg_ages = alt.Chart(customers_ages_spent_avg_filtered).mark_bar(color='#cd071e').encode(
            x=alt.X('age', axis=alt.Axis(title='Age')),
            y=alt.Y('avg_spent', axis=alt.Axis(title='Average amount spent'))
            )
        st.altair_chart(chart_customers_spent_avg_ages, use_container_width=True)

        # --------------------------------------------------
        st.write('### Percentage spent by customers per age group')
        st.write('This is an overview of the amount spent by customers depending on their age group.')
        # create a bar chart of age groups and amount spent
        # st.dataframe(customers_data_spent_age)

        bins_df = customers_data_spent_age.loc[:, ['age', 'spent']]

        bins_df['age_groups'] = pd.cut(bins_df['age'], bins=[15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, float('Inf')], labels=['16-20', '20-25', '25-30', '30-35', '35-40','40-45','45-50','50-55', '55-60','60-65', '65-70', '70+'])
        grouped_df = bins_df.groupby('age_groups').agg({'spent': 'sum'}).reset_index()
        grouped_df['percent_spent'] = grouped_df['spent'] / grouped_df['spent'].sum() * 100

        # st.dataframe(grouped_df)

        chart_bins = alt.Chart(grouped_df).mark_bar(color='#cd071e').encode(
            x=alt.X('age_groups', axis=alt.Axis(title='Age group', labelAngle=0)),
            y=alt.Y('percent_spent', axis=alt.Axis(title='% of total spent'))
            )
        st.altair_chart(chart_bins, use_container_width=True)

    # ---------------------------------------------------- ARTICLES ----------------------------------------------------
    # If statement to enter the articles page.
    if selected == "Articles":
        st.write(f"**Welcome to the {selected} page**")
        st.write("""In this section of the app, you can see the Articles dashboard. There are
        four vizualizations of the data: Top articles of total sales by product type, Top articles 
        of total revenue by product type, Top articles present in catalog and Top colors present in 
        catalog. These visualizations are divided in two sections: one section for the data found in
        the catalog (articles dataframe) and an other section for the data created combining the articles
        dataframe and the transactions dataframe. On the sidebar there is also a filter to choose the
        top you want to see.""")

        # ----------------------------- Creating filter sidebar -----------------------------
        # Add side bar for filters
        st.sidebar.image(logo, width=100)
        st.sidebar.write("## Filters for the Articles data")

        # ------------------------- Retrieving data from API endpoint -------------------------
        # Top articles
        response_top_articles = requests.get("https://api-dot-titanium-vim-377008.oa.r.appspot.com/api/articles/top/product", headers = {"Authorization": "Bearer 69fyX4eByCpWGHnmztRS"})
        response_json_top_articles = response_top_articles.json()
        top_articles_data = load_data(response_json_top_articles)
        # st.write('## Top articles')
        # st.dataframe(top_articles_data)

        # Top colors
        response_top_articles_color = requests.get("https://api-dot-titanium-vim-377008.oa.r.appspot.com/api/articles/top/color", headers = {"Authorization": "Bearer 69fyX4eByCpWGHnmztRS"})
        response_json_top_colors = response_top_articles_color.json()
        top_colors_data = load_data(response_json_top_colors)
        # st.write('## Top colors')
        # st.dataframe(top_colors_data)

        # Top articles sold (count)
        response_sales_count = requests.get("https://api-dot-titanium-vim-377008.oa.r.appspot.com/api/articles/sold/count", headers = {"Authorization": "Bearer 69fyX4eByCpWGHnmztRS"})
        response_json_sales_count = response_sales_count.json()
        sales_count = load_data(response_json_sales_count)

        # Top articles sold (sum)
        response_sales_sum = requests.get("https://api-dot-titanium-vim-377008.oa.r.appspot.com/api/articles/sold/revenue", headers = {"Authorization": "Bearer 69fyX4eByCpWGHnmztRS"})
        response_json_sales_sum = response_sales_sum.json()
        sales_sum = load_data(response_json_sales_sum)

        # ---------------------------------- Adding filters ----------------------------------
        top_filter_article = st.sidebar.slider(
        'Select the top you want to see for articles',
        1, len(top_articles_data), (1, 10))
        st.sidebar.write('You have selected this top for articles:', top_filter_article)

        top_filter_color = st.sidebar.slider(
        'Select the top you want to see for colors',
        1, len(top_colors_data), (1, 10))
        st.sidebar.write('You have selected this top for colors:', top_filter_color)

        top_lb = top_filter_article[0]-1
        top_ub = top_filter_article[1]

        top_lb_color = top_filter_color[0]-1
        top_ub_color = top_filter_color[1]

        # ---------------------------------- Plotting the data ----------------------------------
        # Articles merged with transactions to see the top revenue and top products sold to 
        # later compare to the catalog.
        st.write('# Articles data visualization')
        st.write('## Articles sold')
        

        st.write(f'### Top {top_ub} articles of total sales by product type \n*(starting from {top_lb+1})')
        # st.dataframe(sales_count)

        # Chart to display the top articles (top chosen in filter)
        top_articles_sold_filtered = sales_count.iloc[top_lb:top_ub]

        # Create chart using altair
        chart_top_articles_sold = alt.Chart(top_articles_sold_filtered).mark_bar(color='#cd071e').encode(
            x=alt.X('count_products:Q', axis=alt.Axis(title='Number of products sold')),
            y=alt.Y('product_type_name:N', sort='-x', axis=alt.Axis(title='Type of product')),
            tooltip=['product_type_name', 'count_products']
        )
        st.altair_chart(chart_top_articles_sold, use_container_width=True)
        

        st.write(f'### Top {top_ub} articles of total revenue by product type \n*(starting from {top_lb+1})')
        # st.dataframe(sales_sum)

        top_articles_rev_filtered = sales_sum.iloc[top_lb:top_ub]

        # Create chart using altair
        chart_top_articles_rev = alt.Chart(top_articles_rev_filtered).mark_bar(color='#cd071e').encode(
            x=alt.X('revenue:Q', axis=alt.Axis(title='Revenue generated')),
            y=alt.Y('product_type_name:N', sort='-x', axis=alt.Axis(title='Type of product')),
            tooltip=['product_type_name', 'revenue']
        )
        st.altair_chart(chart_top_articles_rev, use_container_width=True)
                
        # --------------------------------------------------------
        st.write('## Articles in catalog')

        # Chart to display the top articles (top chosen in filter)
        top_articles_filtered = top_articles_data.iloc[top_lb:top_ub]

        # Create chart using altair
        chart_top_articles = alt.Chart(top_articles_filtered).mark_bar(color='#cd071e').encode(
            x=alt.X('count:Q', axis=alt.Axis(title='Number of products')),
            y=alt.Y('product_name:N', sort='-x', axis=alt.Axis(title='Type of product')),
            tooltip=['product_name', 'count']
        )
            
        # --------------------------------------------------------
        # Chart to display the top colors (top chosen in filter)
        top_colors_filtered = top_colors_data.iloc[top_lb_color:top_ub_color]

        # Create chart using altair
        chart_top_colors = alt.Chart(top_colors_filtered).mark_bar(color='#cd071e').encode(
            x=alt.X('count:Q', axis=alt.Axis(title='Number of colors')),
            y=alt.Y('color:N', sort='-x', axis=alt.Axis(title='Color')),
            tooltip=['color', 'count']
        )

        st.write(f'### Top {top_ub} articles present in catalog \n*(starting from {top_lb+1})')
        st.altair_chart(chart_top_articles, use_container_width=True)

        st.write(f'### Top {top_ub_color} colors present in catalog \n*(starting from {top_lb_color+1})')
        st.altair_chart(chart_top_colors, use_container_width=True)
        

    # ---------------------------------------------------- TRANSACTIONS ----------------------------------------------------
    # If statement to enter the transactions page.
    if selected == "Transactions":
        st.write(f"**Welcome to the {selected} page**")
        st.write("""In this section of the app, you can see the Transactions dashboard. There are
        three vizualizations of the data (and two metrics): Daily revenue, Average daily price and total
        revenue per month. On the sidebar there is also a filter to choose the the time frame you want 
        to visualize.""")

        # --------------------------- Creating and adding filters ---------------------------
        st.sidebar.image(logo, width=100)
        # Add side bar for filters
        st.sidebar.write("## Filters for the Transactions data")

        # I set the minimum and maximum selectable dates.
        min_date = datetime.date(2018, 9, 20)
        max_date = datetime.date(2020, 9, 22)

        # Create date filter
        start_date = st.sidebar.date_input("Start date", value=min_date, min_value=min_date, max_value=max_date)
        end_date = st.sidebar.date_input("End date", value=max_date, min_value=min_date, max_value=max_date)

        # start_date = st.sidebar.date_input("Start date", value=datetime.date(2018, 9, 20))
        # end_date = st.sidebar.date_input("End date", value=datetime.date(2018, 10, 1))
        # end_date = st.sidebar.date_input("End date", value=datetime.date(2020, 9, 22))

        # ------------------------- Retrieving data from API endpoint -------------------------
        # Sum of price per day and channel id avg request and load data
        response_sum_per_day= requests.get(f"https://api-dot-titanium-vim-377008.oa.r.appspot.com/api/transactions/sum/{start_date}/{end_date}", headers = {"Authorization": "Bearer 69fyX4eByCpWGHnmztRS"})
        response_json_sum_per_day = response_sum_per_day.json()
        transactions_sum_day = load_data(response_json_sum_per_day)
        # st.write("## Total revenue per day (sum price per day)")
        # st.dataframe(transactions_sum_day)

        # Change the column t_dat to be of type datetime
        transactions_sum_day["t_dat"] = pd.to_datetime(transactions_sum_day["t_dat"])


        # Average price per day request and load data
        response_avg_per_day= requests.get(f"https://api-dot-titanium-vim-377008.oa.r.appspot.com/api/transactions/avg/{start_date}/{end_date}", headers = {"Authorization": "Bearer 69fyX4eByCpWGHnmztRS"})
        response_json_avg_per_day = response_avg_per_day.json()
        transactions_avg_day = load_data(response_json_avg_per_day)
        # st.write("## Total average revenue per day (avg price per day)")
        # st.dataframe(transactions_avg_day)

        # Change the column t_dat to be of type datetime
        transactions_avg_day["t_dat"] = pd.to_datetime(transactions_avg_day["t_dat"])

        # ------------------------- Adding sum KPIs -------------------------
        st.write('# Transactions data visualization')
        
        kpi1, kpi2 = st.columns(2)

        # Total revenue in time frame selected.
        total_revenue = sum(transactions_sum_day['price'])
        # st.write(sum(transactions_sum_day['price']))

        # Average price in time frame selected.
        total_avg_price = mean(transactions_avg_day['price'])
        # st.write(mean(transactions_avg_day['price']))

        kpi1.metric(
            label = "Total revenue in selected time frame",
            value = round(total_revenue,2),
            # delta = round(total_revenue,2),
        )

        kpi2.metric(
            label = "Total average of price in selected time frame",
            value = round(total_avg_price,4),
            # delta = round(total_avg_price,4),
        )

        # ------------------------- Plotting the data -------------------------
        # Daily revenue per day bar plot (selected time frame)
        st.write(f'### Daily revenue (sum price per day) \n*from {start_date} to {end_date}')
        chart_sum_price_day = alt.Chart(transactions_sum_day).mark_bar(color='#cd071e').encode(
            x=alt.X('t_dat', axis=alt.Axis(title='Date')),
            y=alt.Y('price', axis=alt.Axis(title='Daily revenue'))
            )
        st.altair_chart(chart_sum_price_day, use_container_width=True)


        # Average daily price per day (selected time frame)
        st.write(f'### Average daily price per day \n*from {start_date} to {end_date}')
        chart_avg_price_day = alt.Chart(transactions_avg_day).mark_bar(color='#cd071e').encode(
        x=alt.X('t_dat', axis=alt.Axis(title='Date')),
        y=alt.Y('price', axis=alt.Axis(title='Average daily revenue'))
        )
        st.altair_chart(chart_avg_price_day, use_container_width=True)

        # Total monthly revenue 
        df_monthly = transactions_sum_day.groupby(pd.Grouper(key='t_dat', freq='M')).agg(
            {'price': 'sum', 'percentage_online': 'mean', 'percentage_offline': 'mean'})
        
        # reset index to get a column for the month
        df_monthly = df_monthly.reset_index()

        # I rename the t_dat column to month
        df_monthly = df_monthly.rename(columns={'t_dat': 'month'})
        # st.write('## MONTHLY')
        # st.dataframe(df_monthly)

        # I compute the online and offline revenue for each month
        df_monthly['revenue_online'] = df_monthly['price'] * df_monthly['percentage_online']
        df_monthly['revenue_offline'] = df_monthly['price'] * df_monthly['percentage_offline']

        # Then, melt the dataframe to have a 'revenue_type' column and a 'revenue' column
        df_melted = pd.melt(df_monthly, id_vars=['month'], value_vars=['revenue_online', 'revenue_offline'],
                            var_name='revenue_type', value_name='revenue')

        st.write('### Total revenue per month (sum price per month) \n*in time frame selected')

        chart_sum_month = alt.Chart(df_melted).mark_bar().encode(
            x=alt.X('month', axis=alt.Axis(title='Date')),
            y=alt.Y('revenue', axis=alt.Axis(title='Monthly revenue')),
            color=alt.Color('revenue_type', scale=alt.Scale(domain=['revenue_online', 'revenue_offline'],
                                                            range=['#cd071e', 'blue'])))
        st.altair_chart(chart_sum_month, use_container_width=True)