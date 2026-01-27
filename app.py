import streamlit as st
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

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
    .navbar-subtitle {
        font-size: 0.875rem;
        color: #e2e8f0;
        font-weight: 400;
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
        color: #1e293b;
        font-weight: 700;
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 0.5rem;
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

<div class="navbar">
    <div class="navbar-title">📊 Amudham Naturals</div>
    <div class="navbar-subtitle">Analytics Dashboard</div>
</div>
""", unsafe_allow_html=True)

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
        if 'Place of Delivery' in df.columns:
            df['State'] = df['Place of Delivery'].astype(str).str.strip().str.upper()
        else:
            df['State'] = "UNKNOWN"
            
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
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", f"{len(df):,}")
            with col2:
                total_revenue = df['Invoice Value'].sum()
                st.metric("Total Revenue", f"₹{total_revenue:,.2f}")
            with col3:
                st.metric("Total Columns", len(df.columns))

            # Raw Data Expander
            with st.expander("View Raw Data Frame"):
                st.dataframe(df.head(100))
                
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
            
            state_analysis = df.groupby('State').agg({
                'Invoice Value': ['count', 'sum']
            }).round(2)
            state_analysis.columns = ['Order Count', 'Total Revenue']
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
                    ["Bar Chart (Best for Comparison)", "Pie Chart (Best for Share)", "Treemap (Best for Hierarchy)"],
                    horizontal=True,
                    label_visibility="collapsed"
                )
                
                # Check if there are too many states for Pie/Treemap
                plot_data_df = state_analysis.reset_index()
                
                if "Bar" in chart_type:
                    # Horizontal Bar Chart
                    fig = px.bar(
                        plot_data_df.sort_values('Total Revenue', ascending=True), 
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
                    # Logic to group smaller segments for Pie Chart
                    if len(plot_data_df) > 10:
                        top_9 = plot_data_df.nlargest(9, 'Total Revenue')
                        others_val = plot_data_df.nsmallest(len(plot_data_df) - 9, 'Total Revenue')['Total Revenue'].sum()
                        others_row = pd.DataFrame({'State': ['OTHERS'], 'Order Count': [0], 'Total Revenue': [others_val]})
                        plot_data_df = pd.concat([top_9, others_row])
                    
                    fig = px.pie(
                        plot_data_df, 
                        values='Total Revenue', 
                        names='State',
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.RdBu
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                elif "Treemap" in chart_type:
                    fig = px.treemap(
                        plot_data_df, 
                        path=['State'], 
                        values='Total Revenue',
                        color='Total Revenue',
                        color_continuous_scale='Greens'
                    )
                    st.plotly_chart(fig, use_container_width=True)

            # --- 4. TEMPORAL ANALYSIS ---
            st.divider()
            st.header("4. Temporal Analysis")

            monthly_analysis = df.groupby(['Year', 'Month']).agg({
                'Invoice Value': ['count', 'sum']
            }).round(2)
            monthly_analysis.columns = ['Order Count', 'Total Revenue']
            
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

if __name__ == "__main__":
    main()
