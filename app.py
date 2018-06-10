# IMPORTS
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import (Flask, render_template, request, redirect, jsonify)


#Initiate Database
engine = create_engine('sqlite:///DataSets/belly_button_biodiversity.sqlite')

Base = automap_base()

Base.prepare(engine, reflect=True)

otu = Base.classes.otu
samples = Base.classes.samples
samples_meta = Base.classes.samples_metadata

session = Session(engine)

samples_df = pd.read_sql_table('samples', engine)
otu_df = pd.read_sql_table('otu', engine)

app = Flask(__name__)

#Create Routes
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/names")
def sample_names():
    results = session.query(samples_meta.SAMPLEID).all()
    results = ['BD_' + str(id[0] for id in results)]

    return jsonify(results)

@app.route("/otu")
def otu_description():
    results = session.query(otu.lowest_taxonomi_unit_found).all()
    results = [str(results[0]) for result in results]
    return jsonify(results)

@app.route("/metadata/<sample>")
def get_meta_sample(sample):
    query = [
        samples_meta.AGE,
        samples_meta.BBTYPE,
        samples_meta.ETHNICITY,
        samples_meta.GENDER,
        samples_meta.LOCATION,
        samples_meta.SAMPLEID
    ]
    sample_id = sample[3:]
    results = session.query(*query).filter(samples_meta.SAMPLEID == sample_id).all()
    results = results[0]
    result = {}
    result['AGE'] = results[0]
    result['BBTYPE'] = results[1]
    result['ETHNICITY'] = results[2]
    result['GENDER'] = results[3]
    result['LOCATION'] = results[4]
    result['SAMPLEID'] = results[5]

    return jsonify(result)

@app.route('/wfreq/<sample>')
def get_wfreq(sample):
    sample_id = sample[3:]
    query = samples_meta.WFREQ
    results = session.query(query).filter(samples_meta.SAMPLEID == sample_id).all()
    
    try:
        return jsonify(results[0][0])
    except:
        return 'not found'

@app.route('/otu_desc')
def get_otu_desc():
    otus_df = otu_df.copy(deep=True)
    otus_df['otu_id']  = otus_df['otu_id'].apply(lambda x: str(x))
    otus_df.set_index('otu_id', inplace=True)
    response = otus_df['lowest_taxonomic_unit_found'].to_dict()
    return jsonify(response)

@app.route('/samples/<sample>')
def get_samples(sample):
    sample_df = samples_df[['otu_id', sample]]
    sample_df = sample_df.sort_values(by=sample, axis=0, ascending=False)

    sample_df['otu_id'] = sample_df['otu_id'].apply(lambda x: str(x))
    sample_df[sample] = df_sample[sample].apply(lambda x: str(x))
    result={}
    for j in df_sample.keys():
        result[j] = list(sample_df[j])
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=False)