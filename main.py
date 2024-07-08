import classify_transactions
import pandas as pd

classify_transactions.transactions()
df = pd.DataFrame(classify_transactions.transactions())

# create a table for income information

Income_Table = df.query("Amount > 0").groupby('year_month')['Amount'].sum().reset_index(name ='sum')
Income_Table

# change the amounts for graphs
df['Amount'] = df.Amount*(-1)  

# create a function to create a df for each category grouped by month

categories = df['Category'].unique()
dfs = {}
for category in categories:
    dfs[f"{category}_Table"] = df[df['Category'] == category].groupby('year_month')['Amount'].sum().reset_index(name=f"{category}_sum")
for key in dfs:
    exec(f"{key} = dfs['{key}']")
    print(key)

# show all dfs in memory
alldfs = [var for var in dir() if isinstance(eval(var), pd.core.frame.DataFrame)]
alldfs


# alt option to view dataframes:
# %whos DataFrame








