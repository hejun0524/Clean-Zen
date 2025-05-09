import pandas as pd
from geopy.distance import geodesic

def read_csv_file(path):
    try:
        print(f"Attempting to read file: {path}")
        df = pd.read_csv(path, encoding='utf-8')
        print(f"Successfully read {path}")
        print(f"Columns in {path}: {df.columns.tolist()}")
        return df
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(path, encoding='ISO-8859-1')
            print(f"Successfully read {path}")
            print(f"Columns in {path}: {df.columns.tolist()}")
            return df
        except Exception as e:
            print(f"Failed to read {path}: {e}")
            return None

# Define file paths for the 15 CSV files
file_paths = {
    'Arkansas': 'Arkansas_Counties_with_Coordinates.csv',
    'Illinois': 'Illinois_Counties_with_Coordinates.csv',
    'Indiana': 'Indiana_Counties_with_Coordinates.csv',
    'Iowa': 'Iowa_Counties_with_Coordinates.csv',
    'Kentucky': 'Kentucky_Counties_with_Coordinates.csv',
    'Louisiana': 'Louisiana_Counties_with_Coordinates.csv',
    'Michigan': 'Michigan_Counties_with_Coordinates.csv',
    'Minnesota': 'Minnesota_Counties_with_Coordinates.csv',
    'Mississippi': 'Mississippi_Counties_with_Coordinates.csv',
    'Missouri': 'Missouri_Counties_with_Coordinates.csv',
    'Montana': 'Montana_Counties_with_Coordinates.csv',
    'North Dakota': 'North_Dakota_Counties_with_Coordinates.csv',
    'South Dakota': 'South_Dakota_Counties_with_Coordinates.csv',
    'Texas': 'Texas_Counties_with_Coordinates.csv',
    'Wisconsin': 'Wisconsin_Counties_with_Coordinates.csv'
}

# Load all the state-specific CSV files into a dictionary
all_counties_data = {}
for state, path in file_paths.items():
    county_df = read_csv_file(path)
    if county_df is not None:
        if 'County' in county_df.columns:
            all_counties_data[state] = county_df
        else:
            print(f"Skipping {path} due to missing 'County' column")
    else:
        print(f"Skipping {path} due to read error")

if not all_counties_data:
    raise Exception("No county data files could be read")

# Load the sub.csv file
sub_file_path = 'sub.csv'
sub_df = read_csv_file(sub_file_path)

if sub_df is None:
    raise Exception("Failed to read sub.csv")

# Initialize columns for mapped state and county
sub_df['Mapped_State'] = ''
sub_df['Mapped_County'] = ''

# Tolerance level for coordinate matching (in degrees)
tolerance = 0.05

# Function to find the closest county for given lat and lon
def find_county_and_state(lat, lon):
    for state, county_df in all_counties_data.items():
        possible_counties = county_df[(county_df['Longitude'] <= lon + tolerance) & (county_df['Longitude'] >= lon - tolerance)]
        if not possible_counties.empty:
            matched_county = possible_counties[(possible_counties['Latitude'] <= lat + tolerance) & (possible_counties['Latitude'] >= lat - tolerance)]
            if not matched_county.empty:
                return state, matched_county.iloc[0]['County']
    return None, None

# Map each substation to the closest county
for idx, row in sub_df.iterrows():
    lat = row['lat']
    lon = row['lon']
    state, county = find_county_and_state(lat, lon)
    sub_df.at[idx, 'Mapped_State'] = state
    sub_df.at[idx, 'Mapped_County'] = county

# Save the updated sub.csv file
output_file_path = 'updated_sub.csv'
sub_df.to_csv(output_file_path, index=False)

print("The updated sub.csv file has been saved.")