import pandas as pd                       #to perform data manipulation and analysis
import numpy as np                        #to cleanse data
import os                                 #to get update time of file
import time
from datetime import datetime  

# import category mapping 

cat = 'X:/Local_Repo/Budget/Mappings/category_mapping.csv'
subcat = 'X:/Local_Repo/Budget/Mappings/sub_category_mapping.csv'

catmap = pd.read_csv(cat)
subcatmap = pd.read_csv(subcat)

def catmapdf():
    data = catmap  
    return data

def subcatmapdf():
    data = subcatmap  
    return data

# Define the file paths for my accounts
chase_raw = 'X:/MyData/Chase_Activity.csv'
ncu_raw = 'X:/MyData/MYNCU.csv'
cashapp_raw = 'X:/MyData/cash_app_report.csv'

# check the latest time data was updated in AA/PM format
chase_upd_dt = datetime.fromtimestamp(os.path.getmtime(chase_raw)).strftime('%Y-%m-%d %I:%M:%S %p')
ncu_upd_dt = datetime.fromtimestamp(os.path.getmtime(ncu_raw)).strftime('%Y-%m-%d %I:%M:%S %p')
cashapp_upd_dt = datetime.fromtimestamp(os.path.getmtime(cashapp_raw)).strftime('%Y-%m-%d %I:%M:%S %p')

# Read the CSV files into separate data frames
chase_df = pd.read_csv(chase_raw,index_col=False)
ncu_df = pd.read_csv(ncu_raw,index_col=False,header = 3)
cashapp_df = pd.read_csv(cashapp_raw,index_col=False)

print(f"chase_df was updated: {chase_upd_dt}\nncu_df was updated {ncu_upd_dt} \ncashapp_df was updated {cashapp_upd_dt}")

# Clean up chase_df
chase_df.drop(['Details','Balance','Type','Check or Slip #'], axis=1, inplace=True)     
chase_df['Description'] = chase_df['Description'].astype(str).str.upper()
chase_df = chase_df.rename(columns={'Posting Date': 'Date'})

# Clean up ncu_df
ncu_df['Description'] = ncu_df['Description'].astype(str).str.upper() + ' ' + ncu_df['Memo'].astype(str).str.upper()
ncu_df['Amount'] = np.where(ncu_df['Amount Debit'].notnull(), ncu_df['Amount Debit'], ncu_df['Amount Credit'])
ncu_df.drop(['Transaction Number','Check Number','Memo','Amount Debit','Amount Credit','Balance','Fees  '], axis=1, inplace=True)     

# Clean up cashapp_df
# format the date
cashapp_df['Date'] = cashapp_df['Date'].str.replace('CST|CDT', '', regex=True) # remove tz for formatting
cashapp_df['Date'] = cashapp_df['Date'].apply(pd.to_datetime)                  #convert to date
cashapp_df['Date'] = cashapp_df['Date'].dt.strftime('%m/%d/%Y')                #re-format to match other dfs
# option to remove certain transactions 
# cashapp_df = cashapp_df[~cashapp_df['Transaction Type'].isin(['Bitcoin Buy','Bitcoin Sale', 'Bitcoin Boost','Stock Sell','Stock Buy','Boost Payment'])]
# Create a new 'Description' column in cashapp_df combining Transaction Type, Notes, and Name
cashapp_df['Description'] = cashapp_df['Transaction Type'] + ' ' + cashapp_df['Notes'].fillna(cashapp_df['Name of sender/receiver']).fillna('')
# Convert the 'Description' column to uppercase
cashapp_df['Description'] = cashapp_df['Description'].str.upper()
# fix the amount field
cashapp_df['Amount'] = cashapp_df['Amount'].str.replace('$', '')                # remove the $
cashapp_df['Amount'] = pd.to_numeric(cashapp_df['Amount'], errors='coerce')     # convert the format to numeric
#drop columns
cashapp_df.drop(['Transaction ID','Currency','Asset Type','Asset Price','Asset Amount','Account','Fee',
          'Status','Name of sender/receiver','Notes','Transaction Type','Net Amount'], axis=1, inplace=True)     

# Add a new columns 'Source' indicating the source and last updated
chase_df['Source'] = 'Chase Bank'
chase_df['Source Updated'] = chase_upd_dt
ncu_df['Source'] = 'Neighborhood CU'
ncu_df['Source Updated'] = ncu_upd_dt
cashapp_df['Source'] = 'Cash App'
cashapp_df['Source Updated'] = cashapp_upd_dt

# Combine the dataframes into a single dataframe
df = pd.concat([chase_df, ncu_df, cashapp_df], ignore_index=True)

#filter out items prior to 2023
df = df[pd.to_datetime(df['Date']).dt.year >= 2023]

df['Date'] = pd.to_datetime(df['Date'])
df['year_month'] = df['Date'].dt.strftime('%Y-%m')
df['month_day'] = df['Date'].dt.strftime('%m-%d')
df['week'] = df['Date'].dt.strftime('%V')
df['year'] = df['Date'].dt.strftime('%Y')

def transaction_data():
    data = df  
    return data

