### Lesson 2 Pandas Workshop ###

## Data Cleaning ##

taxis = pd.read_csv('C:/Users/gschlett/Downloads/Coding/Anaconda/envs/pandas_workshop/pandas-workshop-main/data/2019_Yellow_Taxi_Trip_Data.csv')

# Dropping some columns, removing columns that have id in it #

mask = taxis.columns.str.contains('id$|store_and_fwd_flag', regex = True) # Regex tests if pattern is true #

columns_to_drop = taxis.columns[mask]

taxis = taxis.drop(columns=columns_to_drop)

# Renaming Columns #
taxis.rename(
    columns = {
        'tpep_pickup_datetime': 'pickup', 
        'tpep_dropoff_datetime': 'dropoff'
        },
    inplace = True
    )

# Converting data types to datetime and not object #

taxis.loc[:, ['pickup', 'dropoff']] = \
    taxis.loc[:, ['pickup', 'dropoff']].apply(pd.to_datetime)

print(taxis.dtypes)

# Creating New Columns #
# wanting to calculate for each row: elapsed time of trip, tip percentage, total taxes fees surcharges, average taxi speed #
taxinew = taxis.assign(
    elapsed_time = lambda x: x.dropoff - x.pickup,
    cost_before_tip = lambda x: x.total_amount - x.tip_amount,
    tip_pct = lambda x: x.tip_amount / x.cost_before_tip,
    fees = lambda x: x.cost_before_tip - x.fare_amount, 
    avg_speed = lambda x: x.trip_distance.div(
        x.elapsed_time.dt.total_seconds() / 60 /60
        )
    )
# In above example use lambda function to avoid typing taxis repeatedly #

# Sorting by values #
taxinew.sort_values(['passenger_count', 'pickup'], ascending=[False, True]) # to put in DF inplace=True#

# picking out smallest and largest using nlargest() and nsmallest() #
print(taxinew.nlargest(3, 'elapsed_time'))

## Working with the Index ##
# Switching from a RangeIndex to a DatetimeIndex by specifying datetime column with set_index() #
taxinew.set_index('pickup', inplace=True)

# Sort by new index # 
taxinew.sort_index(inplace = True)

# Select ranges based on data from datetime same as we did with rows #
print(taxinew['2019-10-23 07:45':'2019-10-23 08'])

# When not specifying a range use loc() #
# taxinew.loc['2019-10-23 08]

# Resetting the Index, reverts back to how it was # 
taxinew.reset_index(inplace=True)

## Reshaping the Data ## 
tsa = pd.read_csv('C:/Users/gschlett/Downloads/Coding/Anaconda/envs/pandas_workshop/pandas-workshop-main/data/tsa_passenger_throughput.csv',
                  parse_dates = ['Date'])

# lowercase column names and take the first word #
tsa = tsa.rename(columns = lambda x: x.lower().split()[0])

# Melting. helps convert data into long format # 
tsa_melted = tsa.melt(
    id_vars = 'date', # Column that uniquely identifies a row (can be multiple) #
    var_name = 'year', # name for the new column created by melting #
    value_name = 'travelers' # name for new column containing values from melted columns #
    )
print(tsa_melted.sample(5, random_state=1)) # Show some random entries #

# Converting into a time series of traveler throughput #
tsa_meltednew = tsa_melted.assign(
    date = lambda x: pd.to_datetime(x.year + x.date.dt.strftime('-%m-%d'))
    )

# Dropping null values #
tsa_meltednew = tsa_meltednew.dropna()


# Pivoting allows us to compare TSA Traveler Throughput on specific days across years #
tsa_pivoted = tsa_meltednew\
    .query('date.dt.month == 3 and date.dt.day <= 10')\
    .assign(day_in_march = lambda x: x.date.dt.day)\
    .pivot(index = 'year', columns = 'day_in_march', values = 'travelers')
    
# Transposing the T attribute is a quick way to flip rows and columns #
tsa_repivoted = tsa_pivoted.T

# Merging # 
# Merging TSA Travel along with holidays # 
holidays = pd.read_csv('C:/Users/gschlett/Downloads/Coding/Anaconda/envs/pandas_workshop/pandas-workshop-main/data/holidays.csv',
                       parse_dates = True, index_col = 'date')
holidays.loc['2019']

tsa_melted_holidays = tsa_meltednew\
    .merge(holidays, left_on = 'date', right_index = True, how = 'left')\
    .sort_values('date')

# Making a few days before and after the holiday a part of the holiday #
tsa_melted_holiday_travel = tsa_melted_holidays.assign(
    holiday = lambda x:
        x.holiday\
            .fillna(method = 'ffill', limit = 1)\
            .fillna(method = 'bfill', limit = 2)
            )

## Aggregations and Grouping ##

# Pivot Table, building a table to compare holiday travel across the years in our dataset #
tsa_melted_holiday_travel.pivot_table(
    index = 'year', columns = 'holiday', 
    values = 'travelers', aggfunc = 'sum'
    ).pct_change()

# Crosstabs, easy way to create a frequency table # 
print(pd.crosstab(
    index = pd.cut(
        tsa_melted_holiday_travel.travelers,
        bins = 3, labels = ['low', 'medium', 'high']
        ),
    columns = tsa_melted_holiday_travel.year,
    rownames = ['travel_volume']
    ))


## Times Series ##

taxis = pd.read_csv('C:/Users/gschlett/Downloads/Coding/Anaconda/envs/pandas_workshop/pandas-workshop-main/data/2019_Yellow_Taxi_Trip_Data.csv')

mask = taxis.columns.str.contains('id$|store_and_fwd_flag', regex = True)

columns_to_drop = taxis.columns[mask]

taxis = taxis.drop(columns=columns_to_drop)

taxis.rename(
    columns = {
        'tpep_pickup_datetime': 'pickup', 
        'tpep_dropoff_datetime': 'dropoff'
        },
    inplace = True
    )

# selecting based on date and time #

taxis.set_index('dropoff', inplace = True)

taxis.sort_index(inplace = True)

taxisdates = taxis['2019-10-24 12' : '2019-10-24 13']
