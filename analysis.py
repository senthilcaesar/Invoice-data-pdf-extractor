import pandas as pd

df = pd.read_csv("/Users/senthilpalanivelu/Desktop/google_analytics/all_invoices.csv")

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
df['Invoice Value'] = pd.to_numeric(
    df['Invoice Value'].str.replace(',', '', regex=False),
    errors='coerce'
)
print(f"✓ Invoice Value converted to numeric")

# Extract date components
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Day'] = df['Order Date'].dt.day
df['DayOfWeek'] = df['Order Date'].dt.day_name()
df['WeekOfYear'] = df['Order Date'].dt.isocalendar().week
print(f"✓ Date components extracted")

# Clean Place of Delivery
df['State'] = df['Place of Delivery'].str.strip().str.upper()
print(f"✓ State names standardized")


print("\n\n3. DESCRIPTIVE STATISTICS")
print("-"*80)
print(f"\nInvoice Value Statistics:")
print(df['Invoice Value'].describe())

print(f"\nTotal Revenue: ₹{df['Invoice Value'].sum():,.2f}")

print("\n\n5. GEOGRAPHICAL ANALYSIS")
print("-"*80)

state_analysis = df.groupby('State').agg({
    'Invoice Value': ['count', 'sum']
}).round(6)

state_analysis.columns = ['Order Count', 'Total Revenue']
state_analysis = state_analysis.sort_values('Total Revenue', ascending=False)

print(f"\nState-wise Performance:")
print(state_analysis)

print("\n\n6. TEMPORAL ANALYSIS")
print("-"*80)

# Monthly trend
monthly_analysis = df.groupby(['Year', 'Month']).agg({
    'Invoice Value': ['count', 'sum']
}).round(2)
monthly_analysis.columns = ['Order Count', 'Total Revenue']

print(f"\nMonthly Trend:")
print(monthly_analysis)

df.groupby(['Year', 'Month'])['Invoice Value'].sum().reset_index()

df.groupby(['Year', 'Month'])['Invoice Value'].count().reset_index()

df.groupby(['Year', 'Month'])['Invoice Value'] \
  .agg(Order_Count='count', Total_Revenue='sum') \
  .reset_index()

import pandas as pd
import matplotlib.pyplot as plt

# Load and prepare data
df = pd.read_csv('/Users/senthilpalanivelu/Desktop/google_analytics/all_invoices.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d.%m.%Y', errors='coerce')
df['Invoice Value'] = pd.to_numeric(
    df['Invoice Value'].str.replace(',', '', regex=False),
    errors='coerce'
)
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month

# Monthly trend
monthly_analysis = df.groupby(['Year', 'Month']).agg({
    'Invoice Value': ['count', 'sum']
}).round(2)
monthly_analysis.columns = ['Order Count', 'Total Revenue']

print("\nMonthly Trend:")
print(monthly_analysis)

# Create month labels
month_labels = []
for idx in monthly_analysis.index:
    year, month = idx
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_labels.append(f"{month_names[month-1]} {year}")

# Create simple line chart
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
ax1.set_xticklabels(month_labels, fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3, linestyle='--')

# Add value labels for orders - positioned ABOVE the line
for i, v in enumerate(monthly_analysis['Order Count']):
    ax1.text(i, v + 2.5, str(int(v)), ha='center', fontsize=12, 
             fontweight='bold', color=color1,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                      edgecolor=color1, linewidth=2))

# Plot revenue on right axis (ORANGE)
ax2 = ax1.twinx()
color2 = 'darkorange'
ax2.set_ylabel('Total Invoice Sum (₹)', fontsize=13, fontweight='bold', color=color2)
line2 = ax2.plot(range(len(monthly_analysis)), monthly_analysis['Total Revenue'], 
                 color=color2, marker='s', linewidth=3, markersize=12, 
                 label='Total Revenue')
ax2.tick_params(axis='y', labelcolor=color2, labelsize=11)

# Add value labels for revenue - positioned BELOW the line
for i, v in enumerate(monthly_analysis['Total Revenue']):
    ax2.text(i, v - 600, f'₹{v:,.0f}', ha='center', fontsize=12, 
             fontweight='bold', color=color2,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                      edgecolor=color2, linewidth=2))

# Title
plt.title('Amudham Naturals - Monthly Orders and Revenue', fontsize=18, fontweight='bold', pad=25)

# Legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=12, frameon=True)

# Add some padding to y-axes to prevent label cutoff
ax1.set_ylim(0, monthly_analysis['Order Count'].max() * 1.15)
ax2.set_ylim(0, monthly_analysis['Total Revenue'].max() * 1.12)

plt.tight_layout()
plt.savefig('/Users/senthilpalanivelu/Desktop/google_analytics/simple_monthly_chart_improved.png', dpi=300, bbox_inches='tight')
print("\n✓ Improved line chart saved: simple_monthly_chart_improved.png")

print("\n" + "="*60)
print("Monthly Summary:")
print("="*60)
for i, (idx, row) in enumerate(monthly_analysis.iterrows()):
    print(f"{month_labels[i]}: {int(row['Order Count'])} orders, ₹{row['Total Revenue']:,.2f}")
print("="*60)