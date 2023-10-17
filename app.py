import streamlit as st
import io
import csv
import pandas as pd
from sklearn.metrics import pairwise_distances

st.title("Erstellung der paarweisen Distanzmatrix")

model = None

if not model:
    # select metric
    metric = st.selectbox('Wählen Sie die zu berechnende Distanz-Metrik',
                                ['cityblock', 'cosine', 'euclidean', 'l1',
                                 'l2', 'manhattan']
                         )
    
    st.write('''Laden Sie eine csv-Datei mit den Daten hoch. Ein Sample pro 
             Zeile. Die erste Reihe wird als Kopfzeile Variablen-Namen interpretiert.''')
    df_sample_inp = pd.DataFrame({'Variable 1': [0.0, 4.1, 2.3], 'Variable 2': [0, 1, 1], 
                                  'Variable 3': [5, 3, 9]})
    st.markdown(df_sample_inp.style.hide(axis="index").to_html(), unsafe_allow_html=True)


    st.text("")
    st.text("")
    st.write("""Sample-Indices können in der ersten Spalte des hochgeladenen Datei 
             angegeben werden. Sie werden als Spalten- und Zeilen-Labels im Output-File 
             verwendet. Wählen Sie in der folgenden Checkbox:""")
    
    df_sample_inp = pd.DataFrame({'Index': ['Sample 1', 'Sample 2', 'Sample 3'], 
                                  'Variable 1': [0.0, 4.1, 2.3], 'Variable 2': [0, 1, 1], 
                                  'Variable 3': [5, 3, 9]})
    st.markdown(df_sample_inp.style.hide(axis="index").to_html(), unsafe_allow_html=True)
    
    index_column = st.checkbox('Erste Spalte enthält Sample-Indices')
    header_row = st.checkbox('Erste Zeile enthält Spalten-Labels') 

    inp_file = st.file_uploader("Wählen Sie ein File")
    if inp_file is not None:
        
        if index_column:
            index_col = 0
        else:
            index_col = None
        if header_row:
            header = 0
        else:
            header = None

        with open(inp_file, newline='') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
        
        df = pd.read_csv(inp_file, dialect.delimiter, index_col=index_col, header=header)
        

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
            label="Distanzmatrix als xlsx-File herunterladen",
            data=buffer,
            file_name='distance_matrix.xlsx',
            mime='application/vnd.ms-excel',
        )
