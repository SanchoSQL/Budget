import classify_transactions
import pandas as pd


classify_transactions.transactions()
df = pd.DataFrame(classify_transactions.transactions())


Income_Table = df.query("Amount > 0").groupby('year_month')['Amount'].sum().reset_index(name ='sum')
Income_Table

df['Amount'] = df.Amount*(-1)  

categories = df['Category'].unique()
dfs = {}
for category in categories:
    dfs[f"{category}_Table"] = df[df['Category'] == category].groupby('year_month')['Amount'].sum().reset_index(name=f"{category}_sum")
for key in dfs:
    exec(f"{key} = dfs['{key}']")
    print(key)


# %whos DataFrame





