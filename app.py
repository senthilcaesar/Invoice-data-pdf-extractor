import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import re
import math

# Page Configuration
st.set_page_config(
    page_title="Amudham Naturals - Analytics",
    page_icon="📊",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Global Settings */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Navbar */
    .navbar {
        background-color: #0e3b5e;
        padding: 1.5rem 2rem;
        margin: -4rem -4rem 2rem -4rem; /* Negative margins to span full width */
        color: white;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .navbar-title {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .navbar-tagline {
        font-size: 0.875rem;
        color: #ccd6e0;
        font-weight: 400;
        margin-top: 4px;
        max-width: 700px;
        line-height: 1.4;
    }
    .navbar-subtitle {
        font-size: 0.875rem;
        color: #e2e8f0;
        font-weight: 600;
        text-align: right;
    }
    .navbar-version {
        font-size: 0.7rem;
        color: #94a3b8;
        font-weight: 400;
        text-align: right;
        margin-top: 2px;
    }
    
    /* Metric Cards Styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    div[data-testid="metric-container"] > label {
        font-weight: 600;
        color: #64748b;
        font-size: 0.875rem;
    }
    div[data-testid="metric-container"] > div[data-testid="stMetricValue"] {
        color: #0e3b5e;
        font-weight: 700;
        font-size: 1.75rem;
    }

    /* Section Headers */
    h2 {
        color: #0e3b5e;
        font-weight: 700;
        font-size: 1.6rem;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        padding: 10px 0px 10px 15px;
        background: linear-gradient(90deg, #f8fafc 0%, rgba(255,255,255,0) 100%);
        border-left: 5px solid #f59e0b; /* Distinct Orange Accent */
        border-bottom: none;
    }
    h3 {
        color: #334155;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Upload Section Styling */
    .uploadedFileName { 
        font-weight: 600; 
        color: #0e3b5e;
    }
    div[data-testid="stFileUploader"] {
        background-color: #f8fafc;
        border-radius: 12px;
        padding: 20px;
        border: 1px dashed #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="navbar">
    <div class="navbar-left">
        <div class="navbar-title">📊 Amudham Naturals</div>
        <div class="navbar-tagline">
            Turn Amazon invoice data into powerful insights. This application automates data extraction 
            and provides an interactive dashboard to instantly track growth, geographical demand, and profitability.
        </div>
    </div>
    <div class="navbar-right">
        <div class="navbar-subtitle">Business Intelligence Portal</div>
        <div class="navbar-version">v1.0.0</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- PROFIT CALCULATION LOGIC ---
data = [
    ["Amudham Naturals Cane Jaggery Powder, Natural Sweetener, Vegetarian, 1kg Pouch", 50, 100, 7.08, 20, 177.08, 15.00, 208, 31, 10.42, 219],
    ["Amudham Naturals Raw Peanuts, Natural Groundnuts, Unroasted, 1kg Pack", 130, 100, 7.08, 20, 257.08, 10.00, 286, 29, 14.28, 300],
    ["Amudham Naturals Roasted Peanut with Skin, Unsalted, High Protein, Crunchy & Healthy, 350g", 45, 76, 7.08, 20, 148.08, 18.00, 181, 33, 9.03, 190],
    ["Roasted Salted Peanuts, 350g", 45, 76, 7.08, 20, 148.08, 18.00, 181, 33, 9.03, 190],
    ["Amudham Naturals 100% Pure Ragi Flour, Traditional Indian Finger Millet Flour, No Added Preservatives, Gluten-Free, 1 kg", 60, 100, 7.08, 20, 187.08, 21.00, 237, 50, 11.84, 249],
    ["Amudham Naturals 100% Pure Sprouted Ragi Flour, Traditional Indian Finger Millet, No Added Preservatives, Gluten-Free, 1 kg", 60, 100, 7.08, 20, 187.08, 34.50, 286, 99, 14.28, 300],
    ["Amudham Naturals 100% Pure Sprouted Ragi Flour, Traditional Indian Finger Millet, No Added Preservatives, Gluten-Free, 500 g", 30, 76, 7.08, 20, 133.08, 30.00, 190, 57, 9.51, 200],
    ["Cashew Nuts, 1kg", 920, 100, 225.27, 20, 1265.27, 8.30, 1380, 115, 68.99, 1449],
    ["Amudham Naturals Premium Whole Cashew Nuts, Raw (500g)", 460, 76, 107.14, 20, 663.14, 7.10, 714, 51, 35.69, 750],
    ["Amudham Naturals Black Rice Porridge Mix | Karuppu Kavuni Kanji Mix | 100% Natural (350g)", 80, 76, 7.08, 20, 183.08, 26.00, 247, 64, 12.37, 260],
    ["Amudham Naturals Black Rice Porridge Mix | Karuppu Kavuni Kanji Mix | 100% Natural (250g)", 60, 76, 7.08, 20, 163.08, 18.50, 200, 37, 10.00, 210],
    ["Amudham Naturals 100% Pure White Rice Flour, Finely Milled Powder for Idlis, Dosas, Traditional Recipes, No Preservatives, 1 kg", 60, 100, 7.08, 20, 187.08, 18.00, 228, 41, 11.41, 240],
    ["Steamed Rice Flour, 1kg", 60, 100, 7.08, 20, 187.08, 24.50, 248, 61, 12.39, 260],
    ["Wheat Flour, 1kg", 60, 100, 7.08, 20, 187.08, 18.00, 228, 41, 11.41, 240],
    ["Golden Maize Corn Flour", 50, 100, 7.08, 20, 177.08, 22.50, 228, 51, 11.42, 240],
    ["Jowar Atta, Sorghum Flour", 70, 100, 7.08, 20, 197.08, 20.00, 246, 49, 12.32, 259],
    ["Amudham Naturals Pesarattu Dosa Mix, Green Gram Dosa Instant Batter Mix, High Protein, Gluten-Free, 500g", 75, 76, 7.08, 20, 178.08, 30.00, 254, 76, 12.72, 267],
    ["Amudham Naturals Kambu Dosa Mix, Pearl Millet, Instant Breakfast Batter, Preservative-Free, 100% Natural, 500g", 60, 76, 7.08, 20, 163.08, 31.00, 236, 73, 11.82, 248],
    ["7-Grain Multi Grain Atta, 1kg", 80, 100, 7.08, 20, 207.08, 22.00, 265, 58, 13.27, 279],
    ["Green Tea, 200g", 160, 76, 7.08, 20, 263.08, 29.00, 371, 107, 18.53, 389],
    ["Black Rice, 1kg", 180, 100, 44, 20, 344, 12.00, 391, 47, 19.55, 410],
    ["Amudham Naturals Mappillai Samba Red Rice, Traditional Indian Bridegroom Rice, 1kg", 80, 100, 7.08, 20, 207.08, 13.50, 239, 32, 11.97, 251]
]

columns = ["Description", "Purchase cost", "Shipping cost", "Referral fee", "Packing cost", "Total Cost", "Margin %", "SP before GST", "Profit", "GST", "Final SP"]
df_data_internal = pd.DataFrame(data, columns=columns)

def extract_weight(description):
    desc = str(description).lower()
    g_match = re.search(r'(\d+)\s*g', desc)
    if g_match: return int(g_match.group(1)) / 1000.0
    kg_match = re.search(r'(\d+(?:\.\d+)?)\s*kg', desc)
    if kg_match: return float(kg_match.group(1))
    return 0.5

def get_dynamic_shipping(total_weight_kg):
    if total_weight_kg <= 0.5: return 76
    elif total_weight_kg <= 1.0: return 100
    elif total_weight_kg <= 2.0: return 143
    elif total_weight_kg <= 5.0: return 143 + (math.ceil(total_weight_kg - 2.0) * 40)
    else: return 263 + (math.ceil(total_weight_kg - 5.0) * 26)

product_costs = {}
for _, row in df_data_internal.iterrows():
    name = row['Description'].strip().lower()
    product_costs[name] = {
        'purchase': row['Purchase cost'], 'referral': row['Referral fee'],
        'packing': row['Packing cost'], 'sp_before_gst': row['SP before GST'],
        'weight': extract_weight(row['Description'])
    }

def calculate_profit_internal(description, qty):
    if pd.isna(description): return 0
    try: quantity = int(qty) if not pd.isna(qty) else 1
    except: quantity = 1
    
    description_str = str(description).lower()
    matched_products = []
    remaining_desc = description_str
    sorted_names = sorted(product_costs.keys(), key=len, reverse=True)
    
    for name in sorted_names:
        if name in remaining_desc:
            # Count how many times this product appears in the string
            # This handles cases where multiple items are listed in one row
            count = remaining_desc.count(name)
            matched_products.extend([product_costs[name]] * count)
            # Remove to prevent double-matching with shorter names
            remaining_desc = remaining_desc.replace(name, " ")
            
    if not matched_products: return 0
    
    total_sp = sum(p['sp_before_gst'] for p in matched_products)
    total_purchase = sum(p['purchase'] for p in matched_products)
    total_referral = sum(p['referral'] for p in matched_products)
    total_packing = sum(p['packing'] for p in matched_products)
    total_weight = sum(p['weight'] for p in matched_products)
    
    revenue = total_sp * quantity
    base_costs = (total_purchase + total_referral + total_packing) * quantity
    shipping = get_dynamic_shipping(total_weight * quantity)
    
    return round(revenue - base_costs - shipping, 2)

def load_and_process_data(uploaded_file):
    """Load and perform initial cleaning on the data."""
    try:
        df = pd.read_csv(uploaded_file)
        
        # Data Cleaning Logic from analysis.py
        # 1. Clean Order Date
        df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d.%m.%Y', errors='coerce')
        
        # 2. Clean Invoice Value
        # Handle cases where it might be string or mixed
        if df['Invoice Value'].dtype == 'object':
             df['Invoice Value'] = pd.to_numeric(df['Invoice Value'].astype(str).str.replace('₹', '').str.replace(',', ''), errors='coerce')
        
        # 3. Extract Date Components
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.month
        df['Day'] = df['Order Date'].dt.day
        df['DayOfWeek'] = df['Order Date'].dt.day_name()
        
        # 4. Clean Place of Delivery
        states_map = {
            'ANDHRA PRADESH': 'Andhra Pradesh', 'ARUNACHAL PRADESH': 'Arunachal Pradesh',
            'ASSAM': 'Assam', 'BIHAR': 'Bihar', 'CHHATTISGARH': 'Chhattisgarh',
            'GOA': 'Goa', 'GUJARAT': 'Gujarat', 'HARYANA': 'Haryana',
            'HIMACHAL PRADESH': 'Himachal Pradesh', 'JHARKHAND': 'Jharkhand',
            'KARNATAKA': 'Karnataka', 'KERALA': 'Kerala', 'MADHYA PRADESH': 'Madhya Pradesh',
            'MAHARASHTRA': 'Maharashtra', 'MANIPUR': 'Manipur', 'MEGHALAYA': 'Meghalaya',
            'MIZORAM': 'Mizoram', 'NAGALAND': 'Nagaland', 'ODISHA': 'Odisha',
            'PUNJAB': 'Punjab', 'RAJASTHAN': 'Rajasthan', 'SIKKIM': 'Sikkim',
            'TAMIL NADU': 'Tamil Nadu', 'TAMILNADU': 'Tamil Nadu', 'TAMIL NADU ': 'Tamil Nadu',
            'TELANGANA': 'Telangana', 'TRIPURA': 'Tripura', 'UTTAR PRADESH': 'Uttar Pradesh',
            'UTTARAKHAND': 'Uttarakhand', 'WEST BENGAL': 'West Bengal',
            # Union Territories
            'ANDAMAN AND NICOBAR ISLANDS': 'Andaman and Nicobar Islands',
            'CHANDIGARH': 'Chandigarh', 'DADRA AND NAGAR HAVELI AND DAMAN AND DIU': 'Dadra and Nagar Haveli and Daman and Diu',
            'DELHI': 'Delhi', 'JAMMU AND KASHMIR': 'Jammu and Kashmir',
            'LADAKH': 'Ladakh', 'LAKSHADWEEP': 'Lakshadweep', 'PUDUCHERRY': 'Puducherry'
        }
        
        def normalize_state(val):
            val_str = str(val).upper().strip()
            # Direct mapping
            if val_str in states_map:
                return states_map[val_str]
            # Search within string if not a direct match (handles noisy address strings)
            for state_key in states_map.keys():
                if state_key in val_str:
                    return states_map[state_key]
            return "Unknown"

        if 'Place of Delivery' in df.columns:
            df['State'] = df['Place of Delivery'].apply(normalize_state)
        elif 'State' in df.columns:
            df['State'] = df['State'].apply(normalize_state)
        else:
            df['State'] = "Unknown"
            
        # 5. Clean Qty and Calculate Profit
        df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(1).astype(int)
        df['Profit'] = df.apply(lambda row: calculate_profit_internal(row['Description'], row['Qty']), axis=1)
            
        return df
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None

def main():
    st.write("Upload your `all_invoices.csv` file below to view the analytics.")

    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    # Session state for sample data
    if 'load_sample' not in st.session_state:
        st.session_state.load_sample = False
    
    if st.button("Load Sample Data"):
        st.session_state.load_sample = True
        
    # Determine which file to process
    df = None
    if uploaded_file is not None:
        st.session_state.load_sample = False # Reset sample state if user uploads a file
        with st.spinner('Processing uploaded data...'):
            df = load_and_process_data(uploaded_file)
    elif st.session_state.load_sample:
        try:
            with st.spinner('Loading sample data...'):
                df = load_and_process_data("all_invoices.csv")
            st.info("Using sample data: `all_invoices.csv`")
        except FileNotFoundError:
            st.error("Sample file `all_invoices.csv` not found in directory.")

    if df is not None:
            # --- 1. BASIC DATA OVERVIEW ---
            st.divider()
            st.header("1. Basic Data Overview")
            
            # Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Records", f"{len(df):,}")
            with col2:
                total_revenue = df['Invoice Value'].sum()
                st.metric("Total Revenue", f"₹{total_revenue:,.2f}")
            with col3:
                total_profit = df['Profit'].sum()
                st.metric("Total Profit", f"₹{total_profit:,.2f}")
            with col4:
                st.metric("Total Columns", len(df.columns))

            # Raw Data Expander
            with st.expander("View Raw Data Frame"):
                st.dataframe(df)
                
            # Column Types
            with st.expander("View Column Info"):
                dtype_df = df.dtypes.astype(str).reset_index()
                dtype_df.columns = ["Column", "Type"]
                st.table(dtype_df)

            # --- 2. DATA QUALITY ---
            st.divider()
            st.header("2. Data Quality Check")
            
            missing = df.isnull().sum()
            missing = missing[missing > 0]
            if not missing.empty:
                st.warning("Found missing values in the following columns:")
                col_miss1, col_miss2 = st.columns([1, 2])
                with col_miss1:
                    missing_df = pd.DataFrame({'Missing Count': missing, 'Percentage': (missing / len(df) * 100).round(2)})
                    st.dataframe(missing_df)
            else:
                st.success("No missing values found!")

            # --- 3. GEOGRAPHICAL ANALYSIS ---
            st.divider()
            st.header("3. Geographical Analysis")
            
            # All India States and UTs for complete map display
            all_india_states = [
                'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
                'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
                'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
                'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan',
                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands',
                'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu',
                'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
            ]
            
            state_analysis = df.groupby('State').agg({
                'Invoice Value': ['count', 'sum'],
                'Profit': 'sum'
            }).round(2)
            state_analysis.columns = ['Order Count', 'Total Revenue', 'Total Profit']
            
            # Reindex to include all states and fill with 0
            state_analysis = state_analysis.reindex(all_india_states).fillna(0)
            state_analysis = state_analysis.sort_values('Total Revenue', ascending=False)

            col_geo1, col_geo2 = st.columns([1, 1])
            with col_geo1:
                st.subheader("State-wise Table")
                st.dataframe(state_analysis, height=400)
            
            with col_geo2:
                st.subheader("Revenue by State")
                
                # Chart Type Selection
                chart_type = st.radio(
                    "Select Chart Type:",
                    ["Map (Interactive)", "Bar Chart", "Pie Chart"],
                    horizontal=True,
                    label_visibility="collapsed"
                )
                
                # Check if there are too many states for Pie/Treemap
                plot_data_df = state_analysis.reset_index()
                
                if "Map" in chart_type:
                    # Choropleth Map of India
                    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                    
                    fig = px.choropleth(
                        plot_data_df,
                        geojson=geojson_url,
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Order Count',
                        hover_name='State',
                        hover_data={'Order Count': True, 'Total Revenue': ':₹,.2f', 'Total Profit': ':₹,.2f'},
                        color_continuous_scale=px.colors.sequential.Blues,
                        range_color=[0, plot_data_df['Order Count'].max()],
                        labels={'Order Count': 'Orders'}
                    )
                    
                    fig.update_geos(
                        visible=False, 
                        resolution=50,
                        showcountries=True, 
                        countrycolor="RebeccaPurple",
                        fitbounds="locations"
                    )
                    
                    fig.update_layout(
                        margin={"r":0,"t":0,"l":0,"b":0},
                        height=500,
                        coloraxis_colorbar=dict(
                            title="Orders",
                            thicknessmode="pixels", thickness=15,
                            lenmode="pixels", len=200,
                            yanchor="top", y=1,
                            ticks="outside"
                        )
                    )
                    st.plotly_chart(fig, use_container_width=True)

                elif "Bar" in chart_type:
                    # Horizontal Bar Chart - Filter out states with no orders
                    bar_plot_df = plot_data_df[plot_data_df['Order Count'] > 0].sort_values('Total Revenue', ascending=True)
                    
                    fig = px.bar(
                        bar_plot_df, 
                        x='Total Revenue', 
                        y='State',
                        orientation='h',
                        text_auto='.2s',
                        color='Total Revenue',
                        color_continuous_scale='Blues'
                    )
                    fig.update_layout(showlegend=False, height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                elif "Pie" in chart_type:
                    # Filter out states with no orders for Pie Chart
                    pie_plot_df = plot_data_df[plot_data_df['Order Count'] > 0]
                    
                    # Logic to group smaller segments for Pie Chart
                    if len(pie_plot_df) > 10:
                        top_9 = pie_plot_df.nlargest(9, 'Total Revenue')
                        others_val = pie_plot_df.nsmallest(len(pie_plot_df) - 9, 'Total Revenue')['Total Revenue'].sum()
                        others_row = pd.DataFrame({'State': ['OTHERS'], 'Order Count': [0], 'Total Revenue': [others_val]})
                        pie_plot_df = pd.concat([top_9, others_row])
                    
                    fig = px.pie(
                        pie_plot_df, 
                        values='Total Revenue', 
                        names='State',
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.RdBu
                    )
                    st.plotly_chart(fig, use_container_width=True)

            # --- 4. TEMPORAL ANALYSIS ---
            st.divider()
            st.header("4. Temporal Analysis")

            monthly_analysis = df.groupby(['Year', 'Month']).agg({
                'Invoice Value': ['count', 'sum'],
                'Profit': 'sum'
            }).round(2)
            monthly_analysis.columns = ['Order Count', 'Total Revenue', 'Total Profit']
            
            # Create labels for display
            monthly_analysis_display = monthly_analysis.copy()
            month_labels_idx = []
            for idx in monthly_analysis.index:
                year, month = idx
                month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                month_labels_idx.append(f"{month_names[month-1]} {year}")
            
            monthly_analysis_display.index = month_labels_idx
            
            st.dataframe(monthly_analysis_display, use_container_width=True)

            # --- 5. MONTHLY ORDERS AND REVENUE CHART ---
            st.divider()
            st.header("5. Monthly Orders & Revenue Trend")
            
            # Create Interactive Dual-Axis Chart with Plotly
            fig = go.Figure()

            # Line Chart for Order Count (Primary Y)
            fig.add_trace(
                go.Scatter(
                    x=month_labels_idx,
                    y=monthly_analysis['Order Count'],
                    name="Order Count",
                    line=dict(color='navy', width=3),
                    marker=dict(size=8),
                    mode='lines+markers+text',
                    text=[str(int(v)) for v in monthly_analysis['Order Count']],
                    textposition="top center",
                    yaxis='y1'
                )
            )

            # Line Chart for Revenue (Secondary Y)
            fig.add_trace(
                go.Scatter(
                    x=month_labels_idx,
                    y=monthly_analysis['Total Revenue'],
                    name="Total Revenue",
                    line=dict(color='darkorange', width=3),
                    marker=dict(size=8),
                    mode='lines+markers+text',
                    text=[f'₹{v:,.0f}' for v in monthly_analysis['Total Revenue']],
                    textposition="bottom center",
                    yaxis='y2'
                )
            )

            # Layout Configuration
            fig.update_layout(
                template="plotly_white",
                title=dict(
                    text='Monthly Orders & Revenue Trend', 
                    font=dict(size=20, color='#0e3b5e')
                ),
                xaxis=dict(
                    title=dict(text=''), 
                    showgrid=False
                ),
                yaxis=dict(
                    title=dict(text='Order Count', font=dict(color='navy')),
                    tickfont=dict(color='navy'),
                    showgrid=True,
                    gridcolor='rgba(0,0,0,0.05)'
                ),
                yaxis2=dict(
                    title=dict(text='Revenue (₹)', font=dict(color='darkorange')),
                    tickfont=dict(color='darkorange'),
                    overlaying='y',
                    side='right',
                    showgrid=False
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                hovermode="x unified",
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

            # --- 6. MONTHLY PROFIT CHART ---
            st.divider()
            st.header("6. Monthly Profit Trend")
            
            fig_profit = go.Figure()

            # Line Chart for Profit
            fig_profit.add_trace(
                go.Scatter(
                    x=month_labels_idx,
                    y=monthly_analysis['Total Profit'],
                    name="Monthly Profit",
                    line=dict(color='green', width=4),
                    marker=dict(size=10, symbol='diamond'),
                    mode='lines+markers+text',
                    text=[f'₹{v:,.0f}' for v in monthly_analysis['Total Profit']],
                    textposition="top center"
                )
            )

            fig_profit.update_layout(
                template="plotly_white",
                title=dict(text='Monthly Profit Performance', font=dict(size=20, color='#0e3b5e')),
                xaxis=dict(title=dict(text='Month')),
                yaxis=dict(
                    title=dict(text='Profit (₹)', font=dict(color='green')),
                    tickfont=dict(color='green'),
                    showgrid=True
                ),
                hovermode="x unified",
                height=500
            )

            st.plotly_chart(fig_profit, use_container_width=True)

            # --- 7. PRODUCT PERFORMANCE SUMMARY ---
            st.divider()
            st.header("7. Product Sales & Profit Performance")
            
            product_performance = df.groupby('Description').agg({
                'Qty': 'sum',
                'Invoice Value': 'sum',
                'Profit': 'sum'
            }).reset_index()
            
            # Sort by Quantity descending
            product_performance = product_performance.sort_values('Qty', ascending=False)
            product_performance.columns = ['Product Description', 'Total Quantity', 'Total Revenue (₹)', 'Total Profit (₹)']
            
            # Format currency columns for display
            display_df = product_performance.copy()
            display_df['Total Revenue (₹)'] = display_df['Total Revenue (₹)'].map('₹{:,.2f}'.format)
            display_df['Total Profit (₹)'] = display_df['Total Profit (₹)'].map('₹{:,.2f}'.format)
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            # --- 8. MASTER DATA REFERENCE ---
            st.divider()
            with st.expander("📊 8. Product Cost & Reference Master Data", expanded=False):
                st.markdown("""
                This table shows the unit costs, referral fees, and selling prices used to calculate 
                the profit margins for each product identified in your invoices.
                """)
                # Format currency for display
                master_display = df_data_internal.copy()
                currency_cols = ["Purchase cost", "Referral fee", "Packing cost", "Total Cost", "SP before GST", "Profit", "GST", "Final SP"]
                for col in currency_cols:
                    if col in master_display.columns:
                        master_display[col] = master_display[col].map('₹{:,.2f}'.format)
                
                st.dataframe(master_display, use_container_width=True, hide_index=True)
if __name__ == "__main__":
    main()
