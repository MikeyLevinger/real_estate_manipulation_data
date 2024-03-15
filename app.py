import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to read and manipulate data
def manipulate_data(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file, skiprows=1)  # Skip the first row as it contains column headers
    else:
        st.error("Unsupported file format. Please upload a CSV file.")
        return None

    # Check if 'Unit' column exists in the DataFrame
    if 'Unit' not in df.columns:
        st.error("Column 'Unit' not found in the uploaded file.")
        return None

    # Drop rows where 'Unit' is NaN
    df = df.dropna(subset=['Unit'])

    # Remove unnecessary columns
    df = df.drop(columns=['Sqft', 'Recurring Charges', 'Annual Rent / SF', 'Deposit'])

    # Convert 'Lease From' and 'Lease To' to datetime
    df['Lease Start Date'] = pd.to_datetime(df['Lease From'], errors='coerce')
    df['Lease End Date'] = pd.to_datetime(df['Lease To'], errors='coerce')

    # Calculate Property % SF
    df['Property % SF'] = df['Square Feet'] / df['Square Feet'].sum() * 100

    return df

# Function for predictive visualizations
def predictive_visualizations(df):
    # Histogram of Lease Duration
    st.subheader("Histogram of Lease Duration")
    plt.hist(df['Lease End Date'] - df['Lease Start Date'], bins=10, color='skyblue', edgecolor='black')
    plt.xlabel('Lease Duration')
    plt.ylabel('Frequency')
    plt.title('Distribution of Lease Duration')
    st.pyplot()

# Function for business insights
def business_insights(df):
    st.subheader("Business Insights")
    # Example 1: Average Rent per Square Foot
    avg_rent_per_sf = df['Rent'].sum() / df['Square Feet'].sum()
    st.write(f"The average rent per square foot is ${avg_rent_per_sf:.2f}.")

    # Example 2: Occupancy Rate
    occupancy_rate = len(df[df['Lease End Date'] > pd.Timestamp.now()]) / len(df) * 100
    st.write(f"The occupancy rate is {occupancy_rate:.2f}%.")

    # Example 3: Top Tenants by Rent
    st.write("Top Tenants by Rent:")
    top_tenants = df.groupby('Tenant')['Rent'].sum().nlargest(10)
    st.write(top_tenants)

# Main function
def main():
    st.title('Real Estate Data Manipulation')

    # File uploader
    file = st.file_uploader("Upload a file", type=["csv"])

    if file is not None:
        st.success("File successfully uploaded!")
        df = manipulate_data(file)

        if df is not None:
            # Display manipulated data
            st.write("Manipulated data:")
            st.write(df)

            # Predictive visualizations
            predictive_visualizations(df)

            # Business insights
            business_insights(df)

if __name__ == "__main__":
    main()
