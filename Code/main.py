import pandas as pd
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]
df=pd.read_csv("../Sales_Data/Sales_April_2019.csv")
print(df)

all_months_data=pd.DataFrame()
files=[file for file in os.listdir("../Sales_Data")]
for file in files:
    df=pd.read_csv("../Sales_Data/"+file)
    all_months_data=pd.concat([all_months_data,df])
    
all_months_data.to_csv("all_data.csv",index=False)

all_data=pd.read_csv("all_data2.csv")
print(all_data.head())

#Cleaning the data
nan_df=all_data[all_data.isna().any(axis=1)]
print(nan_df.head())



all_data=all_data.dropna(how='all')
print(all_data.head())

all_data=all_data[all_data['Order Date'].str[0:2]!="Or"]
print(all_data.head())

all_data['Quantity Ordered']=pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each']=pd.to_numeric(all_data['Price Each'])
all_data['Order Date']=pd.to_datetime(all_data['Order Date'])

#Adding columns for convinience

# Add Month Column

all_data['Month']=all_data['Order Date'].dt.month
print(all_data.head())


#Adding sales Column
all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']
print(all_data.head())

# Adding City Column
all_data['City']=all_data['Purchase Address'].apply(lambda x: get_city(x) + ' ('+get_state(x)+')')
print(all_data.head())

# Adding Hur Column
all_data['Hour']=all_data['Order Date'].dt.hour
all_data['Minute']=all_data['Order Date'].dt.minute

#What was the best month for sales? and amt earned in it

results=(all_data.groupby('Month').sum())

months=range(1,13)
plt.bar(months,results['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()






# What city has the highest  number of sales
results=all_data.groupby('City').sum()
cities=[city for city,df in all_data.groupby('City')]
plt.bar(cities,results['Sales'])
plt.xticks(cities,rotation='vertical',size=8)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Citiy name')
plt.show()


# What time should we display ads to maximize likelihood of customer buying the product

hours =[hour for hour,df in all_data.groupby('Hour')]
plt.plot(hours,all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of orders')
plt.grid()
plt.show()


#What product sold the most
product_group = all_data.groupby('Product')
quantity_ordered=product_group.sum()['Quantity Ordered']

products = [product for product,df in product_group]
prices=all_data.groupby('Product').mean()['Price Each']
fig,ax1 = plt.subplots()
ax2=ax1.twinx()
ax1.bar(products,quantity_ordered,color='g')
ax2.plot(products,prices,'b-')

ax1.set_xlabel('Products')
ax1.set_ylabel('Quantity Bought',color='g')
ax2.set_ylabel('Price in USD ($)',color='b')
ax1.set_xticklabels(products,rotation='vertical',size=8)
plt.show()

# What product are most often bought together by the customers
df=all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x:','.join(x))
df=df[['Order ID','Grouped']].drop_duplicates()
print(df.head())


count=Counter()
for row in df['Grouped']:
    row_list=row.split(',')
    count.update(Counter(combinations(row_list,2)))

for key,value in count.most_common(10):
    print(key,value)
