import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import config # Import the new config file

print("--- Training Tactical Model (Sell-Through Rate) ---")

# 1. Load Data using config
try:
    df = pd.read_csv(config.TACTICAL_TRAINING_DATA)
except FileNotFoundError:
    print(f"Error: '{config.TACTICAL_TRAINING_DATA}' not found. Please run generate_data.py first.")
    exit()

# 2. Define Features and Target
features = ['days_until_expiry', 'stock_to_sales_ratio']
X = df[features]
y = df['sell_through_rate']

# 3. Split Data for evaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train Model
print("Training model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate Model
print("Evaluating model...")
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"Model Mean Squared Error: {mse:.4f}")

# 6. Save Model using config
joblib.dump(model, config.SELL_THROUGH_MODEL)
print(f"✅ Saved '{config.SELL_THROUGH_MODEL}'")
print("\nTactical model training complete.")