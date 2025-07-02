# Sustainable Retail AI Optimizer

This project is a proof-of-concept AI system designed to help retailers optimize inventory management, reduce waste, and make data-driven decisions for stock replenishment. It uses machine learning models to provide both tactical (short-term) and strategic (long-term) recommendations.

## Features

- **Tactical AI Model**: Predicts the sell-through rate of products based on their expiry date and current stock levels, enabling dynamic pricing or promotion recommendations.
- **Strategic AI Model**: Forecasts future stock requirements and potential waste based on historical sales data, helping with procurement planning.
- **Data Generation**: Includes a script to generate synthetic, realistic datasets for training and demonstration.
- **Interactive Dashboard**: A Streamlit application ([`src/app.py`](src/app.py)) provides an easy-to-use interface to view AI-driven recommendations.

## Project Structure

The project is organized to separate concerns, making it scalable and maintainable.

```
/
├── src/                      # All source code
│   ├── ai_core.py            # Core logic for AI predictions
│   ├── app.py                # Main Streamlit application
│   ├── config.py             # Centralized configuration for file paths
│   ├── generate_data.py      # Script to create training/demo data
│   ├── strategic_model_trainer.py # Trains the long-term model
│   └── tactical_model_trainer.py  # Trains the short-term model
├── data/                     # CSV data files (gitignored in a real project)
│   ├── current_inventory.csv
│   ├── historical_data.csv
│   └── tactical_training_data.csv
├── models/                   # Trained model artifacts (gitignored)
│   ├── sell_through_model.joblib
│   ├── stock_model.joblib
│   └── waste_model.joblib
├── requirements.txt          # Python package dependencies
├── README.md                 # This file
└── LICENSE                   # Project license
```

## Setup and Installation

1.  **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd sustainable-retail
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## How to Run

Follow these steps in order to generate data, train the models, and run the application.

1.  **Generate Datasets:**
    Run the data generation script from the root directory. This will create the necessary CSV files in the `data/` folder.
    ```sh
    python src/generate_data.py
    ```

2.  **Train the AI Models:**
    Run the training scripts. This will create the `.joblib` model files in the `models/` folder.
    ```sh
    python src/tactical_model_trainer.py
    python src/strategic_model_trainer.py
    ```

3.  **Launch the Application:**
    Start the Streamlit dashboard.
    ```sh
    streamlit run src/app.py
    ```
    Open your web browser and navigate to the local URL provided by Streamlit.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for full details.