import pandas as pd
import re
import math



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

columns = [
    "Description",
    "Purchase cost",
    "Shipping cost",
    "Referral fee",
    "Packing cost",
    "Total Cost",
    "Margin %",
    "SP before GST",
    "Profit",
    "GST",
    "Final SP"
]

df_data = pd.DataFrame(data, columns=columns)

df = pd.read_csv("all_invoices.csv")

print("1. BASIC DATA OVERVIEW")
print("-"*80)
print(f"Total Records: {len(df)}")
print(f"Total Columns: {len(df.columns)}")
print(f"\nColumn Names:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")

print(f"\nData Types:")
print(df.dtypes)

print(f"\nMissing Values:")
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({'Missing Count': missing, 'Percentage': missing_pct})
print(missing_df[missing_df['Missing Count'] > 0])

# Clean Order Date
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d.%m.%Y', errors='coerce')
print(f"✓ Order Date converted to datetime")

# Clean Invoice Value
# Clean Invoice Value
if df['Invoice Value'].dtype == 'object':
    df['Invoice Value'] = pd.to_numeric(
        df['Invoice Value'].astype(str).str.replace('₹', '').str.replace(',', ''),
        errors='coerce'
    )
else:
    df['Invoice Value'] = pd.to_numeric(df['Invoice Value'], errors='coerce')
print(f"✓ Invoice Value converted to numeric")

# Extract date components
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Day'] = df['Order Date'].dt.day
df['DayOfWeek'] = df['Order Date'].dt.day_name()
df['WeekOfYear'] = df['Order Date'].dt.isocalendar().week
print(f"✓ Date components extracted")

# Clean Place of Delivery and Normalize State
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
    if val_str in states_map:
        return states_map[val_str]
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
print(f"✓ State names standardized and normalized")

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

# Build a lookup dictionary from df_data for efficiency
product_costs = {}
for _, row in df_data.iterrows():
    name = row['Description'].strip().lower()
    product_costs[name] = {
        'purchase': row['Purchase cost'],
        'referral': row['Referral fee'],
        'packing': row['Packing cost'],
        'sp_before_gst': row['SP before GST'],
        'weight': extract_weight(row['Description'])
    }

def calculate_profit(description, qty):
    if pd.isna(description): return 0
    try: quantity = int(qty) if not pd.isna(qty) else 1
    except: quantity = 1
    
    description_str = str(description).lower()
    matched_products = []
    remaining_desc = description_str
    sorted_names = sorted(product_costs.keys(), key=len, reverse=True)
    
    for name in sorted_names:
        if name in remaining_desc:
            count = remaining_desc.count(name)
            matched_products.extend([product_costs[name]] * count)
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

# Clean Qty column - convert to numeric
df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(1).astype(int)
print(f"✓ Qty column cleaned and converted to numeric")

# Add Profit column using both Description and Qty
df['Profit'] = df.apply(lambda row: calculate_profit(row['Description'], row['Qty']), axis=1)
print(f"✓ Profit column added based on product margins and quantities")


print("\n\n3. DESCRIPTIVE STATISTICS")
print("-"*80)
print(f"\nInvoice Value Statistics:")
print(df['Invoice Value'].describe())

print(f"\nTotal Revenue: ₹{df['Invoice Value'].sum():,.2f}")

print("\n\n5. GEOGRAPHICAL ANALYSIS")
print("-"*80)

state_analysis = df.groupby('State').agg({
    'Invoice Value': ['count', 'sum'],
    'Profit': 'sum'
}).round(2)

state_analysis.columns = ['Order Count', 'Total Revenue', 'Total Profit']
state_analysis = state_analysis.sort_values('Total Revenue', ascending=False)

print(f"\nState-wise Performance:")
print(state_analysis)

print("\n\n6. PRODUCT SALES & PROFIT PERFORMANCE")
print("-"*80)

product_performance = df.groupby('Description').agg({
    'Qty': 'sum',
    'Invoice Value': 'sum',
    'Profit': 'sum'
}).reset_index()

# Sort by Quantity descending
product_performance = product_performance.sort_values('Qty', ascending=False)
product_performance.columns = ['Product Description', 'Total Quantity', 'Total Revenue (₹)', 'Total Profit (₹)']

print(f"\nProduct-wise Performance Summary:")
print(product_performance.to_string(index=False))

print("\n\n7. TEMPORAL ANALYSIS")
print("-"*80)

# Monthly trend
monthly_analysis = df.groupby(['Year', 'Month']).agg({
    'Invoice Value': ['count', 'sum'],
    'Profit': 'sum'
}).round(2)
monthly_analysis.columns = ['Order Count', 'Total Revenue', 'Total Profit']

print(f"\nMonthly Trend:")
print(monthly_analysis)

df.groupby(['Year', 'Month'])['Invoice Value'].sum().reset_index()

df.groupby(['Year', 'Month'])['Invoice Value'].count().reset_index()

df.groupby(['Year', 'Month'])['Invoice Value'] \
  .agg(Order_Count='count', Total_Revenue='sum') \
  .reset_index()

# Save to a specific folder
df.to_csv("invoice_data_with_profit.csv", index=False)

#import pandas as pd
#import matplotlib.pyplot as plt

# The monthly_analysis and labels are already prepared above.
# We skip re-loading to ensure Profit column availability.

# Create month labels
#month_labels = []
#for idx in monthly_analysis.index:
#    year, month = idx
#    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
#                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#    month_labels.append(f"{month_names[month-1]} {year}")

# Create simple line chart
#fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot orders on left axis (BLUE)
#color1 = 'blue'
#ax1.set_xlabel('Month', fontsize=13, fontweight='bold')
#ax1.set_ylabel('Total Number of Orders', fontsize=13, fontweight='bold', color=color1)
#line1 = ax1.plot(range(len(monthly_analysis)), monthly_analysis['Order Count'], 
#                 color=color1, marker='o', linewidth=3, markersize=12, 
#                 label='Order Count')
#ax1.tick_params(axis='y', labelcolor=color1, labelsize=11)
#ax1.set_xticks(range(len(monthly_analysis)))
#ax1.set_xticklabels(month_labels, fontsize=12, fontweight='bold')
#ax1.grid(True, alpha=0.3, linestyle='--')

# Add value labels for orders - positioned ABOVE the line
#for i, v in enumerate(monthly_analysis['Order Count']):
#    ax1.text(i, v + 2.5, str(int(v)), ha='center', fontsize=12, 
#             fontweight='bold', color=color1,
#             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
#                      edgecolor=color1, linewidth=2))

# Plot revenue on right axis (ORANGE)
#ax2 = ax1.twinx()
#color2 = 'darkorange'
#ax2.set_ylabel('Total Invoice Sum (₹)', fontsize=13, fontweight='bold', color=color2)
#line2 = ax2.plot(range(len(monthly_analysis)), monthly_analysis['Total Revenue'], 
#                 color=color2, marker='s', linewidth=3, markersize=12, 
#                 label='Total Revenue')
#ax2.tick_params(axis='y', labelcolor=color2, labelsize=11)

# Add value labels for revenue - positioned BELOW the line
#for i, v in enumerate(monthly_analysis['Total Revenue']):
#    ax2.text(i, v - 600, f'₹{v:,.0f}', ha='center', fontsize=12, 
#             fontweight='bold', color=color2,
#             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
#                      edgecolor=color2, linewidth=2))

# Title
#plt.title('Amudham Naturals - Monthly Orders and Revenue', fontsize=18, fontweight='bold', pad=25)

# Legend
#lines1, labels1 = ax1.get_legend_handles_labels()
#lines2, labels2 = ax2.get_legend_handles_labels()
#ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=12, frameon=True)

# Add some padding to y-axes to prevent label cutoff
#ax1.set_ylim(0, monthly_analysis['Order Count'].max() * 1.15)
#ax2.set_ylim(0, monthly_analysis['Total Revenue'].max() * 1.12)

#plt.tight_layout()
#plt.savefig('/Users/senthilpalanivelu/Desktop/google_analytics/simple_monthly_chart_improved.png', dpi=300, bbox_inches='tight')
#print("\n✓ Improved line chart saved: simple_monthly_chart_improved.png")

#print("\n" + "="*60)
#print("Monthly Summary:")
#print("="*60)
#for i, (idx, row) in enumerate(monthly_analysis.iterrows()):
#    print(f"{month_labels[i]}: {int(row['Order Count'])} orders, ₹{row['Total Revenue']:,.2f}, Profit: ₹{row['Total Profit']:,.2f}")
#print("="*60)

# 2. ALSO GENERATE A DEDICATED PROFIT CHART
#fig2, ax_p = plt.subplots(figsize=(14, 7))

#ax_p.set_xlabel('Month', fontsize=13, fontweight='bold')
#ax_p.set_ylabel('Total Profit (₹)', fontsize=13, fontweight='bold', color='green')
#ax_p.plot(range(len(monthly_analysis)), monthly_analysis['Total Profit'], 
#                 color='green', marker='D', linewidth=4, markersize=12, 
#                 label='Monthly Profit')

#ax_p.tick_params(axis='y', labelcolor='green', labelsize=11)
#ax_p.set_xticks(range(len(monthly_analysis)))
#ax_p.set_xticklabels(month_labels, fontsize=12, fontweight='bold')
#ax_p.grid(True, alpha=0.3, linestyle='--')

# Add value labels for profit
#for i, v in enumerate(monthly_analysis['Total Profit']):
#    ax_p.text(i, v + (monthly_analysis['Total Profit'].max() * 0.05), f'₹{v:,.0f}', 
#             ha='center', fontsize=12, fontweight='bold', color='green',
#             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
#                      edgecolor='green', linewidth=2))

#plt.title('Amudham Naturals - Monthly Profit Trend', fontsize=18, fontweight='bold', pad=25)
#ax_p.set_ylim(0, monthly_analysis['Total Profit'].max() * 1.25)

#plt.tight_layout()
#plt.savefig('/Users/senthilpalanivelu/Desktop/google_analytics/monthly_profit_chart.png', dpi=300, bbox_inches='tight')
#print("\n✓ Profit line chart saved: monthly_profit_chart.png")
