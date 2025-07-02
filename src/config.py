from pathlib import Path

# Define the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Define paths for data and models relative to the base directory
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Data file paths
TACTICAL_TRAINING_DATA = DATA_DIR / "tactical_training_data.csv"
HISTORICAL_DATA = DATA_DIR / "historical_data.csv"
CURRENT_INVENTORY = DATA_DIR / "current_inventory.csv"

# Model file paths
SELL_THROUGH_MODEL = MODELS_DIR / "sell_through_model.joblib"
STOCK_MODEL = MODELS_DIR / "stock_model.joblib"
WASTE_MODEL = MODELS_DIR / "waste_model.joblib"