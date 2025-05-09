# EPA Data Directory Documentation

## Directory Structure

- **EPAplantdata.xlsx**: Original EPA data with all detailed plant data.
- **Ordered_Updated_EPAplantdata.xlsx**: Updated EPA data with extra five columns from substation data:
  1. Substation id
  2. Substation name
  3. Substation latitude
  4. Substation longitude
  5. Interconnect (used for BreakThrough Energy, specifically using Eastern)
- **filtered_power_plants_and_communities.xlsx**: Filtered EPA data with only power plants under MISO region:
- **BEvsEPA energy check .xlsx**: Sheet for checking total amount of all types of energy generation are the same for EPA vs BreakThrough Energy
  
- **sub_map_EPAplant.py**: Mapping Converter for EPA plant data to add the five columns. This script utilizes:
  1. Ball Tree Algorithm and KDTree concept of multidimensional partitioning
  2. Organizing & Searching
  3. Finding the nearest neighbor
  4. Splitting & sorting in the dimensions of longitude and latitude
  5. Goal: Treat substation as one node and classify all EPA plants near that node to place under each substation

## File Descriptions

### EPAplantdata.xlsx
This file contains the original data provided by the EPA. It includes comprehensive details about various plants. This data serves as the base for subsequent updates and mapping processes.

### Ordered_Updated_EPAplantdata.xlsx
This updated version of the EPA data includes five additional columns derived from substation data:
1. **Substation id**: Identifier for each substation.
2. **Substation name**: Name of the substation.
3. **Substation latitude**: Latitude coordinate of the substation.
4. **Substation longitude**: Longitude coordinate of the substation.
5. **Interconnect**: Specifies the interconnect region, particularly focusing on the Eastern region for BreakThrough Energy purposes.

### sub_map_EPAplant.py
The script `sub_map_EPAplant.py` is designed to enhance the original EPA data by mapping each plant to the nearest substation. This is accomplished through advanced algorithms and techniques:
1. **Ball Tree Algorithm and KDTree**: These data structures are used for efficient multidimensional partitioning and nearest neighbor searches.
2. **Organizing & Searching**: The script systematically organizes and searches the data to identify relationships.
3. **Nearest Neighbor**: It identifies the nearest substation for each plant.
4. **Splitting & Sorting**: The script splits and sorts the data based on longitude and latitude coordinates.
5. **Goal**: To treat each substation as a node and classify all nearby EPA plants to be associated with that substation.
