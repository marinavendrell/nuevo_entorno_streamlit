from datetime import datetime, timedelta
import matplotlib.pyplot as plt

from OMIEData.DataImport.omie_marginalprice_importer import OMIEMarginalPriceFileImporter
from OMIEData.Enums.all_enums import DataTypeInMarginalPriceFile

import pandas as pd

from datetime import datetime, timedelta

import warnings
#warnings.filterwarnings("ignore")


import pytz
import streamlit as st


fecha_hora_actual = datetime(2023, 8, 7)

# Sumar 24 horas
desplazamiento = timedelta(hours=24)
fecha_24_horas_futuro = fecha_hora_actual + desplazamiento


# This can take time, it is downloading the files from the website..
#df = OMIEMarginalPriceFileImporter(date_ini=fecha_hora_actual, date_end=fecha_24_horas_futuro).read_to_dataframe(verbose=True)

#df.sort_values(by='DATE', axis=0, inplace=True)
#df = df[df.CONCEPT == 'PRICE_SP']

url = "https://www.omie.es/sites/default/files/dados/AGNO_2023/MES_08/TXT/INT_PBC_EV_H_1_06_08_2023_06_08_2023.TXT"

# Leer los datos desde la URL y crear un DataFrame
df = pd.read_csv(url, sep=";", encoding="ISO-8859-1", skiprows=2)

st.dataframe(df)



