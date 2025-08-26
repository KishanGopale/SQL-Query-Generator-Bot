import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyBs2UnMNkx7okr_MvmVcoM1Waz4R4GxZDA"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def main():
    st.set_page_config(page_title="SQL Query Generator", page_icon=":robot:")
    st.markdown(
        """ <div style="text-align: center;">
                <h1>SQL Query Generator</h1>
                <h3>I can generate Sql queries for you</h3>
                <h4>with Explanation as well<h4>
                <p>this tool is a simple tool that allows you to generate SQL queries based on your input.</p>
        """,
        unsafe_allow_html=True,
    ) 

    text_input = st.text_area("Enter your Query here in plain english:", height=150)


    submit = st.button("Generate SQL Query")
    if submit:
        with st.spinner("Generating SQL Query..."):
            template = """
               Create a SQL query snippet for using the below test:
               
               ```
               {text_input}
               ```
               I just want a SQL Query.
               
               """
            formatted_template = template.format(text_input=text_input)

            response = model.generate_content(formatted_template)
            sql_query = response.text
            sql_query = sql_query.strip().lstrip("```sql").rstrip("```")

            expected_output = """
               What would be the expected of this SQL query snippet:
               
               ```
               {sql_query}
               ```
               provide sample tabular response with no explanation.
               
               """
            expected_output_fromatted = expected_output.format(sql_query=sql_query)
            eoutput = model.generate_content(expected_output_fromatted)
            eoutput = eoutput.text

            explanation = """
               Explain this SQL query snippet:
               
               ```
               {sql_query}
               ```
               please provide with simple of explanation:
               
               """
            explanation_fromatted = explanation.format(sql_query=sql_query)
            explanation = model.generate_content(explanation_fromatted)
            explanation = explanation.text

            with st.container():
                st.success("SQL Query Generated Successfully! here is your query below:")
                st.code(sql_query, language='sql')

                st.success("Expected Output of this SQL Query will be:")
                st.markdown(eoutput)

                st.success("Explanation of this SQL Query is:")
                st.markdown(explanation)


main()