#### SCRATCH SHEET ####
### Section 1 Getting Started With Pandas ###
import os

import pandas as pd

## Anatomy Dataframe ##
# Dataframe is composed of one or more series, series are columns, indexes are rows #
os.chdir('C:/Users/gschlett/Downloads/Coding/Anaconda/envs/pandas_workshop/pandas-workshop-main/data')

meteorites = pd.read_csv('C:/Users/gschlett/Downloads/Coding/Anaconda/envs/pandas_workshop/pandas-workshop-main/data/Meteorite_Landings.csv', nrows = 5)

# To see Series #
print(meteorites.name)

# To see Columns #
print(meteorites.columns)

# To see rows or indexes #
print(meteorites.index)

## Creating Dataframes ## 

# Using a flat file # 

meteorites = pd.read_csv('C:/Users/gschlett/Downloads/Coding/Anaconda/envs/pandas_workshop/pandas-workshop-main/data/Meteorite_Landings.csv', nrows = 5)

## Inspecting the Data ## 

# Data from an API #

response = requests.get(
    'https://data.nasa.gov/resource/gh4g-9sfh.json',
    params={'$limit': 50_000}
)

if response.ok:
    payload = response.json()
else:
    print(f'Request was not successful and returned code: {response.status_code}.')
    payload = None

df = pd.DataFrame(payload)

df.head(3)

# What are the data types #
print(df.dtypes)

# Retrieving information about dataframe #
print(df.info())

## Extracting Subsets of DF's ##
# Selecting Columns #

CoLuMns = df[['name', 'mass']]

# Selecting Rows #

RoWs = df[100:104]

# Indexing, can use -iloc{}- to select rows and columns by their positions #

PoSiTion = df.iloc[100:104, [0, 3, 4, 6]]

# Indexing but selecting columns based on their names #
NaMeS = df.loc[100:104, 'name':'year'] #### With this selection it's loc and not iloc ####

## Filtering with Boolean Masks ##

# Trying to make mass column integer #

#df = df.astype({'mass':'int'}) # Still not working #

# Way of filtering which rows and columns we want #

#(df['mass'] > 50) & (df.fall == 'Found')




# Error message for above comment was '> not supported between instances of str and int ' 

# ALternative to above method is using query # 

Lastone = df.query("'mass' > 1e6 and fall == 'fell'") # Still not working cause mass column is str #

## Calculating Summary Statistics ## 
df = pd.read_csv('C:/Users/gschlett/Downloads/Coding/Anaconda/envs/pandas_workshop/pandas-workshop-main/data/Meteorite_Landings.csv')

# How many meteorites were found vs observed falling #

print(df.fall.value_counts())

# mass of average/median meteorite #

print(df['mass (g)'].median())

# Looking at quantiles # 

print(df['mass (g)'].quantile([0.01, 0.05, 0.95, 0.99]))

# What is the mass of heaviest meteorite #
print(df['mass (g)'].max())

# Pull all the information on this meteorite # 
print(df.loc[df['mass (g)'].idxmax()])

# How many different classes are represented in this dataset # 
print(df.recclass.nunique())

print(df.recclass.unique()[:14])

# Getting summary stats #

dff = df.describe(include = 'all')


