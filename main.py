from elasticsearch import Elasticsearch
import flask
from flask import request, jsonify, make_response
import json
import pandas as pd
from flask_cors import CORS


def create_index():
    es.indices.create(index = 'my-index')
    df = pd.read_csv('complaints.csv', low_memory=False)
    # Relabel columns
    pd.set_option('display.max_columns', None)
    df = df.rename(columns={"Date received": "date_received",
                            "Product": "product",
                            "Company": "company",
                            "Complaint ID": "complaint_id",
                            "ZIP code": "zip_code",
                            "State": "state",
                            "Consumer complaint narrative": "complaint_what_happened",
                            "Submitted via": "submitted_via",
                            "Sub-product": "sub_product",
                            "Company public response": "company_response",
                            "Consumer consent provided?": "consent_provided",
                            "Date sent to company": "date_sent",
                            "Company response to consumer": "response_to_consumer",
                            "Timely response?": "timely_response",
                            "Consumer disputed?": "consumer_disputed"})
    
    # Get rid of extraneous columns
    df = df.drop(columns=["consumer_disputed", "Issue", "Sub-issue", "company_response", "Tags", "consent_provided", "date_sent", "response_to_consumer", "timely_response", "consumer_disputed"])

    # Replace nan with empty string
    df = df.fillna('N/A')

    # Drop NaN rows
    df = df[df['complaint_what_happened'].notna()]  
    # Only keep distinct complaint ids
    df = df.drop_duplicates('complaint_id', keep='first')
    # Get sample of 1000 rows
    df = df.sample(n=1000)  

    data = df.to_dict('records')
    for a_data in data:
        es.index(index='my-index', body=a_data)


if __name__ == '__main__':
    es = Elasticsearch("http://localhost:9200")
    app = flask.Flask(__name__)
    CORS(app)
    app.config["DEBUG"] = False

    indices = es.indices.get_alias().keys()

    # es.indices.delete(index='my-index', ignore=[400, 404])

    # Only create the index if it hasn't been already
    if 'my-index' in indices:
        pass
    else:
        create_index()


    @app.route('/', methods=['POST'])
    def home():
        # Read request into dict
        data = json.loads(request.data)

        body = {'query': {'bool': {'must': []}}}
        # Add incoming parameters to query
        for k, v in data.items():
            # Only add entries that are not empty
            if v:
                body['query']['bool']['must'].append({'match': {k: v}})

        # Only search the index if at least one query parameter is specified
        if body['query']['bool']['must']:
            res = dict(es.search(index='my-index', body=body))
        else:
            res = {"error": "No query parameter specified."}

        return make_response(jsonify(res), 200)


    app.run(host='0.0.0.0', port=4999)
