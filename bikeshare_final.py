import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    All three inputs are filtered against a value list to avoid unexpected inputs.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_options = ("chicago", "new york city", "washington")
    city = (input('Choose between Chicago, New York City and Washington data to analyse: ')).lower()
    while city not in city_options:
        city = (input('This is not a possible option. Choose between either Chicago, New York City or Washington: ')).lower()

    # get user input for month (all, january, february, ... , june)
    month_options = ("january", "february", "march", "april", "may", "june", "all")
    month = (input('Filter by a month January - June or just type \'all\' to see the data for all month: ')).lower()
    while month not in month_options:
            month = (input('This is not a possible option. Choose a valid month name or just \'all\' : ')).lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    weekday_options = ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
    day = (input('Filter by a weekday or just type \'all\' if you want to see data for all weekdays: ')).lower()
    while day not in weekday_options:
        day = (input('This is not a possible option. Choose a valid weekday like \'thursday\' or just \'all\' : ')).lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = (df['Start Time']).dt.month
    popular_month = df['month'].mode()[0]
    print('Most Frequent Start Month:', popular_month)

    # display the most common day of week
    df['weekday_name'] = (df['Start Time']).dt.weekday_name
    popular_weekday_name = df['weekday_name'].mode()[0]
    print('Most Frequent Start Weekday:', popular_weekday_name)

    # display the most common start hour
    df['hour'] = (df['Start Time']).dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_startstation = df['Start Station'].mode()[0]
    print('Most Frequent Start Station:', popular_startstation)

    # TO DO: display most commonly used end station
    popular_endstation = df['End Station'].mode()[0]
    print('Most Frequent End Station:', popular_endstation)

    # TO DO: display most frequent combination of start station and end station trip
    trip = df['Start Station'] + " to " + df['End Station']
    popular_trip = trip.mode()[0]
    print('Most Frequent Trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    trip_duration = df['Trip Duration'].sum()
    print('Total Trip Duration:', trip_duration)
    # TO DO: display mean travel time

    trip_mean = df['Trip Duration'].mean()
    print('Mean Trip Duration:', trip_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    usertypes_groupedby = df.groupby('User Type')['User Type'].count()
    print('User stats grouped by: ' + str(usertypes_groupedby))

    # TO DO: Display counts of gender
    try:
        genders_groupedby = df.groupby('Gender')['Gender'].count()
        print('\nUser stats grouped by: ' + str(genders_groupedby))
    except:
        print('\nThere is no data for gender')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_dob = df['Birth Year'].dropna().min()
        latest_dob = df['Birth Year'].dropna().max()
        mostcommon_dob = df['Birth Year'].dropna().mode()[0]
        print ('\nThe earliest year of birth is ' + str(int(earliest_dob)) + ', the most recent one '
               + str(int(latest_dob)) + ' and the most common ' + str(int(mostcommon_dob)))
    except:
        print('There is no data for birth year')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df, city):
    """Asks the user whether he wants to see the first 5 lines of data and presents these continuously if requested"""
    lookup_options = ('yes','no')
    i = 0
    lookup = 'yes'
    while lookup == 'yes':
        print('Would you like to see the rows ' + str(i+1) + ' to ' + str(i+5) + ' of the data?')
        lookup = input('\nyes or no: ')
        while lookup not in lookup_options:
            lookup = (input('Choose either yes or no: ')).lower()
        if lookup == 'yes':
            if city == 'washington':
                print(df.iloc[0+i:5+i,1:7])
            else:
                print(df.iloc[0+i:5+i,1:9])
            i+=5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
