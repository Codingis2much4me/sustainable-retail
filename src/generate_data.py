import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import config

print("Starting data generation...")

# --- Configuration ---
PRODUCTS = ["Chicken Breast", "Organic Bananas", "Gallon Milk", "Bagged Salad", "Artisan Bread"]
START_DATE = datetime(2018, 1, 1)
MONTHS_OF_DATA = 5 * 12  # 5 years

# --- 1. Generate Strategic Historical Data (5 years) ---
data = []
for i in range(MONTHS_OF_DATA):
    current_date = START_DATE + timedelta(days=i*30)
    month = current_date.month
    year = current_date.year
    
    # Seasonality (e.g., higher demand in summer/holidays)
    seasonality = 1.0
    if month in [6, 7, 11, 12]:
        seasonality = np.random.uniform(1.1, 1.3)
        
    for product in PRODUCTS:
        base_stock = np.random.randint(500, 2000)
        base_sales = np.random.randint(400, base_stock)

        # Simulate effects
        promotions = np.random.choice([0, 1], p=[0.8, 0.2])
        stocked_amount = int(base_stock * seasonality)
        
        # Waste is a function of overstocking and lack of promotions
        waste_percentage = np.random.uniform(0.02, 0.15)
        if (stocked_amount > base_sales * 1.2) and promotions == 0:
            waste_percentage *= 1.5
        wasted_amount = int(stocked_amount * waste_percentage)
        
        data.append({
            "product_name": product,
            "month": month,
            "year": year,
            "promotions": promotions,
            "seasonality_indicator": round(seasonality, 2),
            "historical_stock": stocked_amount,
            "historical_waste": wasted_amount
        })

historical_df = pd.DataFrame(data)
historical_df.to_csv(config.HISTORICAL_DATA, index=False) # Use config
print(f"✅ Generated 'historical_data.csv' with {len(historical_df)} rows.")

# --- 2. Generate Tactical Training Data (for sell-through model) ---
tactical_data = []
for days in [7, 6, 5, 4, 3, 2, 1]:
    for ratio in np.linspace(0.5, 8.0, 10):
        # Logic: sell-through drops sharply as expiry nears and overstock increases
        sell_through = 0.95 * (1 / (ratio**0.5)) * (days / 7)
        sell_through = max(0, min(sell_through - np.random.uniform(0, 0.1), 1.0))
        tactical_data.append({
            "days_until_expiry": days,
            "stock_to_sales_ratio": round(ratio, 2),
            "sell_through_rate": round(sell_through, 2)
        })

tactical_df = pd.DataFrame(tactical_data)
tactical_df.to_csv(config.TACTICAL_TRAINING_DATA, index=False) # Use config
print(f"✅ Generated 'tactical_training_data.csv' with {len(tactical_df)} rows.")


# --- 3. Generate Current Inventory Snapshot ---
today = datetime.now()
current_inventory = [
    {'product_id': 101, 'product_name': 'Chicken Breast', 'category': 'Meat', 'avg_daily_sales': 80, 'current_stock': 100, 'expiry_date': (today + timedelta(days=2)).strftime('%Y-%m-%d')},
    {'product_id': 102, 'product_name': 'Organic Bananas', 'category': 'Produce', 'avg_daily_sales': 150, 'current_stock': 250, 'expiry_date': (today + timedelta(days=4)).strftime('%Y-%m-%d')},
    {'product_id': 103, 'product_name': 'Gallon Milk', 'category': 'Dairy', 'avg_daily_sales': 100, 'current_stock': 300, 'expiry_date': (today + timedelta(days=9)).strftime('%Y-%m-%d')},
    {'product_id': 104, 'product_name': 'Bagged Salad', 'category': 'Produce', 'avg_daily_sales': 60, 'current_stock': 130, 'expiry_date': (today + timedelta(days=1)).strftime('%Y-%m-%d')},
    {'product_id': 105, 'product_name': 'Artisan Bread', 'category': 'Bakery', 'avg_daily_sales': 40, 'current_stock': 90, 'expiry_date': (today + timedelta(days=0)).strftime('%Y-%m-%d')}
]
current_inventory_df = pd.DataFrame(current_inventory)
current_inventory_df.to_csv(config.CURRENT_INVENTORY, index=False) # Use config
print("✅ Generated 'current_inventory.csv' for today.")

print("\nData generation complete!")