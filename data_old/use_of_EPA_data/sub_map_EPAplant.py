import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Load data
substations_df = pd.read_csv('sub.csv')
epa_plant_df = pd.read_excel('EPAplantdata_without_description_row.xlsx')

# Filter relevant columns from substations_df
substations_df = substations_df[['sub_id', 'name', 'lat', 'lon', 'interconnect']]

# Drop rows with NaN values in the coordinates columns in EPA plant data
epa_plant_df = epa_plant_df.dropna(subset=['LAT', 'LON'])

# Extract coordinates
substation_coords = substations_df[['lat', 'lon']].values
plant_coords = epa_plant_df[['LAT', 'LON']].values

# Perform nearest neighbor search
nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(substation_coords)
distances, indices = nbrs.kneighbors(plant_coords)

# Map the nearest substation information to each power plant
epa_plant_df['nearest_substation_index'] = indices.flatten()
epa_plant_df = epa_plant_df.merge(substations_df, left_on='nearest_substation_index', right_index=True, suffixes=('', '_sub'))

# Drop the temporary index column
epa_plant_df = epa_plant_df.drop(columns=['nearest_substation_index'])

# Reorder columns to place the new substation columns after the third column of EPA plant data
cols = epa_plant_df.columns.tolist()
# Original EPA plant columns
original_cols = cols[:3]
# New substation columns explicitly named
substation_cols = ['sub_id', 'name', 'lat', 'lon', 'interconnect']
# Remaining EPA plant columns
remaining_cols = cols[3:-5]

# New column order
new_column_order = original_cols + substation_cols + remaining_cols
epa_plant_df = epa_plant_df[new_column_order]

# Save the updated EPA plant data to a new Excel file with the correct column order
updated_file_ordered_path = 'Ordered_Updated_EPAplantdata.xlsx'
epa_plant_df.to_excel(updated_file_ordered_path, index=False)

# updated_file_ordered_path