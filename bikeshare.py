import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['monday', 'tuesday', 'wednessday', 'thursday', 'friday', 'saturday', 'sunday']

CITIES = ['chicago', 'new york city', 'washington']

def get_filter(options_name, options, all_option=False):

    """
    Asks user to specify a filter using filter id, filter name or all when possible
    Args:
        (str)  options_name - name of the filter parameter
        (list) options - avalaible options for the filter
        (Bool) all_options - False if all option is not allowed (default False)
    Returns:
        (str) choosen_filter - name of the filter to use for analysis or 'all' when possible 
    """

    # message to display for the filter selection
    get_message = 'Choose a {} you will like to explore: '.format(options_name)
    
    # if all option is possible for the particular filter, add it to the begining of the options
    if all_option:
        options.insert(0, 'all')

    # generate the menu to be display along the message
    for index in range(len(options)):
        get_message += "\n[{}] {}".format(index+1, options[index].title())
    
    
    # display message with a newline
    print(get_message + '\n')
    
    # get user input
    choosen_filter = get_user_input(options_name, options)
    
    # get user input until a valid input is given
    while choosen_filter not in options:
       choosen_filter = get_user_input(options_name, options)

    return choosen_filter

def get_user_input(options_name, options):

    """
    Asks user to provide an input for a filter using it's name or given id

    Args:
        (str) option_name - name of the filter parameter
        (list) options - avalaible options for the filter
    Returns:
        (str) choosen_filter - the option choosen by the user
    """

    # accept user input with customized message based on filter
    user_input = input('choose a {} using number or city name: '.format(options_name))
    user_input = user_input.strip() #remove extra spaces at begining and end

    # checking for integer value
    try:
        user_input = int(user_input)
        user_input = user_input - 1
        
        # checking to make sure integer is not greater than length of options
        try:
            choosen_filter = options[user_input]
        
        # if integer is greater than length of options
        except IndexError:
            choosen_filter = user_input

    # if user input is not integer
    except ValueError:
        choosen_filter = user_input.lower() #change user input to lower case for comparison
    
    return choosen_filter

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #get user input for city (chicago, new york city, washington) using city id or name.
    cities = CITIES.copy() #create a copy of cities
    city = get_filter('city', cities) #get city filter
    print("Selected city: {}".format(city.title())) 

    #get user input for month (all, january, february, ... , june)
    months = MONTHS.copy() #create copy of MONTHS available 
    month = get_filter('month', months, all_option=True) #get month filter
    print("Selected month: {}".format(month.title()))


    #get user input for day of week (all, monday, tuesday, ... sunday)
    days = DAYS.copy() #create a copy of DAYS available
    day = get_filter('day', days, all_option=True) #get day filter
    print("Selected day: {}".format(day.title()))

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

    # extract month, day of week and start hour from Start Time to create new columns
    df['month'] =  df['Start Time'].dt.strftime('%B')
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')
    df['start_hour'] = df['Start Time'].dt.hour

    

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title() ]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (DataFrame) df - Filtered Pandas DataFrame
    
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    most_common_month = df['month'].mode()[0]
    print('Popular month: {}'.format(most_common_month))

    #display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('Popular day of week: {}'.format(most_common_day_of_week))


    #display the most common start hour
    most_common_start_hour = df['start_hour'].mode()[0]
    print('Popular start hour: {}'.format(most_common_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (DataFrame) df - Filtered Pandas DataFrame
    
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Popular start station: {}'.format(most_common_start_station))


    #display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Popular end station: {}'.format(most_common_end_station))


    #display most frequent combination of start station and end station trip
    most_common_station_combination = (df['Start Station'] + ' <----> ' + df['End Station']).mode()[0]
    print('Popular station combination: {}'.format(most_common_station_combination))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (DataFrame) df - Filtered Pandas DataFrame
    
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_time_travel = df['Trip Duration'].sum()
    print('Total time travel: {}'.format(total_time_travel))

    #display mean travel time
    mean_time_travel = df['Trip Duration'].mean()
    print('Mean time travel: {}'.format(mean_time_travel))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    Args:
        (DataFrame) df - Filtered Pandas DataFrame
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nUser types count\n')
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print('\nUser genders count\n')
        print(genders)
    else:
        print('\nUser gender data is missing\n')
    print('\n')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        popular_birth_year = int(df['Birth Year'].mode()[0])

        print('Earliest birth year: {}'.format(earliest_birth_year))
        print('Most recent birth year: {}'.format(recent_birth_year))
        print('Popular birth year: {}'.format(popular_birth_year))
    else:
        print('\nUser Birth Year data is missing\n')
    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df, start_index=0, chunk_size=5):
    """
    Displays raw data in chunks.
    
    Args:
        (DataFrame) df - Filtered Pandas DataFrame
        (int) start_index - Begining of slice for each chunk default 0
        (int) chunk_size - Size of each chunk default 5
    
    """

    show_raw_data = input('\nWould you like see raw data? Enter yes or no.\n')
    
    end_index = start_index + chunk_size
    
    while show_raw_data.lower() == 'yes' and end_index < df.shape[0]:
        print(df[start_index:end_index])
        show_raw_data = input('\nWould you like see raw data? Enter yes or no.\n')
        start_index += chunk_size
        end_index = start_index + chunk_size
        
def main():


    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
