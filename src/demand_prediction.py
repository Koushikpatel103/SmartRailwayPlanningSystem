import pickle
import pandas as pd

def load_model():

    model = pickle.load(open("models/demand_model.pkl", "rb"))
    return model


def predict_passengers(day, month, holiday):

    model = load_model()

    input_data = pd.DataFrame({
        "Day":[day],
        "Month":[month],
        "Holiday":[holiday]
    })

    prediction = model.predict(input_data)

    return int(prediction[0])