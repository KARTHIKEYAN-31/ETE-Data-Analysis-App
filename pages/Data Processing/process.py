import streamlit as st
import pandas as pd
import variables as var 
import time
import numpy as np



def get_numeric_columns():
    col = st.session_state.table.columns
    num_col = []
    for i in col:
        if pd.api.types.is_integer_dtype(st.session_state.table[i]):
            num_col.append(i)
    return num_col

def get_suggestions(column):
    column = st.session_state.table.copy()[column].dropna()
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
    return suggestions

def get_fill_fun_name(i):
    data_type = str(st.session_state.table.dtypes[i])
    # st.write(data_type)
        
    methods = {
        'object': [
            "Fill with a specific object",
            "Forward fill",
            "Backward fill",
            "Delete rows"
        ],
        'int64': [
            "Fill with a specific value",
            "Fill with mean",
            "Fill with median",
            "Fill with mode",
            "Interpolate",
            "Delete rows"
        ],
        'float64': [
            "Fill with a specific value",
            "Fill with mean",
            "Fill with median",
            "Fill with mode",
            "Interpolate",
            "Delete rows"
        ],
        'datetime64[ns]': [
            "Fill with a specific date",
            "Forward fill",
            "Backward fill",
            "Delete rows"
        ]
    }
    return methods.get(data_type, ["Unsupported data type"])
    # if len(data_type) == 1:
    #     return methods.get(data_type[0], ["Unsupported data type"])
    # else:
    #     method_list = []
    #     for i in data_type:
    #         method_list += methods.get(i)
    #     return list(set(method_list))   




def auto_process():
    cont.empty()
    with cont:
        with st.status("Auto Process Initiated...", expanded = True) as status:
            time.sleep(2)
            status.update(label="Removing rows with Null values initiated...", state = "running", expanded = True)
            st.session_state.table = st.session_state.table.dropna()
            st.toast("Rows with Null values Dropped")
            time.sleep(2)
            status.update(label="Deleting Duplicate rows initiated...", expanded = True)
            st.session_state.table = st.session_state.table.drop_duplicates()
            st.toast("Duplicate rows Deleted")
            time.sleep(2)
            status.update(label="Filtering Outliers initiated...", expanded = True)
            dtype = st.session_state.table.select_dtypes(include=np.number).columns.tolist()
            time.sleep(2)
            status.update(label="Auto Process Completed", state = "complete", expanded = True)


@st.experimental_dialog("Fill Null Values with values from user")
def fill_input_dialog(method, col):
    val = None
    if method == "Fill with a specific object":
        val = st.text_input("Enter a object to fill")
    elif method == "Fill with a specific value":
        val = st.number_input("Enter a number to fill")
    elif method == "Fill with a specific date":
        val = st.date_input("Enter a date to fill")
    elif method == "Interpolate":
        val = st.text_input("Enter a way to interpolate")
    
    st.session_state.value = val
    function = var.methods.get(method)
    function = function.format(df = "st.session_state.table", x = st.session_state.value, col = col)
    if st.button("Fill Nulls"):
        exec(function)
        st.rerun()



@st.experimental_fragment
def select_column(x1, x):
    c1, c2, c3= st.columns(3)
    column_name = x1[x].columns.tolist()
    cont_1 = st.container(height = 200)
    
    with c1: 
        st.write("**Column Name**")
        sel_col = st.selectbox("Select Column Name", column_name, index = None)
    
    
    if sel_col is not None:
        cont_1.empty()
        with cont_1:
            st.dataframe(st.session_state.table[sel_col].value_counts().head(10).reset_index().transpose(),
                         Use_container_width = True)
        with c2:
            st.write("**Number of Empty Values**")
            st.write('')
            st.write('')
            st.write(str(x1[sel_col][0]))
        with c3:
            st.write("**Select a way to fill**")
            # st.write(get_fill_fun_name(sel_col))
            fill_method_list = get_fill_fun_name(sel_col)
            sel_method = st.selectbox(sel_col, fill_method_list, index = None)

            if sel_method is not None:
                if sel_method in ["Fill with a specific object", "Fill with a specific value", "Fill with a specific date"]:
                    fill_input_dialog(sel_method, sel_col)
                else:
                    fill_nulls(sel_method, sel_col)
                
                
                

@st.experimental_dialog("Fill Null Values")
def fill_nulls(method, col):
    """
    Fill null values in a DataFrame column based on the selected method.

    Args:
        method (str): The method to use for filling null values.
        col (str): The name of the column in the DataFrame to fill.
    """
    # Get the fill method from the methods dictionary
    function = var.methods.get(method)
    # Format the fill method with the DataFrame and column names
    function = function.format(df = "st.session_state.table", col = col)

    # Execute the fill method and rerun the Streamlit app
    if st.button("Fill Nulls"):
        exec(function)
        st.rerun()




def fill_empty():
    cont.empty()
    with cont:
        x = st.session_state.table.columns[st.session_state.table.isna().any()].tolist()
        if len(x) != 0:
            x1 = st.session_state.table.isna().sum().reset_index().transpose()
            x1.columns = x1.iloc[0]
            x1 = x1[1:]
            st.write("Columns with empty values:")
            st.dataframe(x1[x], use_container_width=True)                       
            select_column(x1, x)    
                    
        else:
            st.write("No Empty Values")

@st.experimental_fragment
def delete_col():
    columns = st.session_state.table.columns
    selected_columns = st.multiselect("", columns, default = [])
    if len(selected_columns) != 0: 
        if st.button("Delete Columns"):
            st.session_state.table = st.session_state.table.drop(selected_columns, axis = 1)

def delete_columns():
    cont.empty()
    with cont:
        st.write("Select Columns to delete Columns: ")
        delete_col()



@st.experimental_fragment
def filter_out():
    selected_columns = st.multiselect("", get_numeric_columns, default = [])
    if len(selected_columns) != 0: 
        if st.button("Filter Outliers"):
            st.session_state.table[selected_columns] = st.session_state.table[selected_columns].astype(float)
            q1 = st.session_state.table[selected_columns].quantile(0.25)
            q3 = st.session_state.table[selected_columns].quantile(0.75)
            iqr = q3 - q1
            st.session_state.table = st.session_state.table[~((st.session_state.table[selected_columns] < (q1 - 1.5 * iqr)) | 
                                                              (st.session_state.table[selected_columns] > (q3 + 1.5 * iqr)))]


def filter_outlier():
    cont.empty()
    with cont:
        st.write("Select Columns to filter outliers: ")
        filter_out()



if st.session_state.table is None:
    st.write("Load Table First")
    st.page_link("pages/Data Upload/dataupload.py", label= "Load Table", icon = ":material/upload:")

else:
    c1, c2 = st.columns([3,1])
    with c1:
        st.header("Process Data")
    with c2:
        st.write('')
        st.write('')
        st.page_link("pages/Data Processing/datatype.py",
                      label= "Data Type", icon = ":material/123:")
        

    # st.subheader("Original Table")
    with st.expander("**Table Data**", icon = ":material/dataset:"):
        st.write('')
        st.dataframe(st.session_state.table.head(20))
    
    with st.expander("**Table Info and Description**", icon = ":material/info:"):
        st.dataframe(st.session_state.table.describe())
        # st.dataframe(st.session_state.table.info())
    
    c1, c2 = st.columns([1,5])
    with c2:
        cont = st.container(height = 500, border = True)

    with c1:
        with st.container(height = 500, border = True):
            st.write('**Select a Cleaning Process**')
            if st.button("Auto Process", use_container_width = True):
                auto_process()
            if st.button("Fill Empty", use_container_width = True):
                fill_empty()
            if st.button("Delete Columns", use_container_width = True):
                delete_columns()
            if st.button("Drop Duplicates", use_container_width = True):
                st.session_state.table = st.session_state.table.drop_duplicates()
                st.toast("Duplicates Dropped")
            if st.button("Filter Outlier", use_container_width = True):
                filter_outlier()
            if st.button("Reset", use_container_width = True):
                st.session_state.table = st.session_state.table_copy
                st.toast("Table Reset")
            
                
    

        

    

