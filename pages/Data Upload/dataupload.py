import pandas as pd
import streamlit as st


def clear_table():
    st.session_state.table = None
    st.session_state.tbale_copy = None



st.title("Upload Data")

if st.session_state.table is not None:
    c1, c2 = st.columns(2)
    with c1:
        st.success("Table Already Loaded")
    with c2:
        c21, c22 = st.columns([1,2])
        with c21:
            st.write("To Load New Table: ")
        with c22:
            st.button("Load Table", on_click=clear_table)

    with st.expander("**Table Data**", icon = ":material/dataset:"):
        st.dataframe(st.session_state.table.head(20))

    
    

else:
    ds = st.selectbox("Select DataSource", ("", "CSV file / URL", "Google Sheet URL", "Hana Table"))
    
    if ds == "CSV file / URL":
        c1, c2 = st.columns(2)
        with c1:
            file = st.file_uploader("Upload CSV", type=["csv"])
            if file is not None:
                st.session_state.table = pd.read_csv(file)
        with c2:
            url = st.text_input("URL", value="https://")
            if url is not None and not "https://":
                try:
                    st.session_state.table = pd.read_csv(url)
                except Exception as e:
                    st.error(e)
        
if st.session_state.table is not None:
    st.session_state.tbale_copy = st.session_state.table.copy()
    st.session_state.temp_table = st.session_state.table.copy()

    st.write("Table Loaded Successfully")
    st.page_link("pages/Data Processing/process.py", label= "Process Data", icon = ":material/account_tree:")
    # st.switch_page("pages/Data Processing/datatype.py")

    # pg = st.navigation([
    #     st.Page("pages/datatype.py", title= "Check Data Type", icon = ":material/123:"),
    # ])
    # pg.run()