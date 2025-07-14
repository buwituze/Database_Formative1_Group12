import requests
import joblib
import pandas as pd

# Step 1: Call your API and get latest data
API_URL = "http://localhost:8000/salary-records/latest"  # change if your API runs somewhere else

def fetch_latest_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch data from API.")

# Step 2: Load your trained ML model 
def load_model():
    return joblib.load('model.pkl')

# Step 3: Prepare the data to feed into your model
def prepare_data(data):
    # Map API response keys to model feature names (with spaces)
    data_corrected = {
        'Age': data['Age'],
        'Gender': data['Gender'],
        'Education Level': data['Education_Level'],      # underscore -> space
        'Years of Experience': data['Years_of_Experience']  # underscore -> space
    }

    features = ['Age', 'Gender', 'Education Level', 'Years of Experience']
    df = pd.DataFrame([data_corrected])[features]

    # Preprocessing to match what the model expects
    df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1}).fillna(0)
    edu_map = {'High School': 0, 'Bachelor': 1, 'Master': 2, 'PhD': 3}
    df['Education Level'] = df['Education Level'].map(edu_map).fillna(0)

    return df

# Step 4: Predict salary using the model and prepared data
def predict_salary(model, df):
    prediction = model.predict(df)
    return prediction[0]

def main():
    latest_data = fetch_latest_data()
    print("Latest data from API:", latest_data)

    model = load_model()

    input_df = prepare_data(latest_data)
    print("Prepared data for model:\n", input_df)

    predicted_salary = predict_salary(model, input_df)
    print(f"Predicted Salary: {predicted_salary}")

if __name__ == "__main__":
    main()
