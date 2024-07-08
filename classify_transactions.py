import cleandata
import pandas as pd

cleandata.transaction_data()
df = pd.DataFrame(cleandata.transaction_data())

cleandata.catmapdf()
categories = pd.DataFrame(cleandata.catmapdf())

cleandata.subcatmapdf()
subcategories = pd.DataFrame(cleandata.subcatmapdf())

# convert category csv to df then dict

category_dict = categories.set_index('Category').to_dict()['Mapped Value']

# Apply the mapping based on partial matches
for keyword, category in category_dict.items():
    df.loc[df['Description'].str.contains(keyword, case=False, na=False), 'Category'] = category

# nan in the df was a representation of nan, we'll use replace

df['Category'].replace('nan', 'Shopping', inplace=True)

# convert category csv to dict and apply categories

sub_category_dict = subcategories.set_index('SubCategory').to_dict()['Mapped Value']

for category,keyword in sub_category_dict.items():
    df.loc[df['Description'].str.contains(keyword, case=False, na=False), 'Sub_Category'] = category

df['Sub_Category'].replace('nan', 'Misc', inplace=True)

def transactions():
    data = df  
    return data