import streamlit as st
import pandas as pd

st.set_page_config(
    layout="wide"
)


if 'table' not in st.session_state:
    st.session_state.table = None
if 'tbale_copy' not in st.session_state:
    st.session_state.tbale_copy = None
if 'temp_table' not in st.session_state:
    st.session_state.temp_table = None
if 'vlaue' not in st.session_state:
    st.session_state.vlaue = None


pages = {
    "Data Upload":[
        st.Page("pages/Data Upload/dataupload.py", title = "Data Upload", icon = ":material/upload:", default = True)
    ],
    "Data Processing":[
        st.Page("pages/Data Processing/process.py", title = "Data Process", icon = ":material/account_tree:"),
        st.Page("pages/Data Processing/datatype.py", title = "Data Type", icon = ":material/123:")
    ],
    "Data Analysis":[
        st.Page("pages/Data Analysis/customcharts.py", title = "Custom Charts", icon = ":material/bar_chart:"),
        st.Page("pages/Data Analysis/pygwalker.py", title = "PyGwalker", icon = ":material/analytics:"),
        st.Page("pages/Data Analysis/autoanalysis.py", title = "Auto Analysis", icon = ":material/auto_transmission:"),
        st.Page("pages/Data Analysis/chatbot.py", title = "Chatbot", icon = ":material/chat:")
    ]
}


st.title("Easy Analytics")


pages = st.navigation(pages)
pages.run()

# st.markdown('''
# ### Welcome to Easy Analytics

# The application contains 3 parts:
# 1. **Data Upload**
# 2. **Data Processing**
# 3. **Data Analysis**

# ### How to use

# 1. **Data Upload**
#     - Select Data Source
#     - Upload Data
#     - Navigate to Data Processing page

# 2. **Data Processing**
#     - Select Data Type
#     - Process Data
#     - Navigate to Data Analysis page

# 4. **Data Analysis**
#     - Explore different charts and graphs
#     - Run Auto analysis to get best corrilated features
#     - Chat with Bot about the Data
# ''')



