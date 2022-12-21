import sys
import numpy as np
import cfgrib
import json
import csv
import os

from hypercube import HyperCube

typesOfLevel = [
    'meanSea',
    'hybrid',
    'atmosphereSingleLayer',
    'surface',
    'isobaricInhPa',
    'heightAboveGround',
    'depthBelowLandLayer',
    'lowCloudLayer',
    'middleCloudLayer',
    'highCloudLayer'
]


class GRIBReader:

    def __init__(self, grib_file):

        self.grib_file = grib_file
        self.datasets = None
        self.request_csv = []
        self.result_csv = []
        self.load()

    def load(self):

        self.datasets = []

        devnull = open(os.devnull, "w")
        old_stderr = sys.stderr
        sys.stderr = devnull

        ds = cfgrib.open_datasets(
            self.grib_file,
            errors="ignore",
            backend_kwargs={"errors": "ignore"}
        )

        sys.stderr = old_stderr

        for data in ds:
            hc = HyperCube(data)
            self.datasets.append(hc)

    def load_csv(self, csv_name):
        with open(csv_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            head_row = None
            for row in csv_reader:
                if head_row is None:
                    head_row = row
                else:
                    if len(row) > 0:
                        csv_row = {}
                        for i in range(len(row)):
                            csv_row[head_row[i]] = row[i]
                        self.request_csv.append(csv_row)

    def build_result(self):
        self.result_csv = self.request_csv.copy()
        for row in self.result_csv:
            print(row["city"], flush=True)
            data_vars = self.get_vars(float(row["lng"]), float(row["lat"]))
            for key in data_vars:
                row[key] = data_vars[key]

    def save_csv(self, csv_name):
        head_row = self.result_csv[0].keys()
        with open(csv_name, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=head_row)
            writer.writeheader()
            for row in self.result_csv:
                writer.writerow(row)

    def get_var_names(self):
        data_vars = []
        for hc in self.datasets:
            hc_vars = hc.list_vars()
            data_vars.extend(hc_vars)

        return data_vars

    def get_vars(self, lon, lat):
        data = {}

        devnull = open(os.devnull, "w")
        old_stderr = sys.stderr
        sys.stderr = devnull

        for hc in self.datasets:
            idx = hc.get_point_idx(lon, lat)
            hc_vars = hc.list_vars()
            if "real_lon" not in data:
                point = hc.get_point(idx)
                data["real_lat"] = point[1]
                data["real_lon"] = point[0]
            for the_var in hc_vars:
                x = hc.get_var_at_idx(the_var["name"], idx)
                data[the_var["name"]] = x

        sys.stderr = old_stderr

        return data

    def run(self, csv_src, csv_dst):
        self.load_csv(csv_src)
        self.build_result()
        self.save_csv(csv_dst)
