# IMPORTS

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

app = Flask(__name__)

#Create Routes
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/names")
def sample_names():
    results = session.query(samples_meta.SAMPLEID).all()
    results = ['BB_' + str(name[0]) for name in results]

    return jsonify(results)

@app.route("/otu")
def otu_description():
    results = session.query(otu.lowest_taxonomic_unit_found).all()
    results = [str(result[0]) for result in results]
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

@app.route('/samples/<sample>')
def get_samples(sample):
    results = session.query(samples.otu_id, getattr(samples, sample)).order_by(getattr(samples, sample).desc())
    otu_ids = []
    sample_values = []

    for item, value in results:
        otu_ids.append(item)
        sample_values.append(value)

    results_dict = {"otu_ids": otu_ids, "sample_values": sample_values}
    return jsonify(results_dict)


if __name__ == "__main__":
    app.run(debug=False)