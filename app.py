import streamlit as st
import io
import pandas as pd
from sklearn.metrics import pairwise_distances

st.title("Pairwise distance matrix")

model = None

if not model:
    # select metric
    metric = st.selectbox('Select distance metric to calculate',
                                ['cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan']
                                )
    
    st.write("Upload a csv file with the data. One sample per row. 1st row is assumed to hold variable names.")
    df_sample_inp = pd.DataFrame({'Variable 1': [0.0, 4.1, 2.3], 'Variable 2': [0, 1, 1], 'Variable 3': [5, 3, 9]})
    st.markdown(df_sample_inp.style.hide(axis="index").to_html(), unsafe_allow_html=True)


    st.text("")
    st.text("")
    st.write("It is possible to provide sample indeces in the first column of the uploaded file. They will be used to label columns and rows in the resulting distance matrix. Indicate in the following checkbox:")
    
    df_sample_inp = pd.DataFrame({'Index': ['Sample 1', 'Sample 2', 'Sample 3'], 'Variable 1': [0.0, 4.1, 2.3], 'Variable 2': [0, 1, 1], 'Variable 3': [5, 3, 9]})
    st.markdown(df_sample_inp.style.hide(axis="index").to_html(), unsafe_allow_html=True)
    
    index_column = st.checkbox('1st column in uploaded file contains sample indeces')
    header_row = st.checkbox('1st row contains column labels') 

    inp_file = st.file_uploader("Choose a file")
    if inp_file is not None:
        
        if index_column:
            index_col = 0
        else:
            index_col = None
        if header_row:
            header = 0
        else:
            header = None
        df = pd.read_csv(inp_file, delimiter=';', index_col=index_col, header=header)

        # if index_column:
        #     df.set_index(df.columns[0],inplace=True)

        X = df.to_numpy(copy=True)

        y_hat = pairwise_distances(X, metric=metric)

        df_dists = pd.DataFrame(data=y_hat,
                                index=df.index,
                                columns=df.index
                                )

        df_pars = pd.DataFrame([['metric', 'date'],[metric, 'today']])

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer) as writer:  
            df_dists.to_excel(writer, sheet_name='Distance Matrix', index=True)
            df_pars.to_excel(writer, sheet_name='Calculation details', index=False)


        st.download_button(
            label="Download pairwise distance matrix as xlsx",
            data=buffer,
            file_name='distance_matrix.xlsx',
            mime='application/vnd.ms-excel',
        )
