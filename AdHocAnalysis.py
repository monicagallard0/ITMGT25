import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import date

file = open("transaction-data-adhoc-analysis.json")
data = json.load(file)
df = pd.DataFrame(data)
df["transaction_date"] = pd.to_datetime(df["transaction_date"], format = "%Y/%m/%d")
df["transaction_items"] = df["transaction_items"].str.split(";")
df = df.explode("transaction_items").reset_index(drop=True)

df["transaction_items"] = df["transaction_items"].str.split(",")

def product(name): 
    productname = name[1]
    return productname
df["Product"] = df["transaction_items"].apply(product)

def quantity(name): 
    quantity = name[2]
    return quantity
df["Quantity"] = df["transaction_items"].apply(quantity)
df['Quantity'] = df['Quantity'].str.extract('(\d+)', expand=False)
df['Quantity'] = df['Quantity'].astype(int)

df["transaction_items"] = df["transaction_items"].str.join(",")
itemqty = df.groupby([df.transaction_date.dt.month,'Product'])['Quantity'].sum().unstack(level=0)
itemqty.columns = ['January', 'February', 'March', 'April', 'May', 'June']

itemqty.plot.bar(rot=0,figsize=(15,5))



newdf = pd.DataFrame(data)
pricelist = newdf[["transaction_items","transaction_value"]].loc[(newdf['transaction_items'].str.contains(";") == False) & (newdf['transaction_items'].str.contains("x1"))].drop_duplicates(subset = ["transaction_items"]).reset_index(drop = True)
pricelist["transaction_items"] = pricelist["transaction_items"].str.split(",")
pricelist["transaction_items"] = pricelist["transaction_items"].apply(product)
pricelist.columns = ['Product', 'Price']
pricelist = pricelist.set_index('Product')
concat = pd.concat([itemqty, pricelist], axis=1)

concat['January'] = concat['January']*concat['Price']
concat['February'] = concat['February']*concat['Price']
concat['March'] = concat['March']*concat['Price']
concat['April'] = concat['April']*concat['Price']
concat['May'] = concat['May']*concat['Price']
concat['June'] = concat['June']*concat['Price']
concat.drop('Price', inplace=True, axis=1)

concat.plot.bar(rot=0,figsize=(15,5))



frequency = pd.crosstab(df.name,df.transaction_date.dt.month)
frequency.columns = ['January', 'February', 'March', 'April', 'May', 'June']

repeaters = [0]
repeaters.append(len(frequency.loc[(frequency['January'] != 0) & (frequency['February'] != 0)]))
repeaters.append(len(frequency.loc[(frequency['February'] != 0) & (frequency['March'] != 0)]))
repeaters.append(len(frequency.loc[(frequency['March'] != 0) & (frequency['April'] != 0)]))
repeaters.append(len(frequency.loc[(frequency['April'] != 0) & (frequency['May'] != 0)]))
repeaters.append(len(frequency.loc[(frequency['May'] != 0) & (frequency['June'] != 0)]))

repeatersdata = pd.DataFrame(repeaters,index = ['January', 'February', 'March', 'April', 'May', 'June'], columns=['Repeaters']).transpose()



inactive = [0]
inactive.append(len(frequency.loc[(frequency['January'] != 0) & (frequency['February'] == 0)]))
inactive.append(len(frequency.loc[((frequency['January'] != 0) | (frequency['February'] != 0)) & (frequency['March'] == 0)]))
inactive.append(len(frequency.loc[((frequency['January'] != 0) | (frequency['February'] != 0) | (frequency['March'] != 0)) & (frequency['April'] == 0)]))
inactive.append(len(frequency.loc[((frequency['January'] != 0) | (frequency['February'] != 0) | (frequency['March'] != 0) | (frequency['April'] != 0)) & (frequency['May'] == 0)]))
inactive.append(len(frequency.loc[((frequency['January'] != 0) | (frequency['February'] != 0) | (frequency['March'] != 0) | (frequency['April'] != 0) | (frequency['May'] != 0)) & (frequency['June'] == 0)]))

inactivedata = pd.DataFrame(inactive,index = ['January', 'February', 'March', 'April', 'May', 'June'], columns=['Inactive']).transpose()



engaged = []
engaged.append(len(frequency.loc[(frequency['January'] != 0)]))
engaged.append(len(frequency.loc[(frequency['January'] != 0) & (frequency['February'] != 0)]))
engaged.append(len(frequency.loc[(frequency['January'] != 0) & (frequency['February'] != 0) & (frequency['March'] != 0)]))
engaged.append(len(frequency.loc[(frequency['January'] != 0) & (frequency['February'] != 0) & (frequency['March'] != 0) & (frequency['April'] != 0)]))
engaged.append(len(frequency.loc[(frequency['January'] != 0) & (frequency['February'] != 0) & (frequency['March'] != 0) & (frequency['April'] != 0) & (frequency['May'] != 0)]))
engaged.append(len(frequency.loc[(frequency['January'] != 0) & (frequency['February'] != 0) & (frequency['March'] != 0) & (frequency['April'] != 0) & (frequency['May'] != 0) & (frequency['June'] != 0)]))

engageddata = pd.DataFrame(engaged,index = ['January', 'February', 'March', 'April', 'May', 'June'], columns=['Engaged']).transpose()



everything = pd.concat([repeatersdata, inactivedata, engageddata], axis=0)

everything.plot.bar(rot=0,figsize=(15,5))