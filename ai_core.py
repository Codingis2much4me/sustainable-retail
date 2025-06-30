import pandas as pd
import joblib
from datetime import datetime

# --- Load All Trained AI Models ---
try:
    stock_model = joblib.load('stock_model.joblib')
    waste_model = joblib.load('waste_model.joblib')
    sell_through_model = joblib.load('sell_through_model.joblib')
    MODELS_LOADED = True
except FileNotFoundError:
    print("WARNING: One or more model files not found. Please run the trainer scripts.")
    MODELS_LOADED = False

# --- 1. STRATEGIC AI FUNCTIONS ---
def run_strategic_prediction(products, target_month, target_year):
    if not MODELS_LOADED:
        return pd.DataFrame()

    # Create the input DataFrame for the model for next month
    data_to_predict = []
    for product in products:
        data_to_predict.append({
            "month": target_month,
            "year": target_year,
            "promotions": 0, # Assume no promotions for base prediction
            "seasonality_indicator": 1.1, # Assume moderate seasonality
            "product_name": product
        })
    df_predict = pd.DataFrame(data_to_predict)
    
    # One-hot encode to match training format
    df_predict_encoded = pd.get_dummies(df_predict, columns=['product_name'])
    
    # Ensure all columns from training are present
    training_cols = stock_model.feature_names_in_
    for col in training_cols:
        if col not in df_predict_encoded.columns:
            df_predict_encoded[col] = 0
    df_predict_encoded = df_predict_encoded[training_cols] # Order columns correctly

    # Make predictions
    predicted_stock = stock_model.predict(df_predict_encoded)
    predicted_waste = waste_model.predict(df_predict_encoded)

    results_df = pd.DataFrame({
        "Product": products,
        "Recommended Stock (Units)": [int(p) for p in predicted_stock],
        "Predicted Waste (Units)": [int(p) for p in predicted_waste]
    })
    return results_df

# --- 2. TACTICAL AI FUNCTIONS ---
def get_tactical_discount(days_left, stock, avg_sales):
    if days_left < 0 or stock <= 0 or avg_sales <= 0 or not MODELS_LOADED:
        return 0

    stock_ratio = stock / avg_sales
    input_data = pd.DataFrame([[days_left, stock_ratio]], columns=['days_until_expiry', 'stock_to_sales_ratio'])
    
    predicted_sell_through = sell_through_model.predict(input_data)[0]

    discount = 0.0
    if predicted_sell_through < 0.30:
        discount = 0.75
    elif predicted_sell_through < 0.60:
        discount = 0.50
    elif predicted_sell_through < 0.85:
        discount = 0.25

    if days_left > 7: # No sales for items with more than a week left
        return 0
        
    return round(discount, 2)

def run_tactical_analysis(df_inventory):
    # FIX IS HERE: Use Pandas Timestamp for all date operations
    today = pd.Timestamp.now().normalize()  # Gets today's date at midnight
    
    # FIX IS HERE: Convert to datetime but keep it as a Pandas Timestamp object
    df_inventory['expiry_date'] = pd.to_datetime(df_inventory['expiry_date'])

    # This calculation now works correctly
    df_inventory['days_until_expiry'] = (df_inventory['expiry_date'] - today).dt.days

    df_inventory['discount_rate'] = df_inventory.apply(
        lambda row: get_tactical_discount(row['days_until_expiry'], row['current_stock'], row['avg_daily_sales']),
        axis=1
    )
    
    flash_sale_items = df_inventory[(df_inventory['discount_rate'] > 0) & (df_inventory['days_until_expiry'] > 2)].copy()
    donation_items = df_inventory[df_inventory['days_until_expiry'] <= 2].copy()
    
    return flash_sale_items, donation_items