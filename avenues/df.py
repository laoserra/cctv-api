# import libraries
import pandas as pd
from flask import current_app

def clean_report(df):
    # creating timestamp field
    df['timestp_UTC']= df['image'].str.split('_')
    df['timestp_UTC'] = df['timestp_UTC'].apply(lambda x: x[0])
    df['timestp_UTC'] = pd.to_datetime(df['timestp_UTC'], unit='ms')
    # creating new field with camera's location
    df['location'] = df['image'].str.split('_')
    df['location'] = df['location'].apply(lambda x: x[1])
    df = df.replace({
        'A26': 'Broomielaw_@_Washington_St',
        'A27': 'Clyde_walkway_@_McAlpine',
        'A28': 'Broomielaw_@_James_Watt_St_(cam1)',
        'A29': 'Broomielaw_@_James_Watt_St_(cam2)',
        'A30': 'Broomielaw_Rear_of_Casino',
        'A31': 'Clyde_Walkway_@_Dixon_St',
        'A32': 'Clyde_Walkway_@_Jamaica_St',
        'A33': 'Clyde_Walkway_@_Stockwell_St',
        'A03': 'Argyle_St_@_Oswald_St(static)',
        'A47': 'Argyle_St_@_Oswald_St',
        'A66': 'Sauchiehall_St_@_Pitt_St',
        'A82': 'Argyle_St_@_Brown_St',
        'A13':	'Byres_Rd_@_Dowanside_St',
        'A36':	'Gallowgate_@_High_St(cam1)',
        'A47Static': 'Argyle_St_@_Oswald_St(static)',
        'A47static':	'Argyle_St_@_Oswald_St(static)',
        'A52':	'Gordon_St_@_Renfield_St',
        'A71':	'Killermont_St_@_Royal_Concert_Hall',
        'A92':	'Hope_St_@_Waterloo_St',
        'C104':	'Glasgow_Green_Doulton_Fountain',
        'C117':	'Maryhill_Forth_Clyde_Canal',
        'C129':	'Glasgow_Green_Path',
        'C130':	'Glasgow_Green_Circles',
        'C132':	'Glasgow_Green_monument',
        'C133':	'Glasgow_Green_suspension_walkway',
        'C37':	'Maryhill_Rd_@_Shakespeare_St',
        'C79':	'Kelvingrove_Park_fountain',
        'C80':	'Kelvingrove_Park_entrance',
        'C81':	'Kelvingrove_Park_Kelvin_Way',
        'C82':	'Kelvingrove Park_overview',
        'C86':	'Tollcross_Park(cam1)',
        'C90':	'Tollcross_Park(cam2)',
        'C91':	'Bellahouston_Park',
        'E69':	'Duke_St_@_Bellgrove',
        'G124':	'Victoria_Rd_@_Allison_St',
        'T628':	'Gallowgate_@_High_St(cam2)',
        'T63':	'George_Sq_@_South_Hanover_St',
        'T71':	'Argyle_St_@_Jamaica_St'
    })

    # dropping useless fields
    df.drop(['timestamp', 'image'], axis=1, inplace=True)

    # swap fields' position
    df = df[['timestp_UTC','location','car','person', \
            'bicycle','motorcycle','bus','truck']]

    return df


def get_df():
    df = pd.read_csv(current_app.config['CSVFILE'])
    df = clean_report(df)

    return df

def get_cameras_operation(df):
    df['date'] = df['timestp_UTC'].dt.strftime('%Y-%m-%d')
    df = df[['location', 'date']]
    df = df.groupby('location')['date'].agg(['first', 'last']).reset_index()

    return df
