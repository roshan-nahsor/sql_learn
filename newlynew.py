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

# Study Modules Content with scrolling for Experiment 1, Experiment 2, and Experiment 3
study_modules = {
    "Experiment 1: DDL": """
        <div style="max-height: 400px; overflow-y: scroll; padding-right: 10px;">
        DDL (Data Definition Language) commands form the backbone of database management and are crucial for defining, modifying, and organizing the structure of database objects.<br><br>
        
        Key Characteristics of DDL:<br>
        ● Schema-Focused: DDL commands modify the schema (structure) of a database, not the actual data within the tables.<br>
        ● Immediate Effect: Changes made using DDL commands are applied immediately and automatically committed in most databases, meaning the changes cannot be rolled back unless explicitly handled.<br>
        ● Data Safety: DDL commands do not alter the data directly but impact the tables or objects holding the data.<br><br>

        DDL Commands:<br>
        1. CREATE<br>
        &nbsp;&nbsp;&nbsp;&nbsp;● Purpose: Creates new database objects such as tables, indexes, views, or entire databases.<br><br>
        2. DROP<br>
        &nbsp;&nbsp;&nbsp;&nbsp;● Purpose: Permanently removes an existing object (such as a table, view, or database) from the database.<br><br>
        3. ALTER<br>
        &nbsp;&nbsp;&nbsp;&nbsp;● Purpose: Modifies the structure of existing database objects, allowing you to add, modify, or remove columns.<br><br>
        4. TRUNCATE<br>
        &nbsp;&nbsp;&nbsp;&nbsp;● Purpose: Removes all data from a table without deleting the table itself. This operation is faster than DELETE and resets the table storage.<br><br>
        5. COMMENT<br>
        &nbsp;&nbsp;&nbsp;&nbsp;● Purpose: Adds descriptive comments to database objects, helping improve code readability and documentation.<br><br>
        6. RENAME<br>
        &nbsp;&nbsp;&nbsp;&nbsp;● Purpose: Renames existing database objects, such as tables or columns.<br>
        </div>
    """,
    "Experiment 2: DML": """
        <div style="max-height: 400px; overflow-y: scroll; padding-right: 10px;">
        Data Manipulation Language (DML) refers to the subset of SQL commands that manage and manipulate data stored within database tables.<br><br>

        Key Characteristics of DML:<br>
        ● Data-Focused: DML commands work with the data stored in tables, allowing users to add, modify, or remove data.<br>
        ● Transaction Control: DML operations can be committed or rolled back, making them integral for transactions that ensure data integrity.<br>
        ● Conditional Operations: DML commands often include WHERE clauses to target specific rows for updates or deletions.<br><br>

        DML Commands:<br>
        1. INSERT<br>
        &nbsp;&nbsp;&nbsp;&nbsp;● Purpose: Adds new records to a table.<br><br>
        2. UPDATE<br>
        &nbsp;&nbsp;&nbsp;&nbsp;● Purpose: Modifies existing data in one or more rows of a table.<br><br>
        3. DELETE<br>
        &nbsp;&nbsp;&nbsp;&nbsp;● Purpose: Removes one or more records from a table based on a condition.<br>
        </div>
    """,
    "Experiment 3: Joins": """
        <div style="max-height: 400px; overflow-y: scroll; padding-right: 10px;">
        Key Characteristics of JOINS:<br>
        ● Relational Data Access: JOINS are essential for querying and analyzing data relationships in a normalized database.<br>
        ● Complexity Levels: JOINS range from basic (simple inner and outer joins) to advanced (e.g., cross joins, self joins, and full joins).<br>
        ● Performance Considerations: Efficient use of JOINS can enhance query performance, while improper use can slow down operations.<br><br>

        Basic JOINS:<br>
        1. INNER JOIN<br>
        &nbsp;&nbsp;&nbsp;&nbsp;○ Purpose: Returns only the rows where there is a match in both tables.<br><br>
        2. LEFT (OUTER) JOIN<br>
        &nbsp;&nbsp;&nbsp;&nbsp;● Purpose: Returns all rows from the left table, along with matched rows from the right table. Unmatched rows from the left table will have NULL in columns from the right table.<br><br>
        3. RIGHT (OUTER) JOIN<br>
        &nbsp;&nbsp;&nbsp;&nbsp;● Purpose: Returns all rows from the right table, with matched rows from the left table. Unmatched rows from the right table have NULL in columns from the left table.<br><br>
        4. FULL (OUTER) JOIN<br>
        &nbsp;&nbsp;&nbsp;&nbsp;● Purpose: Returns all records when there is a match in either the left or right table. Unmatched records from both tables will be included with NULL values for non-matching columns.<br><br>
        5. CROSS JOIN<br>
        &nbsp;&nbsp;&nbsp;&nbsp;● Purpose: Returns the Cartesian product of both tables, combining each row from the first table with all rows from the second table.<br>
        </div>
    """,
    
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

    st.title("Fr. Conceicao Rodrigues College of Engineering")

    # Sidebar with buttons to navigate to different sections
    menu = ["Home", "Study Modules", "About"]
    choice = st.sidebar.radio("Select a section:", menu)

    # Home Page Layout
    if choice == "Home":
        st.subheader("Virtual Lab")

        # # Columns/Layout for Home Page with increased column width
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
        st.subheader("Experiments")

        # Create columns for layout (description left, compiler right) with increased width
        col1, col2 = st.columns([3, 4])  # Increased width of both columns

        with col1:
            # Display each study module with description
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
