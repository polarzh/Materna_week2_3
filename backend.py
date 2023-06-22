from flask import Flask, jsonify, request, Response, send_file
import pandas as pd
from io import StringIO

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug = True)


@app.route('/add_census_data/', methods = ['POST'])

def add_census_data():
    census_data = request.files[''].stream.read().decode("utf-8")
    # print(census_data)

    global df_census_data
    df_census_data = pd.read_csv(StringIO(census_data))
    print(df_census_data[:3])

    # merge_census_and_states_data()
    return Response(status=200)

@app.route('/add_states_data/', methods = ['POST'])

def add_states_data():
    states_data = request.files[''].stream.read().decode("utf-8")
    global df_states_data
    df_states_data = pd.read_csv(StringIO(states_data), sep = '\t', names = ['Name', 'Lat', 'Lon'])
    # print(df_states_data)
    # merge_census_and_states_data()
    return Response(status=200)

@app.route('/get-state-locations-with-attribute/<attribute>/', methods = ['GET'])

def merge_census_and_states_data(attribute):
    df_merged_census_states = pd.merge( df_states_data, df_census_data)
    if df_census_data.empty() or df_states_data.empty():
        return 'Files werent added to the backend'
    else:
        return send_file(df_merged_census_states[attribute])
