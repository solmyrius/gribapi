import os
import sys

from dotenv import load_dotenv
from gribreader import GRIBReader

load_dotenv()


if __name__ == "__main__":
    src_grib = None
    src_csv = None
    dst_csv = os.getenv("DESTINATION_CSV_FILE", 'result.csv')

    if len(sys.argv) >= 3:
        src_grib = sys.argv[1]
        src_csv = sys.argv[2]

    if src_grib is None:
        src_grib = os.getenv("SOURCE_GRIB2_FILE")

    if src_csv is None:
        src_csv = os.getenv("SOURCE_CSV_FILE")

    reader = GRIBReader(src_grib)
    reader.run(src_csv, dst_csv)
