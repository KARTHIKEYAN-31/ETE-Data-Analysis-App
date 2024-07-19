import streamlit as st
import pygwalker as pyg
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer


pyg_app = StreamlitRenderer(st.session_state.table)
 
pyg_app.explorer()