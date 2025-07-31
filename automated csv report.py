import pandas as pd
import io


def generate_sales_report_embedded_data():
    """
    Uses an embedded dataset to calculate total revenue,
    identifies the top product, and generates a summary report.
    """
    # Embedded dataset as a string
    sales_data_csv = """Date,Product,Units Sold,Unit Price
2025-07-01,Keyboard,5,1200
2025-07-01,Mouse,10,700
2025-07-02,Laptop,2,85000
2025-07-03,Keyboard,3,1200
2025-07-03,Mouse,5,700
2025-07-04,Monitor,1,15000
2025-07-04,Keyboard,2,1200
"""
    try:
        # Read the data using pandas from the string
        df = pd.read_csv(io.StringIO(sales_data_csv))

        # Ensure necessary columns exist (though with embedded data, we control this)
        if not all(col in df.columns for col in ['Product', 'Units Sold', 'Unit Price']):
            return "Error: Required columns 'Product', 'Units Sold', or 'Unit Price' are missing in the embedded data."

        # Calculate revenue for each product
        df['Revenue'] = df['Units Sold'] * df['Unit Price']

        # Calculate total revenue
        total_revenue = df['Revenue'].sum()

        # Group by product to get individual product revenues
        product_revenue = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False)

        # Identify the top product
        top_product = product_revenue.index[0]

        # Prepare the report content
        report_content = "📊 Sales Summary\n"
        for product, revenue in product_revenue.items():
            report_content += f"Product: {product} – Revenue: {revenue}\n"

        report_content += f"\n🔸 Total Revenue: {total_revenue}\n"
        report_content += f"🔸 Top Product: {top_product}\n"

        # Save the report to report.txt with UTF-8 encoding
        with open('report.txt', 'w', encoding='utf-8') as f:  # <--- CHANGE IS HERE
            f.write(report_content)

        return "Report generated successfully as report.txt"

    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    print(generate_sales_report_embedded_data())