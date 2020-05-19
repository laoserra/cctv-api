# import libraries
import pandas as pd
from flask import current_app

def clean_report(dataframe):
    # creating timestamp field
    dataframe['timestp_UTC'] = dataframe['image'].str[0:13]
    dataframe['timestp_UTC'] = pd.to_datetime(dataframe['timestp_UTC'], unit='ms')
    # creating new field with camera's location
    dataframe['location'] = dataframe['image'].str[14:17]
    dataframe = dataframe.replace({
        'A03': 'Argyle_St_@_Oswald_St(static)',
        'A47': 'Argyle_St_@_Oswald_St',
        'A66': 'Sauchiehall_St_@_Pitt_St',
        'A82': 'Argyle_St_@_Brown_St'
    })

    # dropping useless fields
    dataframe.drop(['timestamp', 'image'], axis=1, inplace=True)

    # swap fields' position
    dataframe = dataframe[['timestp_UTC','location','car','person', \
            'bicycle','motorcycle','bus','truck']]

    return dataframe


def get_df():
    df = pd.read_csv(current_app.config['CSVFILE'])
    df = clean_report(df)

    return df
