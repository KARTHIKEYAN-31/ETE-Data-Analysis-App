

#process

@st.experimental_fragment
def fill_empty1():  
    cont.empty()
    with cont:
        x = st.session_state.table.columns[st.session_state.table.isna().any()].tolist()
        if len(x) != 0:
            x1 = st.session_state.table.isna().sum().reset_index().transpose()
            x1.columns = x1.iloc[0]
            x1 = x1[1:]
            st.write("Columns with empty values:")
            st.dataframe(x1[x], use_container_width=True)
            c1, c2 = st.columns([2,1])
            with c2:
                fill_nulls()
            c1, c2, c3= st.columns(3)
            with c1: st.write("**Column Name**")
            with c2: st.write("**Number of Empty Values**")
            with c3: st.write("**Select a way to fill**")
            # with c4: st.write("**Action Button**")
            column_name = x1[x].columns.tolist()
            fill_method_list = column_name
            action_list = column_name

            for i in column_name:
                with c1:
                    with st.container(height = 68, border = False):
                        st.write('')
                        st.write('')
                        st.write(i)
                with c2:
                    with st.container(height = 68, border = False):
                        st.write('')
                        st.write('')
                        st.write(x1[i][0])
                with c3:
                    fill_method_list[column_name.index(i)] = st.selectbox(i, get_fill_fun_name(i), key = 'fill_method' + str(i))


        else:
            st.write("No Empty Values")