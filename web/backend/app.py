from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
from journal_nlp import extract_features_from_journal  # from earlier code

# Load model + encoders
model = joblib.load(r"D:\capstone project\model\mental_health_model.pkl")
le_gender = joblib.load(r"D:\capstone project\model\gender_encoder.pkl")
le_state = joblib.load(r"D:\capstone project\model\state_encoder.pkl")

app = FastAPI()

# Allow frontend JS to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JournalInput(BaseModel):
    age: int
    gender: str
    journal: str

@app.post("/predict")
def predict(input: JournalInput):
    features = extract_features_from_journal(input.journal)
    gender_encoded = le_gender.transform([input.gender])[0]

    input_data = {
        "age": input.age,
        "gender": gender_encoded,
        **features
    }

    df_input = pd.DataFrame([input_data])
    pred = model.predict(df_input)[0]
    proba = model.predict_proba(df_input).max()

    mental_state = le_state.inverse_transform([pred])[0]

    return {
        "mental_state": mental_state,
        "confidence": round(proba * 100, 2),
        "features": features
    }
