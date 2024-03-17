# TODO: python not found error when use this file as dataloader
import pandas as pd

# generate dummy pandas dataframe
df = pd.DataFrame({
    'name': ['John', 'Anna', 'Peter', 'Linda'],
    'age': [23, 36, 32, 28],
    'city': ['New York', 'Paris', 'Berlin', 'London']
})

# print dataframe in csv format
# print(df.to_csv())
# save dataframe to csv file
df.to_csv('docs/data.csv', index=False)
