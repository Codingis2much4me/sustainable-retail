import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

print("--- Training Tactical Model (Sell-Through Rate) ---")

# 1. Load Data
try:
    df = pd.read_csv('tactical_training_data.csv')
except FileNotFoundError:
    print("Error: 'tactical_training_data.csv' not found. Please run generate_data.py first.")
    exit()

# 2. Define Features and Target
features = ['days_until_expiry', 'stock_to_sales_ratio']
X = df[features]
y = df['sell_through_rate']

# 3. Train Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 4. Save Model
joblib.dump(model, 'sell_through_model.joblib')
print("✅ Saved 'sell_through_model.joblib'")
print("\nTactical model training complete.")