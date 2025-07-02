import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

print("--- Training Strategic Models (Stock & Waste) ---")

# 1. Load Data
try:
    df = pd.read_csv('historical_data.csv')
    df = pd.get_dummies(df, columns=['product_name'], drop_first=True) # One-hot encode product names
except FileNotFoundError:
    print("Error: 'historical_data.csv' not found. Please run generate_data.py first.")
    exit()

# 2. Define Features and Targets
features = [col for col in df.columns if col not in ['historical_stock', 'historical_waste']]
X = df[features]
y_stock = df['historical_stock']
y_waste = df['historical_waste']

# 3. Train Stock Prediction Model
print("Training Recommended Stock model...")
stock_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
stock_model.fit(X, y_stock)
joblib.dump(stock_model, 'stock_model.joblib')
print("✅ Saved 'stock_model.joblib'")

# 4. Train Waste Prediction Model
print("Training Predicted Waste model...")
waste_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
waste_model.fit(X, y_waste)
joblib.dump(waste_model, 'waste_model.joblib')
print("✅ Saved 'waste_model.joblib'")

print("\nStrategic model training complete.")