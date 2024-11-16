import streamlit as st
import pandas as pd
import sqlite3
import firebase_admin
from firebase_admin import credentials, firestore


# Run this part only once after running the website
if not firebase_admin._apps:
    cred = credentials.Certificate('sql-learn-fa3e6-0f8947c48904.json') 
    default_app = firebase_admin.initialize_app(cred)


# Initialize Firestore client
db = firestore.client()

# Study Modules Content with scrolling for Experiment 1, Experiment 2, and Experiment 3
study_modules = {}

def get_all_documents(collection_name):
    try:
        # Get all documents in the specified collection
        docs = db.collection(collection_name).stream()
        
        # Step 4: Iterate through the documents and access their fields
        for doc in docs:
            # print(f'Document ID: {doc.id} => Document Data: {doc.to_dict().get('Name')}')
            study_modules[str(doc.id)+": "+doc.to_dict().get('Name')] = doc.to_dict().get('Content')
        print(study_modules)
            
    except Exception as e:
        print('Error getting documents:', e)

# Call the function with your collection name
get_all_documents('experiments')

# Database connection
conn = sqlite3.connect('data/world.sqlite')
c = conn.cursor()

# SQL Execution Function
def sql_executor(raw_code):
    try:
        c.execute(raw_code)
        data = c.fetchall()
        return data
    except sqlite3.Error as e:
        return f"An error occurred: {e}"

# Table information for reference
city = ['ID,', 'Name,', 'CountryCode,', 'District,', 'Population']
country = ['Code,', 'Name,', 'Continent,', 'Region,', 'SurfaceArea,', 'IndepYear,', 'Population,', 'LifeExpectancy,', 'GNP,', 'GNPOld,', 'LocalName,', 'GovernmentForm,', 'HeadOfState,', 'Capital,', 'Code2']
countrylanguage = ['CountryCode,', 'Language,', 'IsOfficial,', 'Percentage']

# Main Function
def main():
    # Add custom CSS to increase the width of the page
    st.markdown(
        """
        <style>
        /* Increase width of the page */
        .block-container {
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            max-width: 1200px;  /* Increase max width of the page */
            margin-left: auto;
            margin-right: auto;
        }
        /* Increase width of the sidebar */
        .css-1d391kg {
            width: 300px; /* Increase sidebar width */
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("Fr. Conceicao Rodrigues College of Engineering")

    # Sidebar with buttons to navigate to different sections
    menu = ["Home", "Study Modules", "About"]
    choice = st.sidebar.radio("Select a section:", menu)

    # Home Page Layout
    if choice == "Home":
        st.subheader("Virtual Lab")

        # Columns/Layout for Home Page with increased column width
        col1, col2 = st.columns([3, 4])  # Increased width of both columns

        with col1:
            with st.form(key='query_form'):
                raw_code = st.text_area("SQL Code Here")
                submit_code = st.form_submit_button("Execute")

            # Table of Info
            with st.expander("Table Info"):
                table_info = {'city': city, 'country': country, 'countrylanguage': countrylanguage}
                st.json(table_info)

        # Results Layout
        with col2:
            if submit_code:
                st.info("Query Submitted")
                st.code(raw_code)

                # Execute the query and show results
                query_results = sql_executor(raw_code)
                with st.expander("Results"):
                    st.write(query_results)

                with st.expander("Pretty Table"):
                    query_df = pd.DataFrame(query_results)
                    st.dataframe(query_df)

    # Study Modules Page Layout
    elif choice == "Study Modules":
        # Create columns for layout (description left, compiler right) with increased width
        col1, col2 = st.columns([3, 4])  # Increased width of both columns

        with col1:
            # Display each study module with description
            st.subheader("Experiments")
            for module, description in study_modules.items():
                with st.expander(module):  # Collapsible section for each module
                    st.markdown(description, unsafe_allow_html=True)

        with col2:
            # SQL Query Section for the study modules page
            st.subheader("SQL Query Section")
            with st.form(key='query_form_module'):
                raw_code = st.text_area("Enter your SQL code here:")
                submit_code = st.form_submit_button("Execute SQL")

            with st.expander("Table Info"):
                table_info = {'city': city, 'country': country, 'countrylanguage': countrylanguage}
                st.json(table_info)

            if submit_code:
                st.info("Query Submitted")
                st.code(raw_code)

                # Execute and display results
                query_results = sql_executor(raw_code)
                with st.expander("Results"):
                    st.write(query_results)

                with st.expander("Pretty Table"):
                    query_df = pd.DataFrame(query_results)
                    st.dataframe(query_df)

    # About Section
    elif choice == "About":
        st.subheader("About")
        st.text("SQL Virtual Lab")

if __name__ == '__main__':
    main()
