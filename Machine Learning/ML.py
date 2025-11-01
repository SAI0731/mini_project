import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# -------------------------------------------
# 1. Load Dataset
# -------------------------------------------
st.title("⚡ Energy Consumption Forecasting App")

st.write("""
This app predicts **Energy Consumption (kWh)** based on **Temperature** and **Humidity**.
Dataset: *energy_consumption_dataset.csv*
""")

# Load dataset
df = pd.read_csv("energy_consumption_dataset_v2.csv")

# Show dataset
st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

# -------------------------------------------
# 2. Preprocessing and Model Training
# -------------------------------------------
X = df[['Temperature', 'Humidity']]
y = df['Energy_Consumption']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

st.subheader("📈 Model Performance")
st.write(f"**Mean Absolute Error:** {mae:.2f}")
st.write(f"**R² Score:** {r2:.2f}")

# -------------------------------------------
# 3. User Input for Prediction
# -------------------------------------------
st.subheader("🔮 Predict Energy Consumption")

temperature = st.number_input("Enter Temperature (°C):", min_value=0.0, max_value=50.0, value=25.0, step=0.5)
humidity = st.number_input("Enter Humidity (%):", min_value=0.0, max_value=100.0, value=60.0, step=1.0)

if st.button("Predict"):
    input_data = np.array([[temperature, humidity]])
    prediction = model.predict(input_data)
    st.success(f"Predicted Energy Consumption: **{prediction[0]:.2f} kWh**")

# -------------------------------------------
# 4. Visualization
# -------------------------------------------
st.subheader("📉 Actual vs Predicted (Test Data)")
fig, ax = plt.subplots()
ax.scatter(y_test, y_pred, color='blue')
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
ax.set_xlabel('Actual Energy Consumption')
ax.set_ylabel('Predicted Energy Consumption')
ax.set_title('Actual vs Predicted')
st.pyplot(fig)
