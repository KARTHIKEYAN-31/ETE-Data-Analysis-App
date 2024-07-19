import streamlit as st
import pandas as pd




@st.experimental_fragment
def update_dtype():
    if st.button("Update Data Types"):
        for i in range(len(data_type)):
            try:
                st.session_state.table[data_type.index[i]] = st.session_state.table[data_type.index[i]].astype(new_data_type_list[i])
                # st.toast(f"Updated {data_type.index[i]} to {new_data_type_list[i]}")
            except Exception as e:
                # st.write(data_type.index[i])
                st.error(e)
        st.rerun()

@st.experimental_fragment
def reset_data():
    if st.button("Reset Data"):
        st.session_state.table = st.session_state.temp_table
        st.rerun()
        
                


def suggest_dtypes(column):
    suggestions = []
    # Check if all values are integers
    if pd.api.types.is_integer_dtype(column):
        suggestions.append('int64')
    # Check if all values can be converted to floats
    try:
        column.astype(float)
        suggestions.append('float64')
    except:
        pass
    # Check if all values are strings
    if pd.api.types.is_string_dtype(column):
        suggestions.append('object')
    # Check if all values can be converted to datetime
    try:
        pd.to_datetime(column)
        suggestions.append('datetime64[ns]')
    except (ValueError, TypeError):
        pass
    # st.write(suggestions)
    return suggestions





if st.session_state.table is None:
    st.write("Load Table First")
    st.page_link("pages/Data Upload/dataupload.py", label= "Load Table", icon = ":material/upload:")

elif len(st.session_state.table.columns[st.session_state.table.isna().any()].tolist()) != 0:
    st.write("There are some missing values found please fill them.")
    st.page_link("pages/Data Processing/process.py", label= "Process Data", icon = ":material/account_tree:")

else:
    c1, c2 = st.columns([3,1])
    with c1:
        st.header("Assign Data Type")
    with c2:
        st.write('')
        st.write('')
        st.page_link("pages/Data Analysis/customcharts.py",
                      label= "Manual Analysis", icon = ":material/bar_chart:")  

    # st.subheader("Original Table")
    with st.expander("**Table Data**", icon = ":material/dataset:"):
        st.write('')
        st.dataframe(st.session_state.table.head(20))


    data_type = st.session_state.table.dtypes
    # data_type_list = ['int64', 'float64', 'object', 'bool', 'datetime64[ns]']
    # st.dataframe(data_type.reset_index().columns)

    st.write('')
    st.write('')
    st.write('')
    st.write('')

    c1, c2 = st.columns([2,1])
    with c1:
        st.subheader("Data Types")
    with c2:
        c21, c22 = st.columns(2)
        with c21:
            update_dtype()
        with c22:
            reset_data()

    
    new_data_type_list = list(data_type.reset_index().astype(str)[0])
    # st.write(new_data_type_list)
    # st.write(new_data_type_list)
    for i in range(len(data_type)):
        data_type_list = suggest_dtypes(st.session_state.table[data_type.index[i]])
        index = data_type.index[i]
        dtype = data_type[i]
        c1, c2, c3 = st.columns(3)

        with c1:
            st.write('')
            st.write('')
            st.write(index)

        with c2:
            st.write('')
            st.write('')
            st.write(dtype)

        with c3:
            new_data_type_list[i] = st.selectbox(index, data_type_list,
                                                 index = data_type_list.index(str(dtype)))
        
    # st.write(new_data_type_list)




