# Analytics & Visualization Guide

This guide explains the statistical methods and visualizations used in the **Profit Distribution Analysis** section of the dashboard.

---

## 1. Interquartile Range (IQR) Method

The **IQR Method** is a robust statistical technique used to identifying "outliers"—data points that differ significantly from other observations. We use this to filter out extreme profit values (both high and low) to analyze your "typical" business performance.

### How It Works

1.  **Quartiles**: The data is split into four equal parts:
    *   **Q1 (25th Percentile)**: 25% of orders have profit below this value.
    *   **Q3 (75th Percentile)**: 75% of orders have profit below this value.

2.  **Calculate IQR**: The range of the middle 50% of the data.
    $$IQR = Q3 - Q1$$

3.  **Define Bounds**:
    *   **Lower Bound**: $Q1 - 1.5 \times IQR$
    *   **Upper Bound**: $Q3 + 1.5 \times IQR$

4.  **Filter**: Any order with a profit **below the Lower Bound** or **above the Upper Bound** is considered an outlier.

### Why Exclude Outliers?
*   **Skewed Averages**: A single order with ₹5000 profit (when typical is ₹50) can artificially inflate the Mean, giving a false sense of performance.
*   **Predictability**: Removing random anomalies helps identifying the stable profit margin you can rely on.

---

## 2. Visualization Types

### A. Box Plot (Mean & Variance)
**Best for**: A quick summary of the data's central tendency (median) and spread (variability).

*   **The Box**: Represents the middle 50% of data (Q1 to Q3). A shorter box means consistent profits; a tall box means high variation.
*   **The Line Inside**: The **Median** profit. 50% of orders earned more, 50% earned less.
*   **The Whiskers**: Extend to show the range of the rest of the data.
*   **Dots**: Individual outliers (if not excluded).

### B. Histogram (Frequency Distribution)
**Best for**: Seeing "how many" orders fall into specific profit ranges.

*   **Bars**: Each bar represents a profit range (e.g., ₹50-₹60). The height shows the *count* of orders in that range.
*   **Peak**: The tallest bar is the "Mode"—the most common profit outcome.
*   **Skew**:
    *   Long tail to the right = Frequent low profits, occasional high profits.
    *   Long tail to the left = Frequent high profits, occasional losses.

### C. Violin Plot (Density)
**Best for**: visualizing the "shape" of the data distribution.

*   **Width**: The thicker the violin at a certain profit level, the more likely that profit is to occur.
*   **Shape**: Unlike a box plot, it reveals if data is "bimodal" (e.g., two distinct peaks—one for small items, one for bulk items).

### D. Cumulative (ECDF)
**Best for**: Answering "What percentage of orders are below ₹X?"

*   **X-Axis**: Profit Value.
*   **Y-Axis**: Probability (0 to 1, or 0% to 100%).
*   **Example**: If you look at ₹100 on the X-axis, and the line is at 0.8 on the Y-axis, it means **80% of your orders earn ₹100 or less**.

---

## 3. Statistical Metrics Glossary

| Metric | Description | Interpretation |
| :--- | :--- | :--- |
| **Mean** | Average Profit | The sum of all profits divided by the count. Sensitive to outliers. |
| **Median** | Middle Value | The exact middle profit value. Robust against outliers. |
| **Std Deviation** | Spread | Average difference from the Mean. High SD = Volatile profits. |
| **Skewness** | Asymmetry | **> 0**: Long tail of high profits. **< 0**: Long tail of low profits/losses. |
| **Variation (CV)** | Relative Spread | (Std Dev / Mean) * 100. **> 100%**: Highly unpredictable. **< 20%**: Very consistent. |
