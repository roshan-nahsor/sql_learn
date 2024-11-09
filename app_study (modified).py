import streamlit as st
import pandas as pd
import sqlite3

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

# Study Modules Content
study_modules = {
    "Module 1: Introduction to SQL": "Learn the basics of SQL including SELECT, WHERE, and JOIN.",
    "Module 2: Advanced SQL Queries": "Explore complex SQL queries, subqueries, and aggregation.",
    "Module 3: Database Design": "Learn about database normalization, keys, and relational design.",
    "Module 4: SQL Optimization": "Understand query optimization techniques for better performance."
}

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

    st.title("SQL Playground")

    # Sidebar with buttons to navigate to different sections
    menu = ["Home", "Study Modules", "About"]
    choice = st.sidebar.radio("Select a section:", menu)

    # Home Page Layout
    if choice == "Home":
        st.subheader("HomePage")

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
        st.subheader("Study Modules")

        # Create columns for layout (description left, compiler right) with increased width
        col1, col2 = st.columns([3, 4])  # Increased width of both columns

        with col1:
            # Display each study module with description
            for module, description in study_modules.items():
                with st.expander(module):  # Collapsible section for each module
                    st.write(description)

        with col2:
            # SQL Query Section for the study modules page
            st.subheader("SQL Query Section")
            with st.form(key='query_form_module'):
                raw_code = st.text_area("Enter your SQL code here:")
                submit_code = st.form_submit_button("Execute SQL")

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

    # About Page Layout
    elif choice == "About":
        st.subheader("About")
        st.write("This app allows you to interact with SQL queries and learn through study modules.")

# Run the app
if __name__ == '__main__':
    main()
