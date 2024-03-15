import streamlit as st
import pandas as pd
import base64

# Function to read and display file
def read_file(file):
    df = None
    if file is not None:
        if file.type == 'application/vnd.ms-excel' or file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(file)
        elif file.type == 'text/csv':
            df = pd.read_csv(file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
    return df

# Function for data manipulation
def manipulate_data(df):
    # Add your data manipulation code here
    # For now, let's just return the original DataFrame
    return df

# Function to download file
def download_file(df):
    if df is not None:
        csv_file = df.to_csv(index=False)
        b64 = base64.b64encode(csv_file.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

# Main function
def main():
    st.title('File Uploader, Manipulator, and Downloader')

    # File uploader
    file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

    if file is not None:
        st.success("File successfully uploaded!")
        df = read_file(file)

        if df is not None:
            # Option to display the imported data
            if st.checkbox("Display the imported data"):
                st.write("Imported data:")
                st.write(df)

            # Option to manipulate the data
            if st.checkbox("Manipulate the data"):
                df = manipulate_data(df)
                if st.checkbox("Display the manipulated data"):
                    st.write("Data after manipulation:")
                    st.write(df)

            # Option to download the file
            if st.button("Download"):
                download_file(df)

if __name__ == "__main__":
    main()
