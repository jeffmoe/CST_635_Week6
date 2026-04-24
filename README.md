# Advanced Exploratory Data Analysis (EDA) App
An interactive, all-in-one web application for **Exploratory Data Analysis (EDA)** built with **Streamlit**. It combines manual visualizations (using Matplotlib & Seaborn) with an automated profiling report (ydata-profiling).

## Table of Contents

- Project Overview
- Features
- Technology
- Visualization Methods
- Project Structure
- Getting Started
- License

---

## Project Overview

This application provides a comprehensive solution for Exploratory Data Analysis with two approaches:

1. **Manual EDA** – Interactive visualizations where users can select columns and customize plots
2. **Automated EDA** – Using `ydata-profiling` to generate a complete report with one click

The tool handles both **numeric** and **categorical** data, providing insights into:
- Data distribution and skewness
- Missing values patterns
- Outlier detection
- Correlation between variables
- High cardinality in categorical variables

---

## Features

### Core Features

| Feature | Description |
|---------|-------------|
| **Dataset Overview** | Preview data, summary statistics, and column data types |
| **Numerical Visualizations** | Histograms with KDE, box plots, violin plots |
| **Categorical Visualizations** | Count plots and bar plots with target column segregation |
| **Correlation & Heatmaps** | Interactive correlation heatmaps and pair plots |
| **Missing Value Analysis** | Missing value counts and heatmap visualization |
| **Outlier Detection** | IQR-based outlier detection and boxplot visualization |
| **Auto EDA Report** | Generate an automated, interactive EDA report |
| **Key Takeaways** | Automatic insights on missing values, skewness, high correlation, outliers, and cardinality |

### Automatic Insights Generated

- Missing values detection with column names and counts
- Skewness analysis (identifying columns with |skewness| > 1)
- High correlation pairs (|correlation| > 0.7)
- Outlier detection using IQR method (1.5× IQR rule)
- Cardinality analysis for categorical columns (>10 unique values)

---

## Technology

| Component | Technology |
|-----------|-----------|
| **Frontend & Backend** | Streamlit |
| **Data Manipulation** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Auto EDA** | ydata-profiling (formerly pandas-profiling) |
| **Environment** | Python 3.8+ |

---

## Visualization Methods

The app implements various visualization techniques as outlined in the course material:

### Numeric Column Visualizations
| Plot Type | Seaborn Function |
|-----------|-----------------|
| Histogram with KDE | `sns.histplot(df[col], kde=True)` |
| Box Plot | `sns.boxplot(x=df[col])` |
| Violin Plot | `sns.violinplot(x=df[col])` |
| Pair Plot | `sns.pairplot(df[numeric_cols])` |

### Categorical Visualizations
| Plot Type | Seaborn Function |
|-----------|-----------------|
| Count Plot | `sns.countplot(y=df[col], hue=df[target_col])` |
| Bar Plot | `sns.barplot(x=df[col], y=df[num_col], hue=df[target_col])` |

### Correlation & Statistical Plots
| Plot Type | Seaborn/Matplotlib Function |
|-----------|----------------------------|
| Correlation Heatmap | `sns.heatmap(df.corr(), annot=True, cmap="coolwarm")` |
| Missing Values Heatmap | `sns.heatmap(df.isnull(), cbar=False, cmap="viridis")` |

---

## Project Structure
advanced-eda-app/  
├── EDA_app.py Main Streamlit application  
├── requirements.txt Python dependencies  
├── README.md Project documentation (this file)  
└── LICENSE MIT License  

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/advanced-eda-app.git  
cd advanced-eda-app  
```
### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  
```
### 3. Download requirements

```bash
pip install -r requirements.txt 
```
### 4. Run the app

```bash
streamlit run EDA_app.py 
```
---

## License  

This project is licensed under the MIT License - see the LICENSE file for details.
