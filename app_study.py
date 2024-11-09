import streamlit as st
import pandas as pd
import sqlite3

# Database connection
conn = sqlite3.connect('data/world.sqlite')
c = conn.cursor()

# SQL Execution Function
def sql_executor(raw_code):
    c.execute(raw_code)
    data = c.fetchall()
    return data

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
    st.title("SQL Playground")

    # Sidebar menu with Home, About, and Study Modules
    menu = ["Home", "About", "Study Modules"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Home Page Layout
    if choice == "Home":
        st.subheader("HomePage")

        # Columns/Layout
        col1, col2 = st.columns(2)  # Updated method here

        with col1:
            with st.form(key='query_form'):
                raw_code = st.text_area("SQL Code Here")
                submit_code = st.form_submit_button("Execute")

            # Table of Info
            with st.expander("Table Info"):  # Use expander instead of beta_expander
                table_info = {'city': city, 'country': country, 'countrylanguage': countrylanguage}
                st.json(table_info)

        # Results Layouts
        with col2:
            if submit_code:
                st.info("Query Submitted")
                st.code(raw_code)

                # Results 
                query_results = sql_executor(raw_code)
                with st.expander("Results"):  # Use expander instead of beta_expander
                    st.write(query_results)

                with st.expander("Pretty Table"):  # Use expander instead of beta_expander
                    query_df = pd.DataFrame(query_results)
                    st.dataframe(query_df)

    # Study Modules Page (with description on the left and compiler on the right)
    elif choice == "Study Modules":
        st.subheader("Study Modules")

        # Create columns for layout (description left, compiler right)
        col1, col2 = st.columns([1, 2])  # Left column for module description, right for SQL compiler

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

                # SQL Results
                query_results = sql_executor(raw_code)
                with st.expander("Results"):
                    st.write(query_results)

                with st.expander("Pretty Table"):
                    query_df = pd.DataFrame(query_results)
                    st.dataframe(query_df)

    # About Page
    else:
        st.subheader("About")
        st.write("This app allows you to interact with SQL queries and learn through study modules.")

# Run the app
if __name__ == '__main__':
    main()
