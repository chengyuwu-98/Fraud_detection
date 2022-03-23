import os
import requests
import numpy as np
import pandas as pd

my_data = {
        "type": {0: "TRANSFER"},
        "amount": {0: 10000000.0},
        "oldbalanceOrg": {0: 0.0 },
        "newbalanceOrig": {0: 0.0},
        "oldbalanceDest": {0: 0.0},
        "newbalanceDest": {0: 0.0},
    }
df = pd.DataFrame(data=my_data)


def create_tf_serving_json(data):
  return {'inputs': {name: data[name].tolist() for name in data.keys()} if isinstance(data, dict) else data.tolist()}

def score_model(dataset):
  url = 'https://adb-8196151818591343.3.azuredatabricks.net/model/fraud_detection_new/1/invocations'
  headers = {'Authorization': f'Bearer {os.environ.get("DATABRICKS_TOKEN")}'}
  data_json = dataset.to_dict(orient='split') if isinstance(dataset, pd.DataFrame) else create_tf_serving_json(dataset)
  response = requests.request(method='POST', headers=headers, url=url, json=data_json)
  if response.status_code != 200:
    raise Exception(f'Request failed with status {response.status_code}, {response.text}')
  return response.json()

if __name__ == "__main__":
    print(score_model(df))