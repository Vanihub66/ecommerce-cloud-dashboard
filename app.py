import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import boto3
from io import StringIO

# Page configuration for a clean dashboard layout
st.set_page_config(page_title="E-Commerce Analytics Dashboard", layout="wide")

# ==================== DATA LOADING LAYER ====================
@st.cache_data
def load_data_from_aws():
    """
    Loads data from AWS S3. 
    Uses a local backup dataset if cloud credentials are not provided.
    """
    try:
        # AWS S3 Client setup
        s3 = boto3.client(
            's3',
            aws_access_key_id='YOUR_ACCESS_KEY', 
            aws_secret_access_key='YOUR_SECRET_KEY',
            region_name='us-east-1'
        )
        
        bucket_name = 'vani-ecommerce-analytics-bucket'
        file_key = 'raw_sales_data.csv'
        
        # Fetching dataset from S3
        csv_obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        body = csv_obj['Body'].read().decode('utf-8')
        
        df = pd.read_csv(StringIO(body))
        return df, True
        
    except Exception:
        # Backup: Local dataset simulation if cloud connection is missing
        np.random.seed(42)
        n_orders = 100 
        data = {
            'Order_ID': [f'ORD{1000 + i}' for i in range(n_orders)],
            'Customer_Age': np.random.randint(18, 65, size=n_orders),
            'Product_Category': np.random.choice(['Electronics', 'Clothing', 'Home Decor'], size=n_orders),
            'Sales_Amount': np.random.randint(100, 5000, size=n_orders),
            'Profit_Margin': np.random.uniform(-0.1, 0.3, size=n_orders)
        }
        df = pd.DataFrame(data)
        return df, False

# Load data and create profit column
df, aws_connected = load_data_from_aws()
df['Profit_Amount'] = df['Sales_Amount'] * df['Profit_Margin']

# Create age segments
age_bins = [0, 30, 50, 100]
age_labels = ['Youth', 'Working Class', 'Senior']
df['Age_Group'] = pd.cut(df['Customer_Age'], bins=age_bins, labels=age_labels)


# ==================== DASHBOARD UI ====================
st.title("📊 Cloud-Integrated E-Commerce Performance Dashboard")

# Display pipeline connection status
if aws_connected:
    st.success("⚡ Pipeline Status: Connected to Live AWS S3 Bucket!")
else:
    st.info("ℹ️ Pipeline Status: Running on Automated Local Backup Data")

st.markdown("---")

# Sidebar Filters
st.sidebar.header("🎯 Filter Options")
selected_category = st.sidebar.multiselect(
    "Select Product Categories:",
    options=df['Product_Category'].unique(),
    default=df['Product_Category'].unique()
)

# Apply filters to dataset
filtered_df = df[df['Product_Category'].isin(selected_category)]

# Financial KPI Cards
total_revenue = filtered_df['Sales_Amount'].sum()
total_profit = filtered_df['Profit_Amount'].sum()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="💰 Total Revenue", value=f"₹{total_revenue:,.2f}")
with col2:
    st.metric(label="📈 Total Profit", value=f"₹{total_profit:,.2f}")

st.markdown("---")

# Interactive Charts Panel
col3, col4 = st.columns(2)

with col3:
    st.subheader("🛍️ Total Sales by Product Category")
    product_analysis = filtered_df.groupby('Product_Category')['Sales_Amount'].sum().reset_index()
    fig_bar = px.bar(product_analysis, x='Product_Category', y='Sales_Amount', 
                     color='Product_Category', text_auto='.2s',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_bar, width='stretch')

with col4:
    st.subheader("📉 Profit Trend by Product Category")
    product_profit = filtered_df.groupby('Product_Category')['Profit_Amount'].sum().reset_index()
    fig_line = px.line(product_profit, x='Product_Category', y='Profit_Amount', markers=True)
    fig_line.add_hline(y=0, line_dash="dash", line_color="black")
    st.plotly_chart(fig_line, width='stretch')

# Data Registry View
st.subheader("📋 Detailed Transaction Registry")
st.dataframe(filtered_df, width='stretch')


# ==================== PREDICTIVE ANALYTICS ENGINE ====================
from sklearn.linear_model import LinearRegression

st.markdown("---")
st.subheader("🔮 Sales Revenue Forecasting Model")
st.markdown("Predicting future revenue outcomes based on historical marketing expenditures.")

# Training dataset vectors
X_marketing = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]).reshape(-1, 1)
Y_sales = np.array([1200, 1800, 2500, 3100, 4000, 4400, 5100, 5900, 6400, 7200])

# Initialize and train linear regression model
model = LinearRegression()
model.fit(X_marketing, Y_sales)

# User slider input for marketing budget
st.markdown("### 🎛️ Select Next Month's Marketing Budget:")
budget = st.slider("Adjust marketing budget plan (₹):", 
                       min_value=1000, max_value=5000, value=1500, step=500)

# Run model prediction
predicted_sales = model.predict(np.array([[budget]]))[0]

# Display prediction result
st.info(f"🔮 **Revenue Forecast:** Spending **₹{budget:,}** on marketing is expected to estimate a revenue of **₹{predicted_sales:,.2f}**.")

# Generate future forecast projection curve
future_budgets = np.array(range(1000, 5500, 500)).reshape(-1, 1)
future_preds = model.predict(future_budgets)

pred_df = pd.DataFrame({
    'Marketing_Budget': future_budgets.flatten(),
    'Predicted_Sales': future_preds
})

fig_pred = px.line(pred_df, x='Marketing_Budget', y='Predicted_Sales', 
                   title="📈 Revenue Growth Projection Curve",
                   markers=True, color_discrete_sequence=['purple'])
st.plotly_chart(fig_pred, width='stretch')