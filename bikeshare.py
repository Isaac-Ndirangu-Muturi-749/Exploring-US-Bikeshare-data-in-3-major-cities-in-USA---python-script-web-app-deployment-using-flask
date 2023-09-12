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

def calculate_statistics(df):
    # Calculate the average trip duration in seconds
    avg_trip_duration_seconds = df['Trip Duration'].mean()
    # Convert the average trip duration from seconds to minutes
    avg_trip_duration_minutes = avg_trip_duration_seconds / 60
    # Find the most popular starting station among users
    most_popular_start_station = df['Start Station'].mode()[0]
    # Find the most popular ending station among users
    most_popular_end_station = df['End Station'].mode()[0]
    # Calculate the total travel time in seconds
    total_travel_time_seconds = df['Trip Duration'].sum()
    # Convert the total travel time from seconds to minutes
    total_travel_time_minutes = total_travel_time_seconds / 60
    # Check if 'Birth Year' column exists in the DataFrame
    if 'Birth Year' in df.columns:
        # Get the current year
        current_year = datetime.now().year
        # Calculate the age of users based on their birth year
        df['Age'] = current_year - df['Birth Year']
        # Calculate the median age of users
        median_age = df['Age'].median()
        # Calculate the average age of users
        average_age = df['Age'].mean()
    # Find the most popular day of the week for bike rentals
    most_popular_day = df['day_of_week'].mode()[0]
    # Find the longest trip duration in seconds
    longest_trip_duration_seconds = df['Trip Duration'].max()
    # Convert the longest trip duration from seconds to minutes
    longest_trip_duration_minutes = longest_trip_duration_seconds / 60
    # Count the number of unique starting stations
    unique_starting_stations = df['Start Station'].nunique()

    return {"\nAverage trip duration (in minutes)": round(avg_trip_duration_minutes, 2), "\nMost popular start station": most_popular_start_station, "\nMost popular end station": most_popular_end_station, "\nTotal travel time (in minutes)": round(total_travel_time_minutes, 2), "\nMedian age of users": int(median_age) if 'Birth Year' in df.columns else None, "\nAverage age of users": round(average_age, 2) if 'Birth Year' in df.columns else None, "\nMost popular day of the week for bike rentals": most_popular_day, "\nLongest trip duration recorded (in minutes)": round(longest_trip_duration_minutes, 2), "\nNumber of unique starting stations": unique_starting_stations}

def display_raw_data(df):
    start_idx = 0
    while True:
        raw_data_request = input("\nWould you like to see 5 lines of raw data? Enter 'yes' or 'no': ").lower()
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
        month = input("Enter the month (January, February ,march, april, may, june) or 'all' for all months: ").lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print("Invalid month. Please enter a valid month or 'all' for all months.\n")

    while True:
        day = input("Enter the day of the week (e.g., Monday, Tuesday ...) or 'all' for all days: ").lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print("Invalid day. Please enter a valid day or 'all' for all days.\n")

    # Load and filter data
    df = load_data(city, month, day)

    if df is not None:
        statistics = calculate_statistics(df)
        for key, value in statistics.items():
            print(f"{key}: {value}")

        display_raw_data(df)

        print("\nTHANK YOU")
        print("\nProject by: Isaac Muturi")

if __name__ == "__main__":
    main()
