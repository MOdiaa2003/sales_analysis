#!/usr/bin/env python
# coding: utf-8

# # Sales_ Analysis_Project

# ### load important libraries

# In[1]:


import pandas as pd
import os 
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# In[2]:


#all_sales.to_csv('F:\\my protofolio\\pandas_projects\\meduim_projects\\sales_analysis\\all_sales.csv', index=False)


# ### task #1: merging 12 months dataset into one file

# In[3]:


#create list of months names to use it when connecting all months together in the same df
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]
# Create an empty list to store DataFrames for each month
monthly_dfs = []
#define the base directory
base_dir='C:/Users/midoo/'

# Loop through each month
for month in months:
    # Generate file path for each month
    file_path = f'{base_dir}Sales_{month}_2019.csv'  # Assuming file names are like '‪C:/Users/midoo/Sales_January_2019.csv'
    
    # Read the CSV file for the current month into a DataFrame
    df = pd.read_csv(file_path)
    
    # Add the DataFrame to the list
    monthly_dfs.append(df)

# Concatenate all DataFrames vertically
all_sales = pd.concat(monthly_dfs)

# Display the combined DataFrame
all_sales.head()


# ### another approach for first_task

# In[4]:


#load all csv's names in list by using  list comprehension 
files=[file for file in os.listdir('C:/Users/midoo/Sales_Data')]
#empty dataframe to store all months sales
all_months_data=pd.DataFrame()
#iterating over every file in list,convert it into csv
#every month concat it with previous months
for file in files:
    df=pd.read_csv(file)
    all_months_data=pd.concat([all_months_data,df])
    

all_months_data.to_csv("all_data.csv",index=False)


# #### updated_dataframe

# In[5]:


all_data=pd.read_csv('C:/Users/midoo/all_data.csv')
all_data.head()


# #### cleaning_before_answer questions

# In[6]:


#remove any Nan values 
all_data=all_data.dropna()
#remove any non numeric values 
all_data=all_data[all_data['Order Date']!='Order Date']
all_data


# #### Adding_column_for_month#

# In[7]:


#split every value in Order Date column before '/' and get the first string from generated list which is # of the month
all_data['month']=all_data['Order Date'].str.split('/').str[0]
#convert the price and Quantity from  string to int so i can use it in calculations
all_data['Quantity Ordered']=all_data['Quantity Ordered'].astype(int)
all_data['Price Each']=all_data['Price Each'].astype(float)
all_data['month']=all_data['month'].astype('int32')
all_data


# ### Question #1: What was the best month for sales? how much was earned this month?

# In[8]:


#add new column to get total price of each order
all_data['total_amount']=all_data['Quantity Ordered']*all_data['Price Each']
#group the data by month then get the sum of total prices and get max 
res=all_data.groupby('month')['total_amount'].sum().reset_index()
res


# #### visualizing the result

# In[9]:



plt.bar(res['month'],res['total_amount'])
plt.xlabel('Month')  # Label for the x-axis
plt.ylabel('Total amount')  # Label for the y-axis
plt.title('Total Sales by Month')  # Title for the plot
plt.xticks(res['month'],size=15)
plt.yticks(size=15)
# Define a function to format y-axis labels
def format_func(value, tick_number):
    return f'{value/1000000:.1f}M'  # Convert values to millions and add "M"

plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_func))

plt.show()


# In[10]:


##we can see that the sales in 12 is very high compared to other months that because New Year's Holiday 
##all people exchange gifts with each other 
## in months of jan,feb,mar isn't so well bec the segmentation of student is still studying 


# #### Adding City column

# In[11]:


#split every value in Purchase Address column before ',' and get the second string from generated list which is city name
#all_data['city']=all_data['Purchase Address'].str.split(',').str[1]
#another appraoch 
#define func to get the string after the first comma and the state
def bring_city( Address):
    return  Address.split(',')[1]
def bring_state( Address):
    return  Address.split(',')[2].split(' ')[1]

# using apply function to perform any function by appply it in Purchase Address iterating over every element 
#in column by lambda and bring the city name and the state name
all_data['city']=all_data['Purchase Address'].apply(lambda x: bring_city(x)+' '+bring_state(x))
all_data


# ### Question #2: What city sold the most product?

# In[12]:


#group the rows by city and state name then get sum of sales by city and state name and order them from descending prespective 
res1=all_data.groupby('city')['total_amount'].sum().reset_index(name='total_amount')


# #### visualizing the result and give explinations

# In[13]:



plt.bar(res1['city'],res1['total_amount'])
plt.xlabel('city')  # Label for the x-axis
plt.ylabel('sales in milions ($)')  # Label for the y-axis
plt.title('highest soldest city')  # Title for the plot
plt.xticks(res1['city'],rotation='vertical',size=12)
plt.yticks(size=15)
plt.show()


# In[14]:


##as we see san francisco is highest sold city because it has highest paid salaries in us on the other hand
## portland is lowest sold city because it has lowest salaries in us
#San Francisco's tech-oriented population and strong presence of technology companies likely drive higher sales for tech-related products
#while Portland's market may be less focused on these types of goods.


# ### Question #3: What time should we display advertisements to maximize the likelihood of purchases?

# #### add new column which own # of hour 

# In[15]:


##convert order date into datetime format to easily manipulate into hour 
all_data['Order Date']=pd.to_datetime(all_data['Order Date'])
##adding new column called hour and having num of hour 
all_data['hour']=all_data['Order Date'].dt.hour
#group element by num of hour then get # of orders in every hour 
res2=all_data.groupby('hour')['Order ID'].count().reset_index(name='# of orders')
res2


# #### visualizing the result and give explinations

# In[16]:




plt.plot(res2['hour'],res2['# of orders'],linestyle='-')
plt.xticks(res2['hour'],rotation='vertical',size=12)
plt.xlabel('hour')
plt.ylabel('num_product_sold')
plt.title('num_product_sold by hour')
plt.yticks(size=12)
plt.grid()
plt.show()


# In[17]:


##At 11 AM, many people are typically settled into their workday, taking breaks or making purchases during lunchtime.
#At 7 PM, after finishing work or school, individuals often engage in leisure activities, including shopping or running errands before dinner.
#so i reccomend around 11 am and 7 pm 


# In[18]:


all_data['Product'].value_counts()


# ### Question #4: What products are most often sold together? 

# In[19]:


#we must get all the same order id without any uniquely id's to get the products sold together
m=all_data[all_data['Order ID'].duplicated(keep=False)]
#Merging repetead order id's and filter from them the repeated products
two_product=pd.merge(m,m,on='Order ID',how='inner').query('Product_x!=Product_y')
#combine the two products in one column
two_product['products']=list(zip(two_product['Product_x'], two_product['Product_y']))
##keep only unique order id with two products purchased
two_product=two_product[two_product['Order ID'].duplicated(keep='first')][['Order ID','products']]
#split two products of one column into two columns every one with one product
two_product[['prod_1', 'prod_2']] = two_product['products'].apply(pd.Series)

two_product.head(10)


# In[29]:


#group the two products and counts the occurance of this two products together 
two_prods_occurance=two_product.groupby(['prod_1','prod_2']).size().sort_values(ascending=False).reset_index(name='occ')
two_prods_occurance.head(10)


# In[45]:


import matplotlib.pyplot as plt
import seaborn as sns

# Get top 10 pairs of products and their occurrences
top_10_pairs = two_prods_occurance.head(10)

# Plotting
plt.figure(figsize=(10, 6))
sns.barplot(x='prod_1', y='occ', data=top_10_pairs, hue='prod_2', palette='viridis')

# Rotate x-axis labels to vertical orientation
plt.xticks(rotation=90)

# Add labels and title
plt.xlabel('Product 1', fontsize=14)
plt.ylabel('Number of Occurrences', fontsize=14)
plt.title('Top 10 Product Pairs by Occurrences', fontsize=16)

# Show plot
plt.show()


# #### my_observations and suggestions

# In[21]:


#so we have observation that products are most often sold together are phones with Headphones and charging cables
#from examples of that [[Lightning Charging Cable,iPhone]:1006,[USB-C Charging Cable,Google Phone]:987,[Wired Headphones,iPhone]:449]
#so we can make several suggestions to increase sales:
#Bundle Deals: Offer bundle deals or package discounts for the frequently co-purchased products.
#This strategy encourages customers to buy both products together, increasing the overall sales value while providing perceived value to the customers
#Cross-Selling: Implement cross-selling strategies by recommending complementary products during the checkout process or on product pages.
#For example, if customers are buying a camera, suggest related accessories like memory cards, tripods, or camera cases.
#if you have two related products you must have the same # in the inventory because it is likely to sold together


# ### Question #5: What product sold the most? Why do you think it did?

# In[47]:


#group rows by product and get the sum of orderd quantity  
res4=all_data.groupby('Product')['Quantity Ordered'].sum().reset_index(name='num_purchased')
#get the price of each product 
res5=all_data.groupby('Product').mean()['Price Each'].reset_index(name='price')
#merging this two column in the same table to use it in combined figure 
res5=pd.merge(res4,res5,on='Product',how='inner')
res5


# In[23]:


plt.bar(res4['Product'],res4['num_purchased'])
plt.xlabel('product')  # Label for the x-axis
plt.ylabel('# of purchased')  # Label for the y-axis
plt.title('highest purchased product')  # Title for the plot
#make label rotation in x-axis vertical and size of each label=15
plt.xticks(res4['Product'],rotation='vertical',size=15)
#size of each labelin y_axis=15
plt.yticks(size=15)


plt.show()


# In[48]:


# Create figure which is  top-level container for all plot elements and axis objects represents a single subplot within the figure.
fig, ax1 = plt.subplots()

# creating Bar chart by specifying x-axis and y-axis and assign this plot for ax1
res5.plot(kind='bar', x='Product', y='num_purchased', ax=ax1, color='blue')

# Create a second y-axis for the line chart by sharing the same x-axis of ax1
ax2 = ax1.twinx()

# Line chart by specifying x-axis and y-axis and assign this plot for ax2
res5.plot(kind='line', x='Product', y='price', ax=ax2, color='green', marker='o')

# Set labels and title for two y-axis and shared x-axis
ax1.set_ylabel('#_purchased', color='blue')
ax2.set_ylabel('price in ($)', color='green')
ax1.set_xlabel('product')

# Show plot
plt.show()


# In[ ]:


##your assumption is slightly right because  are commonly used in various household electronics such 
#as remote controls, toys, and small appliances. They are considered essential items for powering everyday devices.
# Unlike durable goods such as laptops or TVs,[ batteries,USB-C Charging Cable,Lightning Charging Cable] are consumable items that need to be replaced regularly 
#as they are depleted. This leads to more frequent purchases, resulting in higher sales volume.
#but in some products it seems not very right like gaming ,ultrawide and 4k monitors
##as it used in many jobs like (graphic design ,motion graphic,Video Editors and 3D Artists and Animators)and many other jobs
##so it make sense


# In[25]:


##all_data[all_data['Product'].isin(['USB-C Charging Cable'
#,'Lightning Charging Cable',
#'AAA Batteries (4-pack)',
#'AA Batteries (4-pack)' ])].drop_duplicates(keep='first')[['Product','Price Each']]


# In[26]:



all_data.groupby('city')['total_amount'].sum().reset_index(name='total_amount')

