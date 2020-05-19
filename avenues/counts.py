# import libraries
import pandas as pd
import json
from flask import (
    Blueprint, render_template, url_for
)
from avenues.df import get_df

bp = Blueprint('counts', __name__)

# ------- Flask routes to serve HTTP traffic -------------

#endpoint to the initial page of the api
@bp.route('/')
def index():
    df = get_df()
    locations = df.location.unique()
    return render_template('index.html', locations=locations)

# endpoint to get all data
@bp.route('/counts/')
def get_all_data():
    all_data = get_df().head().to_dict('index')# delete head
    
    #default=str since timestp not serializable
    return json.dumps(all_data, default=str) 

# endpoint to get all counts per location
@bp.route('/counts/<location>')
def get_data_by_location(location):
    df = get_df()
    if location not in df['location'].unique():
        return 'Error: location does not exist'
    data_by_location = df[df['location']==location]
    data_by_location = data_by_location.head().to_dict('index') # delete head
    
    return json.dumps(data_by_location, default=str) 

# endpoint to get all counts per time interval
@bp.route('/counts/<first_date>/<last_date>')
def get_all_data_by_time_interval(first_date, last_date):
    df = get_df()
    fst_date = pd.to_datetime(first_date)
    lst_date = pd.to_datetime(last_date)
    if fst_date > lst_date:
        return 'Error: left side date more recent than right side date'
    # add one day because dates are converted to "date 00:00:00"
    lst_date = lst_date + pd.Timedelta('1 days')
    all_data_filtered = df[df['timestp_UTC'] >= fst_date]
    all_data_filtered = all_data_filtered[all_data_filtered['timestp_UTC']\
            < lst_date]
    all_data_filtered = all_data_filtered.to_dict('index')
    
    return json.dumps(all_data_filtered, default=str) 

# endpoint to get counts per location and time interval
@bp.route('/counts/<location>/<first_date>/<last_date>')
def get_data_by_location_time_interval(location, first_date, last_date):
    df = get_df()
    if location not in df['location'].unique():
        return 'Error: location does not exist'
    data_by_location = df[df['location']==location]
    fst_date = pd.to_datetime(first_date)
    lst_date = pd.to_datetime(last_date)
    if fst_date > lst_date:
        return 'Error: left side date more recent than right side date'
    # add one day because dates are converted to "date 00:00:00"
    lst_date = lst_date + pd.Timedelta('1 days')
    data_by_location_filtered = \
            data_by_location[data_by_location['timestp_UTC'] >= fst_date]
    data_by_location_filtered = \
            data_by_location_filtered[data_by_location_filtered['timestp_UTC']\
            < lst_date]
    data_by_location_filtered = data_by_location_filtered.to_dict('index')
    
    return json.dumps(data_by_location_filtered, default=str) 
