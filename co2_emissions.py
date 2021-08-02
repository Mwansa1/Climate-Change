import datapackage
import pandas as pd
import matplotlib.pyplot as plt


data_url = 'https://datahub.io/core/co2-ppm/datapackage.json'

# to load Data Package into storage
package = datapackage.Package(data_url)

# to load only tabular data
resources = package.resources

def get_info_to_df(sources):
    data = None
    for resource in sources:
        if resource.tabular:
            data = pd.read_csv(resource.descriptor['path'])
    return data


def make_save_bar_chart(x_col, y_col, title, df):
    ax = df.plot.bar(x=x_col, y=y_col, title=title)
    fig = ax.get_figure()
    fig.savefig('static/barchart.png')
    
    
data = get_info_to_df(resources)
make_save_bar_chart('Year', 'Annual Increase', 'Yearly Atmospheric Carbon Dioxide Rates',data)