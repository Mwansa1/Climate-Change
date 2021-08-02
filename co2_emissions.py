import datapackage
import pandas as pd
import matplotlib.pyplot as plt

data_url = 'https://datahub.io/core/co2-ppm/datapackage.json'

# to load Data Package into storage
package = datapackage.Package(data_url)

# to load only tabular data
resources = package.resources

x_col = 'Year'
y_col = 'Annual Increase'
title = 'Yearly Atmospheric Carbon Dioxide Rates'

def get_info_to_df(sources):
    data = None
    for resource in sources:
        if resource.tabular:
            data = pd.read_csv(resource.descriptor['path'])
    return data


def make_save_barchart():
    df = get_info_to_df(resources)
    ax = df.plot.bar(x=x_col, y=y_col, title=title)
    fig = ax.get_figure()
    fig.savefig('static/barchart.png')

