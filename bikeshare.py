import pandas as pd
from datetime import datetime

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}

def load_data(city, month, day):
    try:
        # Load data file into a dataframe
        df = pd.read_csv(CITY_DATA[city])

        # Convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # Extract month and day of week from Start Time
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.day_name()

        # Filter by month if applicable
        if month.lower() != 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
            month = months.index(month.lower()) + 1
            df = df[df['month'] == month]

        # Filter by day of week if applicable
        if day.lower() != 'all':
            df = df[df['day_of_week'] == day.title()]

        return df

    except FileNotFoundError:
        print("File not found for the selected city. Please check the file name.")
        return None

from datetime import datetime

def calculate_statistics(df):
    if df.empty:
        # Return an empty dictionary if the DataFrame is empty
        return {}

    results = {
        "popular times of travel": {
            "most common month": None,
            "most popular day of the week for bike rentals": None,
            "most common hour of day": None,
        },
        "popular stations and trip": {
            "most popular start station": None,
            "most popular end station": None,
            "most common trip from start to end": None,
            "number of unique starting stations": None,
        },
        "trip duration": {
            "average trip duration (in minutes)": None,
            "total travel time (in minutes)": None,
            "longest trip duration recorded (in minutes)": None,
        },
        "user info": {
            "counts of each user type": None,
            "counts of each gender": None,
            "earliest year of birth": None,
            "most recent year of birth": None,
            "most common year of birth": None,
            "median age of users": None,
            "average age of users": None,
        }
    }
    
    # Most common month
    most_common_month = df['month'].mode()[0]
    results["popular times of travel"]["most common month"] = most_common_month
    
    # Most common hour of the day
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    results["popular times of travel"]["most common hour of day"] = most_common_hour
    
    # Find the most popular day of the week for bike rentals
    most_popular_day = df['day_of_week'].mode()[0]
    results["popular times of travel"]["most popular day of the week for bike rentals"] = most_popular_day
    
    # Find the most popular starting station among users
    most_popular_start_station = df['Start Station'].mode()[0]
    results["popular stations and trip"]["most popular start station"] = most_popular_start_station
    
    # Find the most popular ending station among users
    most_popular_end_station = df['End Station'].mode()[0]
    results["popular stations and trip"]["most popular end station"] = most_popular_end_station
    
    # Find the most common trip from start to end
    most_common_trip = df['Start Station'] + " to " + df['End Station']
    most_common_trip = most_common_trip.mode()[0]
    results["popular stations and trip"]["most common trip from start to end"] = most_common_trip
    
    # Count the number of unique starting stations
    unique_starting_stations = df['Start Station'].nunique()
    results["popular stations and trip"]["number of unique starting stations"] = unique_starting_stations
    
    # Calculate the average trip duration in minutes
    avg_trip_duration_minutes = df['Trip Duration'].mean() / 60
    results["trip duration"]["average trip duration (in minutes)"] = round(avg_trip_duration_minutes, 2)
    
    # Calculate the total travel time in minutes
    total_travel_time_minutes = df['Trip Duration'].sum() / 60
    results["trip duration"]["total travel time (in minutes)"] = round(total_travel_time_minutes, 2)
    
    # Find the longest trip duration in minutes
    longest_trip_duration_minutes = df['Trip Duration'].max() / 60
    results["trip duration"]["longest trip duration recorded (in minutes)"] = round(longest_trip_duration_minutes, 2)
    
    # Check if 'User Type' column exists in the DataFrame
    if 'User Type' in df.columns:
        # Counts of each user type
        user_type_counts = df['User Type'].value_counts().to_dict()
        results["user info"]["counts of each user type"] = user_type_counts
    
    # Check if 'Gender' column exists in the DataFrame
    if 'Gender' in df.columns:
        # Counts of each gender
        gender_counts = df['Gender'].value_counts().to_dict()
        results["user info"]["counts of each gender"] = gender_counts
    
    # Check if 'Birth Year' column exists in the DataFrame
    if 'Birth Year' in df.columns:
        # Get the earliest year of birth
        earliest_birth_year = df['Birth Year'].min()
        results["user info"]["earliest year of birth"] = int(earliest_birth_year)
        
        # Get the most recent year of birth
        most_recent_birth_year = df['Birth Year'].max()
        results["user info"]["most recent year of birth"] = int(most_recent_birth_year)
        
        # Get the most common year of birth
        most_common_birth_year = df['Birth Year'].mode()[0]
        results["user info"]["most common year of birth"] = int(most_common_birth_year)
        
        # Calculate the median age of users
        current_year = datetime.now().year
        df['Age'] = current_year - df['Birth Year']
        median_age = df['Age'].median()
        results["user info"]["median age of users"] = int(median_age)
        
        # Calculate the average age of users
        average_age = df['Age'].mean()
        results["user info"]["average age of users"] = round(average_age, 2)
    
    return results

def display_raw_data(df):
    start_idx = 0
    while True:
        raw_data_request = input("\nWould you like to see 5 more lines of raw data? Enter 'yes' or 'no': ").lower()
        if raw_data_request == 'yes':
            print(df.iloc[start_idx:start_idx + 5])
            start_idx += 5
        elif raw_data_request == 'no':
            break

def main():
    print("Hello there\n I am Isaac\n Let's explore US Bikeshare Data together\n")

    while True:
        city = input("Enter the city name (Chicago, New York City, Washington): ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please choose from Chicago, New York City, or Washington.\n")

    while True:
        month = input("Enter the month (January, February, March, April, May, June) or 'all' for all months: ").lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print("Invalid month. Please enter a valid month or 'all' for all months.\n")

    while True:
        day = input("Enter the day of the week (e.g., Monday, Tuesday, ...) or 'all' for all days: ").lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print("Invalid day. Please enter a valid day or 'all' for all days.\n")

    # Load and filter data
    df = load_data(city, month, day)

    if df is not None:
        statistics = calculate_statistics(df)
        if statistics:  # Check if statistics is not empty
            for group, group_stats in statistics.items():
                print('\n')
                print(group.upper())
                for key, value in group_stats.items():
                    print(f"{key}: {value}")
        else:
            print("No data available for the selected filters.")

        display_raw_data(df)

        print("\nTHANK YOU")
        print("\nProject by: Isaac Muturi")

if __name__ == "__main__":
    main()
