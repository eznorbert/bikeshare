import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTHS = ('', 'january', 'february', 'march', 'april', 'may', 'june', 'all')
DAYS = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all')


def get_user_input(input_prompt, error_prompt, pick_list, format_value):
    """Get interactive user input for the filters of city, month and workday!"""

    while True:
        ret = input(input_prompt)
        ret = format_value(ret)
        if ret in pick_list:
            print("You have selected: {}!".format(ret.title()))
            return ret
        else:
            print(error_prompt)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('=' * 40)
    print('Hello! Let\'s explore some US bikeshare data!')

    city = get_user_input("\nPlease specify the city in which you want to view the data!"
                          "\nChicago, New York City or Washington (mandatory but not case sensitive): ",
                          "Please specify a valid city!",
                          CITY_DATA.keys(),
                          lambda x: str.lower(x))

    month = get_user_input("\nPlease specify a month, use 'all' for all months: ",
                           "Please specify a valid month!",
                           MONTHS[1:],
                           lambda x: str.lower(x))

    day = get_user_input("\nPlease specify a workday, use 'all' for all workdays: ",
                         "Please specify a valid day!",
                         DAYS,
                         lambda x: str.lower(x))

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    if month != 'all':
        month = MONTHS.index(month)
        df = df[df['month'] == month]

    if day != 'all':
        day = DAYS.index(day)
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    print("The users ride most in the month: {}!".format(MONTHS[most_common_month].title()))

    most_common_day = df['day_of_week'].mode()[0]
    print("The users ride most on the day: {}!".format(DAYS[most_common_day].title()))

    most_common_hour = df['hour'].mode()[0]
    print("The users ride most at the hour: {}!".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    print("The users ride most from the station: {}!".format(most_common_start_station.title()))

    most_common_end_station = df['End Station'].mode()[0]
    print("The users ride most to the station: {}!".format(most_common_end_station))

    df['Trip Combination'] = df['Start Station'] + ' -> ' + df['End Station']
    most_common_trip = df['Trip Combination'].mode()[0]
    print("The trip the users ride most is: {}!".format(most_common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print("The users ride together {} seconds!".format(total_travel_time))

    mean_travel_time = df['Trip Duration'].mean()
    print("The users ride for every trip on average {} seconds!".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        user_type_counts = df['User Type'].value_counts()
        print("Different user types are as follows: \n{}".format(user_type_counts))
    except KeyError:
        print("\nThere's no user type information!")
    try:
        gender_counts = df['Gender'].value_counts()
        print("\nThe user gender distribution is as follows: \n{}".format(gender_counts))
    except KeyError:
        print("\nThere's no gender information!")
    try:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print("\nThe youngest user was born in {}, the oldest was born in {}, and most were born in {}!".format(
            most_recent_year, earliest_year, most_common_year
        ))
    except KeyError:
        print("\nThere's no birth information!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
