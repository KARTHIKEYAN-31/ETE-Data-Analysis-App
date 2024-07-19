import streamlit as st
import pandas as pd


if st.session_state.table is None:
    st.write("Load Table First")
    st.page_link("pages/Data Upload/dataupload.py", label= "Load Table", icon = ":material/upload:")

else:
    st.markdown("##### Chat with Data")
    


