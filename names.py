import os
import json
from gribreader import GRIBReader
from dotenv import load_dotenv

load_dotenv()

reader = GRIBReader(os.getenv("SOURCE_GRIB2_FILE"))
names = reader.get_var_names()
print(json.dumps(names, indent=4))
