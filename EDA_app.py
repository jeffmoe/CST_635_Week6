import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(page_title="Advanced EDA App", layout="wide")
st.title("Advanced Exploratory Data Analysis App")
st.write("Upload a CSV file to explore automated and manual EDA visualizations.")


st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Dataset Overview",
        "Numerical Visualizations",
        "Categorical Visualizations",
        "Correlation & Heatmaps",
        "Missing Values",
        "Outlier Detection",
        "Auto EDA Report",
        "Key Takeaways",
    ],
)

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    def get_insights():
        insights = []
        insights.append(f'### Dataset Overview\n- **Rows:** {df.shape[0]}\n- **Columns:** {df.shape[1]}\n- **Numeric Columns:** {len(numeric_cols)}\n- **Categorical Columns:** {len(categorical_cols)}')
        missing_counts = df.isnull().sum()
        missing_cols = missing_counts[missing_counts > 0]
        if not missing_cols.empty:
            insights.append(
                f"### Missing Values\n- **Columns with Missing Values:** {', '.join(missing_cols.index.tolist())}\n"
                f"- **Highest missing count:** {missing_cols.max()} missing values in \"{missing_cols.idxmax()}\""
            )
        else:
            insights.append('### Missing Values\n- No missing values detected.')
        
        if numeric_cols:
            high_skew = []
            for col in numeric_cols:
                skewness = df[col].skew()
                if abs(skewness) > 1:
                    high_skew.append(f"{col} (skew={skewness:.2f})")
            if high_skew:
                insights.append(f'### High Skewness\n- **Columns with High Skewness:** {", ".join(high_skew)}')
            else:
                insights.append('### High Skewness\n- No numeric columns with high skewness detected.')
        
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr()
            high_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.7:
                        high_corr.append(f"{corr_matrix.columns[i]} & {corr_matrix.columns[j]} (corr={corr_matrix.iloc[i, j]:.2f})")
            if high_corr:
                insights.append(f'### High Correlation\n- **Highly Correlated Pairs:** {", ".join(high_corr)}')
            else:
                insights.append('### High Correlation\n- No highly correlated pairs detected.')

        outlier_count = 0
        outlier_cols = []
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outliers = df[(df[col] < lower) | (df[col] > upper)]
            if not outliers.empty:
                outlier_count += len(outliers)
                outlier_cols.append(f"{col} ({len(outliers)} outliers)")
        if outlier_cols:
            insights.append(f'### Outliers\n- **Total Outliers Detected:** {outlier_count}\n- **Columns with Outliers:** {", ".join(outlier_cols)}')
        else:
            insights.append('### Outliers\n- No outliers detected in numeric columns.')
        
        if categorical_cols:
            cardinality = [col for col in categorical_cols if df[col].nunique() > 10]
            if cardinality:
                insights.append(f'### High Cardinality\n- **Categorical Columns with High Cardinality:** {", ".join(cardinality)}')
            else:
                insights.append('### High Cardinality\n- No categorical columns with high cardinality detected.')
        return insights

    if page == "Dataset Overview":
        st.header("Dataset Preview")
        st.dataframe(df.head())

        st.header("Summary Statistics")
        st.write(df.describe(include="all"))

        st.header("Column Information")
        st.write(df.dtypes)


    elif page == "Numerical Visualizations":
        st.header("Numerical Column Visualizations")

        if numeric_cols:
            col = st.selectbox("Select a numeric column", numeric_cols)

            st.subheader("Histogram with KDE")
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            st.pyplot(fig)

            st.subheader("Boxplot")
            fig, ax = plt.subplots()
            sns.boxplot(x=df[col], ax=ax)
            st.pyplot(fig)

            st.subheader("Violin Plot")
            fig, ax = plt.subplots()
            sns.violinplot(x=df[col], ax=ax)
            st.pyplot(fig)
        else:
            st.warning("No numeric columns found.")


    elif page == "Categorical Visualizations":
        st.header("Categorical Column Visualizations")

        if categorical_cols:
            col = st.selectbox("Select a categorical column", categorical_cols)
            target_col = st.selectbox("Select target column for bar plot", df.columns)

            st.subheader("Count Plot")
            fig, ax = plt.subplots()
            sns.countplot(y=df[col], hue=df[target_col], order=df[col].value_counts().index, ax=ax)
            st.pyplot(fig)

            st.subheader("Bar Plot (Category vs Numeric)")
            if numeric_cols:
                num_col = st.selectbox("Select numeric column", numeric_cols)
                fig, ax = plt.subplots()
                sns.barplot(x=df[col], y=df[num_col], hue=df[target_col], ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)
            else:
                st.info("No numeric columns available for bar plot.")
        else:
            st.warning("No categorical columns found.")


    elif page == "Correlation & Heatmaps":
        st.header("Correlation Heatmap")

        if numeric_cols:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

            st.subheader("Pairplot")
            if st.checkbox("Generate Pairplot (slow for large datasets)"):
                fig = sns.pairplot(df[numeric_cols])
                st.pyplot(fig)
        else:
            st.warning("No numeric columns found.")


    elif page == "Missing Values":
        st.header("Missing Value Analysis")

        st.subheader("Missing Value Count")
        st.write(df.isnull().sum())

        st.subheader("Missing Value Heatmap")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df.isnull(), cbar=False, cmap="viridis", ax=ax)
        st.pyplot(fig)


    elif page == "Outlier Detection":
        st.header("Outlier Detection (IQR Method)")

        if numeric_cols:
            col = st.selectbox("Select numeric column", numeric_cols)

            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outliers = df[(df[col] < lower) | (df[col] > upper)]

            st.write(f"Number of outliers in **{col}**: {len(outliers)}")
            st.dataframe(outliers)

            st.subheader("Boxplot with Outliers")
            fig, ax = plt.subplots()
            sns.boxplot(x=df[col], ax=ax)
            st.pyplot(fig)
        else:
            st.warning("No numeric columns found.")


    elif page == "Auto EDA Report":
        st.header("Automated EDA Report (ydata‑profiling)")

        if st.button("Generate Report"):
            profile = ProfileReport(df, title="Auto EDA Report", explorative=True)
            st_profile_report(profile)
    
    elif page == "Key Takeaways":
        st.header("Key Takeaways")
        insights = get_insights()
        for insight in insights:
            with st.expander(insight.split("\n")[0].replace("### ", ""), expanded=True):
                st.markdown(insight)
else:
    st.info("Upload a CSV file to begin.")
