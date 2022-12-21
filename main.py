import os

from dotenv import load_dotenv
from gribreader import GRIBReader

load_dotenv()

reader = GRIBReader(os.getenv("SOURCE_GRIB2_FILE"))
reader.run(os.getenv("SOURCE_CSV_FILE"), os.getenv("DESTINATION_CSV_FILE"))
