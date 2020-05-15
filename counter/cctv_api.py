# import libraries
import pandas as pd
import json
from flask import Flask
import cctv_prep as prep

# create a Flask app
app = Flask(__name__)

df = pd.read_csv('./report.csv')
df = prep.clean_report(df)

# ------- Flask routes to serve HTTP traffic -------------

#endpoint to the initial page of the api
@app.route('/')
def hello_world():
    return 'work on progress... :)'

# endpoint to get all data
@app.route('/counts/')
def get_all_data():
    all_data = df.head().to_dict('index')# delete head
    
    #default=str since timestp not serializable
    return json.dumps(all_data, default=str) 

# endpoint to get all counts per location
@app.route('/counts/<location>')
def get_data_by_location(location):
    if location not in df['location'].unique():
        return 'Error: location does not exist'
    data_by_location = df[df['location']==location]
    data_by_location = data_by_location.head().to_dict('index') # delete head
    
    return json.dumps(data_by_location, default=str) 

# endpoint to get all counts per time interval
@app.route('/counts/<first_date>/<last_date>')
def get_all_data_by_time_interval(first_date, last_date):
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
@app.route('/counts/<location>/<first_date>/<last_date>')
def get_data_by_location_time_interval(location, first_date, last_date):
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

# run the app with the debug mode as True
if __name__ == '__main__':
    app.run(debug=True)
