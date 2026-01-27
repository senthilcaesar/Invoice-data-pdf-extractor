import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(
    page_title="Amudham Naturals - Analytics",
    page_icon="📊",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #0e3b5e;
    }
</style>
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
    st.title("📊 Amudham Naturals Invoice Analytics")
    st.write("Upload your `all_invoices.csv` file to generate the analysis dashboard.")

    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

    if uploaded_file is not None:
        with st.spinner('Processing data...'):
            df = load_and_process_data(uploaded_file)

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
                st.bar_chart(state_analysis['Total Revenue'])

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
            
            # Prepare Data for Plotting
            month_labels = month_labels_idx
            
            # Create simple line chart using Matplotlib logic from analysis.py
            fig, ax1 = plt.subplots(figsize=(14, 7))

            # Plot orders on left axis (BLUE)
            color1 = 'blue'
            ax1.set_xlabel('Month', fontsize=13, fontweight='bold')
            ax1.set_ylabel('Total Number of Orders', fontsize=13, fontweight='bold', color=color1)
            line1 = ax1.plot(range(len(monthly_analysis)), monthly_analysis['Order Count'], 
                             color=color1, marker='o', linewidth=3, markersize=12, 
                             label='Order Count')
            ax1.tick_params(axis='y', labelcolor=color1, labelsize=11)
            ax1.set_xticks(range(len(monthly_analysis)))
            ax1.set_xticklabels(month_labels, fontsize=12, fontweight='bold', rotation=45)
            ax1.grid(True, alpha=0.3, linestyle='--')

            # Add value labels for orders
            for i, v in enumerate(monthly_analysis['Order Count']):
                ax1.text(i, v + (v*0.05), str(int(v)), ha='center', fontsize=10, 
                         fontweight='bold', color=color1,
                         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                                  edgecolor=color1, linewidth=1))

            # Plot revenue on right axis (ORANGE)
            ax2 = ax1.twinx()
            color2 = 'darkorange'
            ax2.set_ylabel('Total Invoice Sum (₹)', fontsize=13, fontweight='bold', color=color2)
            line2 = ax2.plot(range(len(monthly_analysis)), monthly_analysis['Total Revenue'], 
                             color=color2, marker='s', linewidth=3, markersize=12, 
                             label='Total Revenue')
            ax2.tick_params(axis='y', labelcolor=color2, labelsize=11)

            # Add value labels for revenue
            for i, v in enumerate(monthly_analysis['Total Revenue']):
                # Offset label slightly to avoid overlap
                ax2.text(i, v - (v*0.1), f'₹{v:,.0f}', ha='center', fontsize=10, 
                         fontweight='bold', color=color2,
                         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                                  edgecolor=color2, linewidth=1))

            plt.title('Amudham Naturals - Monthly Orders and Revenue', fontsize=16, fontweight='bold', pad=20)
            
            # Legend
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10, frameon=True)

            st.pyplot(fig)

if __name__ == "__main__":
    main()
