import cfgrib

from scipy.spatial.distance import cdist


class HyperCube:

    def __init__(self, dataset):
        self.dataset = dataset
        self.vars = None
        self.points = None

    def list_vars(self):
        if self.vars is None:
            self.vars = []
            for dv in self.dataset.data_vars:
                the_var = {
                    'name': dv,
                    'grib_name': self.dataset.data_vars[dv].attrs['GRIB_cfVarName'],
                    'long_name': self.dataset.data_vars[dv].attrs['long_name'],
                    'units': self.dataset.data_vars[dv].attrs['units'],
                    'param_id': self.dataset.data_vars[dv].attrs['GRIB_paramId'],
                    'dims_count': len(self.dataset.data_vars[dv].dims)
                }
                if the_var["param_id"]:
                    self.vars.append(the_var)

        return self.vars

    def get_points(self):
        if self.points is None:
            hc_vars = self.list_vars()
            the_var =hc_vars[0]
            df = self.dataset.data_vars[the_var["name"]].to_dataframe()
            points = [(x, y) for x, y in zip(df['longitude'], df['latitude'])]
            self.points = list(points)

        return self.points

    def get_point(self, idx):
        points = self.get_points()
        return points[idx]

    def get_var(self, var_name):
        hc_vars = self.list_vars()
        for the_var in hc_vars:
            if the_var["name"] == var_name:
                return the_var
        return None

    def find_nearest_point_idx(self, lon, lat):
        points = self.get_points()
        point = [lon, lat]
        idx = cdist([point], points).argmin()
        return idx

    def get_var_at_point(self, var_name, lon, lat):
        idx = self.get_point_idx(lon, lat)
        return self.get_var_at_idx(var_name, idx)

    def get_point_idx(self, lon, lat):
        idx = self.find_nearest_point_idx(lon, lat)
        points = self.get_points()
        return idx

    def get_var_at_idx(self, var_name, idx):
        the_var = self.get_var(var_name)
        var_df = self.dataset.data_vars[var_name].to_dataframe()

        if the_var["dims_count"] == 2:
            var_list = [x for x in var_df[var_name]]

        if the_var["dims_count"] == 3:
            dim_first = self.dataset.data_vars[var_name].dims[0]
            dim_values = self.dataset.coords[dim_first].values
            dim_0 = dim_values[0]
            var_list = [x for x in var_df[var_name][dim_0]]

        return var_list[idx]