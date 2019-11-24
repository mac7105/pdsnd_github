import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input ("Which city's bikeshare data do you want to explore (Chicago, New York City or Washington)? ").lower()
    while city not in ("chicago", "new york city", "washington"):
        print("Your input might be wrong, please try again... ")
        city = input ("Which city's bikeshare data do you want to explore (Chicago, New York City or Washington)? ").lower()
    else:
        print("You selected", city)

    # get user input for month (all, january, february, ... , june)
    month = input("Enter the month you want to analyze. Select one of the first six months or all: ").title()
    while month not in ("January", "February", "March", "April", "May", "June","all"): 
        print("Only the months from January up until June are available!") 
        month = input("Enter the month you want to analyze. Select one of the first six months or all: ").title()
    else:
        print("You selected", month)
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input ("Enter the day of the week for your analysis: ").title()
    while day not in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "all"):
        print("Your input might be wrong, please try again... ")
        day = input("Enter the day of the week for your analysis: ").title()
    else:
        print ("Great stuff! You are done with your selection.", day)
    
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
 
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df["Start Time"])  
    df['month'] = df['Start Time'].dt.strftime('%B')    
    df["day_of_week"] = df["Start Time"].dt.weekday_name
    
    if month != "All":
        df = df[df["month"] == month]

    if day != "All":
        df = df[df["day_of_week"] == day]
    
    return df
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df["month"].mode()
    print("Most Frequent Month: ", most_common_month)

    # display the most common day of week
    most_common_day = df["day_of_week"].mode()
    print ("Most Frequent Day: ", most_common_day)
  
    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    most_common_hour = df["hour"].mode()
    print ("Most Frequent Hour: ", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df["Start Station"].mode()
    print("Most common Start Station: ", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df["End Station"].mode()
    print("Most common End Station: ", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df['Start Station'] + "*" + df['End Station']
    common_station = most_common_start_end_station.value_counts().idxmax()
    print('The most commonly used Start Station and End Station are:\n{} \nto\n{}'.format(common_station.split('*')[0], common_station.split('*')[1]))       

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
   
    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total Travel Time is ", total_travel_time)

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("Average Travel Time is ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print("The counts of user types are ", user_types)

    # Display counts of gender
    counts_of_gender = df["Gender"].value_counts()
    print("The counts of gender are ", counts_of_gender)

    # Display earliest, most recent, and most common year of birth
    if city=='washington':
        print('Year count is unavailable for Washington.')
    else:
        earliest_year = df["Birth Year"].min()
        print("Earliest year of birth:", earliest_year)

    most_recent = df["Birth Year"].max()
    print("Most recent year of birth:", most_recent)

    most_common_year = df["Birth Year"].mode()
    print("Most common year of birth:", most_common_year)     

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        
        data_request_1 = input ("Do you want to display the first five rows of the database? Enter Yes or No.").title()
        if data_request_1 != "Yes":
            print("Thank you!")
            
        else:
            print(df.head(6))
            data_request_2 = input ("Do you want to display five more rows? Enter Yes or No.").title()
            
            num = 6
            count_by = 5
            rows = num
            while data_request_2 == "Yes":
            
                rows += count_by
                print(df.head(rows))
                data_request_2 = input ("Do you want to display five more rows? Enter Yes or No.").title()
                               
            else:
                print("Thank you")
        restart = input('\nWould you like to restart? Enter Yes or No.\n')
        if restart.lower() != 'Yes':
            break

if __name__ == "__main__":

	main()