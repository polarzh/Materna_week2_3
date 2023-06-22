from flask import Flask, jsonify, request, Response, send_file
import pandas as pd
from io import StringIO

app = Flask(__name__)



@app.route('/add-census-data/', methods = ['POST'])
def add_census_data():
    census_data = request.files[''].stream.read().decode("utf-8")
    global df_census_data
    df_census_data = pd.read_csv(StringIO(census_data))
    print(df_census_data[:3])

    # merge_census_and_states_data()
    return Response(status=200)

@app.route('/add-states-data/', methods = ['POST'])
def add_states_data():
    states_data = request.files[''].stream.read().decode("utf-8")
    global df_states_data
    df_states_data = pd.read_csv(StringIO(states_data), sep = '\t', names = ['Name', 'Lat', 'Lon'])
    # df_states_data.loc['Name'] =  df_states_data.loc['Name'].split(',', expand = True)[0]
    print(df_states_data)
    # merge_census_and_states_data()
    return Response(status=200)

@app.route('/get-state-locations-with-attribute/<attribute>/', methods = ['GET'])
def merge_census_and_states_data(attribute):
    print(df_states_data, df_census_data)
    print(attribute, type(attribute))

    df_merged_census_states =  df_states_data.merge(df_census_data)
    print(df_merged_census_states)
    if df_census_data.empty() or df_states_data.empty():
        return 'Files werent added to the backend'
    else:
        return send_file(df_merged_census_states[attribute])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
