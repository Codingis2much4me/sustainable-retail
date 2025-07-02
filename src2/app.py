import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import ai_core # Our main AI logic file

st.set_page_config(layout="wide", page_title="Walmart Fresh Future")

# --- Title and Header ---
st.title("Walmart Fresh Future 💡")
st.markdown("An AI-powered ecosystem for a sustainable future, combining strategic planning with tactical action to minimize food waste.")

# --- 1. STRATEGIC PLANNER: Monthly Forecasting ---
st.header("1. Strategic Planner: Monthly Forecast")
st.markdown("This AI analyzes 5 years of historical data to recommend optimal stock levels and predict potential waste for the upcoming month, enabling smarter inventory decisions.")

# Run strategic prediction
products_list = ["Chicken Breast", "Organic Bananas", "Gallon Milk", "Bagged Salad", "Artisan Bread"]
next_month = (datetime.now().month % 12) + 1
next_year = datetime.now().year if next_month > 1 else datetime.now().year + 1

if ai_core.MODELS_LOADED:
    strategic_predictions = ai_core.run_strategic_prediction(products_list, next_month, next_year)

    col1, col2 = st.columns(2)
    total_rec_stock = strategic_predictions['Recommended Stock (Units)'].sum()
    total_pred_waste = strategic_predictions['Predicted Waste (Units)'].sum()
    col1.metric(f"Total Recommended Stock for Next Month", f"{total_rec_stock:,} units")
    col2.metric(f"Total Predicted Waste for Next Month", f"{total_pred_waste:,} units", delta=f"-{round((total_pred_waste/total_rec_stock)*100, 1)}% of stock", delta_color="inverse")

    # Interactive Graph
    fig = px.bar(strategic_predictions, x='Product', y=['Recommended Stock (Units)', 'Predicted Waste (Units)'],
                 barmode='group', title=f"AI-Powered Forecast for Month {next_month}/{next_year}",
                 labels={'value': 'Number of Units', 'variable': 'Metric'})
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("View Detailed Forecast Data"):
        st.dataframe(strategic_predictions)

    # --- Purchase Order Generation ---
    st.header("2. Generate Next Month's Purchase Order")
    if st.button("Generate Purchase Order CSV"):
        po_df = strategic_predictions[['Product', 'Recommended Stock (Units)']]
        st.download_button(
            label="Download Purchase Order",
            data=po_df.to_csv(index=False).encode('utf-8'),
            file_name=f"purchase_order_{next_month}_{next_year}.csv",
            mime='text/csv',
        )
else:
    st.error("Strategic models not found. Please run the training scripts first.")


st.markdown("---")

# --- Run Tactical Analysis (Needed for multiple sections) ---
try:
    inventory_df = pd.read_csv('current_inventory.csv')
    if ai_core.MODELS_LOADED:
        sale_items, donation_items = ai_core.run_tactical_analysis(inventory_df.copy())
    else:
        sale_items, donation_items = pd.DataFrame(), pd.DataFrame()
except FileNotFoundError:
    st.error("Error: 'current_inventory.csv' not found. Please run generate_data.py first.")
    sale_items, donation_items = pd.DataFrame(), pd.DataFrame()


# --- 3. SUSTAINABILITY IMPACT DASHBOARD ---
st.header("3. Sustainability & Business Impact")
st.markdown("Quantifying the positive impact of proactive, AI-driven waste reduction.")

if ai_core.MODELS_LOADED and not sale_items.empty:
    # --- Dummy calculations for impact ---
    co2_saved_per_unit = 0.5 # kg CO2e per unit of food waste saved
    water_saved_per_unit = 25 # Liters of water per unit
    total_waste_prevented = donation_items['current_stock'].sum() + sale_items['current_stock'].sum()
    total_revenue_recovered = sale_items['recovered_revenue'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total CO2 Emissions Saved", f"{total_waste_prevented * co2_saved_per_unit:.1f} kg")
    col2.metric("Embedded Water Saved", f"{total_waste_prevented * water_saved_per_unit:,.0f} Liters")
    col3.metric("Revenue Recovered Today", f"${total_revenue_recovered:,.2f}")


st.markdown("---")


# --- 4. TACTICAL RESPONDER: Daily Flash Sales & Donations ---
st.header("4. Tactical Responder: Daily Inventory Actions")
st.markdown("This AI runs daily, scanning current on-shelf inventory. It identifies at-risk items and triggers dynamic flash sales or charity donations to prevent waste in real-time.")

if ai_core.MODELS_LOADED:
    # Dashboard Metrics
    st.subheader("Today's Real-Time Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Items on Flash Sale", f"{len(sale_items)}")
    col2.metric("Items for Donation", f"{len(donation_items)}")
    potential_meals = int(donation_items['current_stock'].sum() * 2.5) # Assuming 1 item = 2.5 meals
    col3.metric("Potential Meals Donated", f"~ {potential_meals:,}")
    
    # --- Consumer-Facing Notifier ---
    st.subheader("📱 Mock Consumer-Facing Notifier")
    if not sale_items.empty:
        latest_item = sale_items.iloc[0]
        st.info(f"**New Flash Sale Alert!** ⚡ {latest_item['product_name']} is now {int(latest_item['discount_rate']*100)}% off! Only {latest_item['current_stock']} left. Grab it before it's gone!")

    # Display Flash Sale Items
    st.subheader("🛒 Fresh Flash Sale Items")
    if not sale_items.empty:
        for index, row in sale_items.iterrows():
            st.markdown(
                f"""
                <div style="border: 2px solid #28a745; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 2px 2px 10px #EAEAEA;">
                    <h4>{row['product_name']} <span style="font-size: 14px; color: grey;">({row['category']})</span></h4>
                    <p>
                        <span style="background-color: #dc3545; color: white; padding: 4px 8px; border-radius: 5px; font-weight: bold;">
                            {int(row['discount_rate']*100)}% OFF
                        </span>
                        &nbsp; | &nbsp; 
                        Expires in: <strong>{row['days_until_expiry']} days</strong>
                        &nbsp; | &nbsp; 
                        Stock: {row['current_stock']} units
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("Inventory is optimal. No items require a flash sale right now.")

    # Display Donation Items
    st.subheader("💖 Upcoming Charity Donations (Expires in <= 2 days)")
    if not donation_items.empty:
        # TYPO FIX IS HERE: Changed 'donation_actions' to 'donation_items'
        st.dataframe(donation_items[['product_name', 'current_stock', 'days_until_expiry', 'category']])
    else:
        st.info("No items are scheduled for immediate donation.")

else:
    st.error("Tactical model not found. Please run the training scripts first.")