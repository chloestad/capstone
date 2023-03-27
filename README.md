# Capstone Project

> Capstone Project - Final Assignment Documentation
STAD Chloé
MCSBT
> 

**Project Links:**

⭐  [Application Link](https://frontend-dot-titanium-vim-377008.oa.r.appspot.com/)

📌  [API Documentation](https://api-dot-titanium-vim-377008.oa.r.appspot.com/)

# 1. Introduction

## 1.1. Purpose of documentation

This documentation aims to provide a comprehensive guide for users and developers to understand and utilize the H&M Data Dashboard application. It covers the application's architecture, user interface, navigation and dashboard components.

## 1.2. Overview of the application

The H&M Dashboard is a Streamlit-based web application designed to visualize and analyze data from H&M's customers, articles, and transactions. The application leverages Google Cloud storage to host the dataframes and uses optimized data processing techniques like group bys and merging to reduce loading time and have a better user experience. It retrieves data via API endpoints, secured through a token-based authentication system.

After the user loads the page for the first time, they are welcomed with a login page. If the user logs in successfully it will have access the home page, which contains a brief description of the dashboard's purpose. On top of the web page, the user can see a button to log out, the username that is currently connected and a navigation bar that allows users to navigate between the home page, customers dashboard, articles dashboard, and transactions dashboard. Each dashboard provides key metrics and visualizations tailored to the respective data types along with filters to further investigate the data.

# 2. Application Architecture

## 2.1. Overview of the architecture

The H&M Data Dashboard architecture has three main components: Google cloud database for the data hosting, API endpoints for the data retrieval and the streamlit-based application for the frontend visualization.

## 2.2. Google Cloud storage

The application uses three main types of data from the H&M database: customers, articles, and transactions. These dataframes are hosted on my personal Google Cloud account, ensuring secure storage and efficient access. 

### 2.2.1. Data optimization with group bys and merging

Since the three main dataframes from the H&M database have a lot of entries, loading the data in my application would take a lot of time, resulting in poor user experience. Therefore, to optimize loading time and improve application performance, I created new dataframes from different group bys and merging multiple dataframes. This results in smaller dataframes that are easier to load, providing a seamless user experience.

## 2.3. APIs for data retrieval

The application uses APIs that I previously created to access and retrieve data from the hosted dataframes on Google Cloud. These APIs act as an intermediary between the data storage and the front-end, ensuring secure and efficient communication.

### 2.3.1. API endpoints

The APIs are divided in three parts: Customers, Articles and Transactions. Inside each namespace, you will find the different endpoints to retrieve the corresponding data. The endpoints are:

- **Customers:**
    - `/customers`: It returns the entire customers table. This endpoint is not used in the app since it returns a big dataframe that takes too long to load.
    - `/customers/ages`: it returns a table that is a group by of customers by age. It has the number of customers by age.
    - `/customers/ages/spent`: It returns a table thet is is a group by of customers by age. It has the total amount spent by customers by age. It comes from a merge with the transactions table.
    - `/customers/string:id`: It returns the data of a specific customers by customer_id.
- ******************Articles:******************
    - `/articles`: It returns the entire articles table. This endpoint is not used in the app since it returns a big dataframe that takes too long to load.
    - `/articles/top/product`: It returns the data from the table product_count. This table is the result of a group by product type name. It has the number of products by product_type_name.
    - `/articles/top/color`: It returns the data from the table color_count. This table is the result of a group by color. It has the number of products by color.
    - `/articles/sold/count`: It returns the data from the table product_name_sales_count. This table is the result of a group by color. It has the number of products by color.
    - `/articles/sold/revenue`: It returns the data from the table product_name_sales_sum. This table comes from a merge with transactions. It is a group by product name that sums price for each transaction by product.
    - `/articles/string:id`: It returns the data of a specific article by aticle_id.
- **************************Transactions:**************************
    - `/transactions`:  It returns the entire transactions table. This endpoint is not used in the app since it returns a big dataframe that takes too long to load.
    - `/transactions/sum/string:start_date/string:end_date`: It returns  the sum of transactions by day (revenue). It comes from a group by date and sums price for each day. The endpoint also has two parameters: start_date and end_date to get the data between the start end end date.
    - `/transactions/avg/string:start_date/string:end_date`: It returns  the average of transactions by day (revenue). It comes from a group by date and average price for each day. The endpoint also has two parameters: start_date and end_date to get the data between the start end end date.

### 2.3.2. Authentication and token usage

In order to have access to the data, the APIs implement a token-based authentication system. The user must provide a valid token when making API calls to access the data. This token is: `69fyX4eByCpWGHnmztRS`. Without a valid token, the user cannot access the data.

# 3. User Authentication and Navigation bar

## 3.1. Authentication and Login process

The H&M Data Dashboard application requires users to log in before accessing the dashboard features. Upon visiting the application, users are presented with a login screen, where they must enter their credentials. Once authenticated, the user can access the dashboard page. Furthermore, after the user has accessed, the session will expire in thirty days. This means that the account will be logged in for thirty days, unless the user logs out. The only users that currently have access are:

| Name of User | Username | Password |
| --- | --- | --- |
| Chloé Stad | chloestad | capstone |
| Pepe García | pepegarcia | pepepw |
| Gustavo Martín | gustavomartin | gustavopw |

If the user that is trying to log in is not in the list of authorized users, then the page won't let them log in, and therefore access the dashboard.

To give access to these users, I used the file `credentials.py` and hashed the passwords. 

## 3.2. Navigation Bar

Once the user has logged in, they are welcomed by the home page. On the home page, the user will find a brief introduction to the dashboard. 

On top of the web page, the user can find the log out button and a message that shows the username that is currently logged in. Under this, the user can explore the navigation bar. It consists of four main options: **Home** (home page), **Customers** (customers dashboard), **Articles** (articles dashboard), and **Transactions** (transactions dashboard).

# 4. Customers Dashboard

## 4.1. Customers data visualization

The Customers Dashboard is designed to provide insights into H&M's customer data. It offers various visualizations and key metrics related to customer demographics and purchases. The visualizations you can find are:

- ****Number of customers by age****: This visualization shows a bar plot of the total amount of customers by age.
- ****Total amount spent by customers per age****: This visualization shows a bar plot of the total amount spent by customers per age.
- ****Average amount spent by customers per age****: This visualization shows a bar plot of the average amount of spent by customers per.
- ****Percentage spent by customers per age group****: This visualization shows a bar plot of the percentage spent by customers per age group. The age groups start at 16 years old and every bin of age group is for five years, ending at 70 years old and older since there aren't many customers over the age of 70.

## 4.2. Filters

The customers dashboard has a filter for age range. This is so that the user that wants to visualize a specific age range, they can do so by choosing the exact age one they want to see. The default age range is from 15 years old to 100 years old, but if the user want's to see the distribution of a desired age range, they can do it with this filter. Notice that this filter is for the first three plots, since the last one (percentage spent by customers per age group) is static. When the user changes the age range, this will also be reflected on the title of the plots.

# 5. Articles Dashboard

## 5.1. Articles data visualization

The Articles Dashboard is designed to provide insights into H&M's articles data. It offers various visualizations and key metrics related to articles sold and the articles in catalog.

### 5.1.1. Articles sold

Inside the articles sold visualizations, the user can find two plots:

- ****Top articles of total sales by product type****: This visualization shows a horizontal bar plot of the top articles sold. This means that you can see the total amount of articles sold by product type name.
- ****Top articles of total revenue by product type****: This visualization shows a horizontal bar plot of the top revenue from articles sold. This means that you can see the total revenue of articles sold by product type name.

The difference between these two plots is that the first one shows us the number of product sold, while the second one the total revenue. 

These visualizations where made from retrieving data of a dataframe that comes from a merging the articles dataframe and transactions dataframe, followed by a group by product type name.

### 5.5.2. Articles in catalog

Inside the articles in catalog, the user can find two plots:

- ****Top articles present in catalog****: This visualization shows a horizontal bar plot of the top articles that are present in the catalog. This means that you can see the total amount of articles present in the catalog.
- ****Top colors present in catalog****: This visualization shows a horizontal bar plot of the top colors that are present in the catalog. This means that you can see the total amount of articles that have a specific color present in the catalog.

The top articles present n catalog plot, is useful to compare with the top articles of total sales. This is because we can see if they look similar, since the company would want to have more products of the most popular product sold.  

## 5.2. Filters

The articles dashboard has a filter for top articles and top colors. These filters are set by default for top 10. This means that when the user loads the articles dashboard for the first time, they will see the top 10, but this can be modified. The user can not only modify to see more than 10 product at a time, but they can also modify it to see the top 10 less present articles in catalog or sold, for example. Notice that when the user changes the top range, this will also be reflected on the title of the plots.

# 6. Transactions Dashboard

## 6.1. Transactions data visualization

The Transactions Dashboard is designed to provide insights into H&M's transaction data. It offers various visualizations and key metrics related to transactions revenue and type of sales channel. The visualizations and metrics that you can find are:

- **Total revenue**: This metric shows the total revenue from transactions. This metric comes from the sum of price.
- **Total average of price**: This metric shows the average revenue from transactions. This metric comes from the average of price.
- ****Daily revenue****: This visualizations shows a bar plot for the daily revenue that comes from the sum of price per day.
- ****Average daily price****: This visualizations shows a bar plot for the average daily revenue that comes from the average of price per day.
- ****Total revenue per month****: This visualizations shows a bar plot for the monthly revenue that comes from the sum of price per month. This plot also shows us the proportion of the sales that were made online and offline.

## 6.2. Filters

The transactions dashboard has a filter for the time frame of the visualizations. This is so that the user that wants to visualize some specific dates, they can do so by modifying the time frame. The default time frame is set to the first and last day that we have data from, and the user cannot choose a timeframe outside of the dates that we have data. Notice that when the user changes the time frame, this will also be reflected on the title of the plots.

# 7. Appendix

The files used are:

- api (folder)
    - app.yaml
    - main.py
    - requirements.txt
- frontend (folder)
    - app.yaml
    - main.py
    - logo.png
    - credentials.yaml
    - requirements.txt
- README.md
- hashed_password.py
