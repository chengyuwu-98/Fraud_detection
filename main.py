from fastapi import FastAPI
import uvicorn
import mlflow
import pandas as pd
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

class Story(BaseModel):
    type: str
    amount: float
    oldbalanceOrg: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float

def predict(Story):
    print(f"Accepted payload: {Story.type,Story.amount,Story.oldbalanceOrg,Story.oldbalanceDest,Story.newbalanceDest}")
    my_data = {
        "type": {0: Story.type},
        "amount": {0: Story.amount},
        "oldbalanceOrg": {0: Story.oldbalanceOrg},
        "newbalanceOrig": {0: Story.newbalanceOrig},
        "oldbalanceDest": {0: Story.oldbalanceDest},
        "newbalanceDest": {0: Story.newbalanceDest},
    }
    data = pd.DataFrame(data=my_data)
    result = loaded_model.predict(pd.DataFrame(data))
    return result


# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model('model')
app = FastAPI()

@app.post("/predict")
async def predict_story(story: Story):
    print(f"predict_story accepted json payload: {story}")
    result = predict(story)
    print(f"The result is the following payload: {result}")
    payload = {"IsFraudTrueFalse": result.tolist()[0]}
    json_compatible_item_data = jsonable_encoder(payload)
    return JSONResponse(content=json_compatible_item_data)

@app.get("/")
async def root():
    return {"message": "Welcome to use the Fraud Detection application"}




if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')