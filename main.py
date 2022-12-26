### Working Data Frames with Pandas ###

## Creating New Data Frame From Scratch ##

import pandas as pd
import os
from pathlib import Path
# Each column in a data frame is called a series #
df = pd.DataFrame(
    {
        'Name': [
            'Braund, Mr. Owen Harris',
            'Allen, Mr. William Henry',
            'Bonnell, Ms. Elizabeth',
            ],
        'Age': [22, 35, 38],
        'Sex': ['M', 'M', 'F'],
    }
)

print(df)

# Want to know the max age of someone in the data frame #

print(df['Age'].max())

# Want to know some basic Statistics of the Age Series #
print(df.describe())

## Reading in CSV Files ##
os.chdir('C:\Python\PythonProjects\DataFrameswithPandas')

print(Path.cwd())

titanic = pd.read_csv('C:/Python/PythonProjects/DataFrameswithPandas/titanic.csv')

print(titanic)

# See the first 8 rows of a panda dataframe #
print(titanic.head(8))
print(titanic.tail(10)) # Returns the last 10 rows of a data frame #

# How Pandas interprets the data types of each column #
print(titanic.dtypes)

# If you want it to be a xlsx spreadsheet #
# titanic.read_excel('titanic.xlsx', sheet_name = 'Passengers') #

## Selecting subset of a dataframe ##
# Selecting age of titanic passengers #

ages = titanic["Age"]

print(ages.head())

age_sex = titanic[['Age', 'Sex']]

print(age_sex.head())

# Filtering specific rows from a data frame #
above_35 = titanic[titanic['Age'] > 35]

print(above_35.head(20))

# Filtering based on cabin class #
HighClass = titanic[titanic['Pclass'].isin([2, 3])]

print(HighClass.head())

# Filtering out passengers where age is unknown #
age_known = titanic[titanic['Age'].notna()]

print(age_known.head())

## Selecting specific cells using Pandas ##
adult_names = titanic.loc[titanic["Age"] > 35, "Name"]

print(adult_names.head())


