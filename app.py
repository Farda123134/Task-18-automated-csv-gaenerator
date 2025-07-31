import streamlit as st
import pandas as pd
import io


def generate_sales_report(df):
    """
    Calculates total revenue, identifies the top product,
    and returns a summary report string.
    """
    # Ensure necessary columns exist
    if not all(col in df.columns for col in ['Product', 'Units Sold', 'Unit Price']):
        return "Error: CSV file must contain 'Product', 'Units Sold', and 'Unit Price' columns."

    # Convert columns to appropriate types
    try:
        df['Units Sold'] = pd.to_numeric(df['Units Sold'], errors='coerce')
        df['Unit Price'] = pd.to_numeric(df['Unit Price'], errors='coerce')
        df.dropna(subset=['Units Sold', 'Unit Price'], inplace=True)  # Remove rows with NaN after coercion
    except Exception as e:
        return f"Error: Could not convert 'Units Sold' or 'Unit Price' to numeric. Please check your data. ({e})"

    # Calculate revenue for each product
    df['Revenue'] = df['Units Sold'] * df['Unit Price']

    # Calculate total revenue
    total_revenue = df['Revenue'].sum()

    # Group by product to get individual product revenues
    product_revenue = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False)

    # Identify the top product
    top_product = product_revenue.index[0] if not product_revenue.empty else "N/A"

    # Prepare the report content
    report_content = "### 📊 Sales Summary\n"
    for product, revenue in product_revenue.items():
        report_content += f"- **Product**: {product} – **Revenue**: ${revenue:,.2f}\n"

    report_content += f"\n### 💰 Total Revenue: ${total_revenue:,.2f}\n"
    report_content += f"### 🔝 Top Product: {top_product}\n"

    return report_content


# --- Streamlit App Layout ---
st.set_page_config(page_title="Automated Sales Report Generator", layout="centered")

st.title("Automated Sales Report Generator 📈")
st.write("Upload your sales CSV file to generate a quick summary report.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded CSV file
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("Raw Data Preview")
        st.dataframe(df.head())

        # Generate the report
        report = generate_sales_report(df.copy())  # Pass a copy to avoid modifying original df

        if "Error" in report:
            st.error(report)
        else:
            st.markdown(report)  # Use st.markdown to render formatted text

            # Option to download the report as a text file
            st.download_button(
                label="Download Report as Text File",
                data=report,
                file_name="sales_report.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"Error processing your file: {e}. Please ensure it's a valid CSV with the required columns.")

st.markdown("---")
st.markdown("This application was created as part of the ProSensia Python Internship - Day 19 task.")