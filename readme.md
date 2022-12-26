# GRIB2 API Toolset

Toolset lib to extract variables data from the GRIB2 meteo model  

## Installation

bz2 system lib:

`apt-get install libbz2-dev`

python dependencies

`python -m pip install -r requirements.txt`

## Settings

Settings are in system environment. (You can use .env file for development purposes)

`SOURCE_GRIB2_FILE`= path to the source GRIB2 file

`SOURCE_CSV_FILE`= path to the .CSV file with locations which should be pulled

`DESTINATION_CSV_FILE`= path to the destination .CSV file where data will be exported

## Usage

To run script use command:

`python main.py SOURCE_GRIB2_FILE SOURCE_CSV_FILE`

If command line arguments for source files are omitted the values from the system ENVs will be used

Default location for result file is `result.csv` but it may be overriden by system ENVs

## Result structure

Result is .csv files with the variables values in the points, which are the closest to the points given in request.

Coordinates of mentioned above "closest points" are also provided as `real_lon` and `real_lat`