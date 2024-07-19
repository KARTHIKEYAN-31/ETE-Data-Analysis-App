import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



if st.session_state.table is None:
    st.write("Load Table First")
    st.page_link("pages/Data Upload/dataupload.py", label= "Load Table", icon = ":material/upload:")

else:
    st.header("Customize your charts")
    uni, bi = st.tabs(['Uni-Variable Charts', 'Bi-Variable Charts'])

    with uni:
        st.markdown("##### Uni-Variable Manual Analysis")
        c1, c2 = st.columns(2)
        with c1:
            column = st.selectbox("Select Column", st.session_state.table.columns, index=None, )
        if column is not None:
            if str(st.session_state.table.dtypes[column]) in ['object', 'datetime64[ns]']:
                with c2:
                    chart_type = st.selectbox("Select Chart Type",['Histogram', 'Pie'], index=None)
                if chart_type == 'Histogram':
                    df = st.session_state.table[column].value_counts().reset_index()
                    with c1:
                        st.write("Top 20 Values")
                        fig = px.histogram(df.head(20), x=column, y = 'count', title=column) 
                        fig.update_layout(xaxis_title="Values", yaxis_title="Count")
                        st.plotly_chart(fig)
                    with c2:
                        st.write("Bottom 20 Values")
                        fig = px.histogram(df.tail(20), x=column, y='count', title=column)
                        fig.update_layout(xaxis_title="Values", yaxis_title="Count")
                        st.plotly_chart(fig)

                elif chart_type == 'Pie':
                    df = st.session_state.table[column].value_counts().reset_index()
                    with c1:
                        st.write("Top 20 Values")
                        fig = px.pie(df.head(20), names=column, values = 'count', title=column, color_discrete_sequence= px.colors.sequential.RdBu) 
                        fig.update_layout(xaxis_title="Values", yaxis_title="Count")
                        st.plotly_chart(fig)
                    with c2:
                        st.write("Bottom 20 Values")
                        fig = px.pie(df.tail(20), names=column, values='count', title=column, color_discrete_sequence= px.colors.sequential.RdBu)
                        fig.update_layout(xaxis_title="Values", yaxis_title="Count")
                        st.plotly_chart(fig)
            else:
                with c2:
                    chart_type = st.selectbox("Select Chart Type", ['Box Plot', 'Violin', 'Histogram'], index=None)
                if chart_type is not None:
                    if chart_type == 'Histogram':
                        fig = px.histogram(st.session_state.table, x=column, title=column, nbins=10) 
                    elif chart_type == 'Pie':
                        fig = px.pie(st.session_state.table, names=column, title=column)
                    elif chart_type == 'Box Plot':
                        fig = px.box(st.session_state.table, y=column, title=column)
                    elif chart_type == 'Violin':
                        fig = px.violin(st.session_state.table, y=column, title=column)
                    st.plotly_chart(fig)


    with bi:
        st.markdown("##### Bi-Variable Manual Analysis")
        

        chart_type = st.selectbox("Select Chart Type",
                                       ['Scatter or Bubble', 'Line', 'Bar',
                                         'Heatmap', 'Heirarchy - Sunburst',
                                         'Tables', 'Pie'],
                                         index=None)
        c1, c2 = st.columns([5,1])

        if chart_type is not None:
            if chart_type == 'Scatter or Bubble':
                with c2:
                    x_axis = st.selectbox("Select X Axis", st.session_state.table.select_dtypes(include=['int64', 'float64']).columns.tolist(), index=None)
                    y_axis = st.selectbox("Select Y Axis", st.session_state.table.select_dtypes(include=['int64', 'float64']).columns.tolist(), index=None)
                    size = st.selectbox("Select Size", st.session_state.table.select_dtypes(include=['int64', 'float64']).columns.tolist(), index=None)
                    if x_axis is not None and y_axis is not None:
                        if st.button("Generate Chart"):
                            if size is not None:
                                fig = px.scatter(st.session_state.table, x=x_axis, y=y_axis, size=size,
                                                title=f"{x_axis} vs {y_axis} vs {size}")
                            else:
                                fig = px.scatter(st.session_state.table, x=x_axis, y=y_axis,
                                                title=f"{x_axis} vs {y_axis}")

                            with c1:st.plotly_chart(fig)
            
            if chart_type == 'Line':
                with c2:
                    x_axis = st.selectbox("Select X Axis", st.session_state.table.select_dtypes(include=['int64', 'float64', 'datetime64[ns]']).columns.tolist(), index=None)
                    y_axis = st.selectbox("Select Y Axis", st.session_state.table.select_dtypes(include=['int64', 'float64']).columns.tolist(), index=None)
                    color = st.selectbox("Select Size", st.session_state.table.select_dtypes(include=['object']).columns.tolist(), index=None)
                    if x_axis is not None and y_axis is not None:
                        if st.button("Generate Chart"):
                            if color is not None:
                                temp_df = st.session_state.table.groupby([x_axis, color])[y_axis].mean().reset_index()
                                temp_df = temp_df[temp_df[color] in temp_df[color].unique()[0:10]]
                                fig = px.line(temp_df, x=x_axis, y=y_axis, color=color,
                                                title=f"{x_axis} vs {y_axis} vs {color}")
                            else:
                                temp_df = st.session_state.table.groupby(x_axis)[y_axis].mean().reset_index()
                                fig = px.line(temp_df, x=x_axis, y=y_axis,
                                                title=f"{x_axis} vs {y_axis}")

                            with c1:st.plotly_chart(fig)
            


        # c1, c2, c3, c4 = st.columns(4)
        # with c1:
        #     chart_type = st.selectbox("Select Chart Type",
        #                                ['Scatter or Bubble', 'Line', 'Bar',
        #                                  'Heatmap', 'Heirarchy - Sunburst',
        #                                  'Tables', 'Pie'],
        #                                  index=None)
        #     mea_mea = ['Scatter or Bubble']
        #     dim_mea = ['Line', 'Bar', 'Pie']

        # if chart_type is not None:
        #     with c2:
        #         x_axis = st.selectbox("Select X Axis", st.session_state.table.select_dtypes(include=['object', 'datetime64[ns]']).columns.tolist(), index=None)
        #     if x_axis is not None:
        #         with c3:
        #             if chart_type in ['Scatter', 'Line', 'Bar', 'Heatmap', 'Bubble', 'Heirarchy - Sunburst']: 
        #                 y_axis = st.selectbox("Select Y Axis", st.session_state.table.select_dtypes(include=['object', 'datetime64[ns]']).columns.tolist(), index=None)
                    
    




