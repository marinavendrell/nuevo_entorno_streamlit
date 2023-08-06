import requests
from datetime import datetime, timedelta
import pandas as pd
import pytz

import streamlit as st
import warnings
#warnings.filterwarnings("ignore")

fecha_hora_actual = datetime(2022, 10, 5)
# Sumar 24 horas
desplazamiento = timedelta(hours=24)
fecha_24_horas_futuro = fecha_hora_actual + desplazamiento

# Obtener el año como una cadena de texto
anyo = str(fecha_hora_actual.year)

# Obtener el mes como una cadena de texto con formato 'MM'
mes = f"{fecha_hora_actual.month:02d}"

# Obtener el día como una cadena de texto con formato 'DD'
dia = f"{fecha_hora_actual.day:02d}"

# Obtener el año final como una cadena de texto
anyo_final = str(fecha_hora_actual.year)

# Obtener el mes final como una cadena de texto con formato 'MM'
mes_final = f"{fecha_hora_actual.month:02d}"

# Obtener el día final como una cadena de texto con formato 'DD'
dia_final = f"{fecha_hora_actual.day:02d}"


url_inicial = f"https://www.omie.es/sites/default/files/dados/AGNO_{anyo}/MES_{mes}/TXT/INT_PBC_EV_H_1_{dia}_{mes}_{anyo}_{dia}_{mes}_{anyo}.TXT"
url_final = f"https://www.omie.es/sites/default/files/dados/AGNO_{anyo_final}/MES_{mes_final}/TXT/INT_PBC_EV_H_1_{dia_final}_{mes_final}_{anyo_final}_{dia_final}_{mes_final}_{anyo_final}.TXT"


url = []
url.append(url_inicial)
url.append(url_final)

 
# Leer los datos desde la URL y crear un DataFrame
#df = pd.read_csv(url[0], sep=";", encoding="ISO-8859-1", skiprows=2)


    
df = pd.DataFrame()

for url_actual in url:

    # Leer los datos desde la URL actual y crear un DataFrame
    df_actual = pd.read_csv(url_actual, sep=";", encoding="ISO-8859-1", skiprows=2)
    df_actual = df_actual[df_actual['Unnamed: 0'] == 'Precio marginal en el sistema español (EUR/MWh)']
    df_actual = df_actual.iloc[:,0:25]
    df_actual = df_actual.drop(columns = ['Unnamed: 0'])
    
    # Concatenar el DataFrame actual a df
    df = pd.concat([df, df_actual], ignore_index=True)




# Crear una columna 'date' en el DataFrame
df['date'] = None

# Asignar el valor de fecha_hora_actual a la columna 'date' en la primera iteración
df.loc[0, 'date'] = fecha_hora_actual.strftime('%Y-%m-%d')

# Asignar el valor de fecha_24_horas_futuro a la columna 'date' en la segunda iteración
df.loc[1, 'date'] = fecha_24_horas_futuro.strftime('%Y-%m-%d')

# Mover la columna 'date' a la primera posición del DataFrame
df.insert(0, 'date', df.pop('date'))

# Convertimos la columna 'DATE' al tipo datetime
df_date = df.copy()
df_date['date'] = pd.to_datetime(df['date'])

# Creamos una lista para almacenar las horas del día generadas
horas_del_dia = []

# Iteramos por cada fecha única en el DataFrame original
for fecha in df_date['date'].unique():
    # Generamos un rango de horas del día para la fecha actual
    fecha_siguiente = fecha + pd.DateOffset(days=1)
    horas_del_dia_fecha = pd.date_range(start=fecha, end=fecha_siguiente, freq='H', closed='left')
    # Extendemos la lista con las horas del día generadas para la fecha actual
    horas_del_dia.extend(horas_del_dia_fecha)

# Creamos un DataFrame con las horas del día
df_date = pd.DataFrame({'date': horas_del_dia})

# Lista para almacenar los registros transpuestos
registros_transpuestos = []

df = df.drop(columns = ['date'])
# Iteramos por cada registro (fila) en el DataFrame
for index, row in df.iterrows():
    # Transponemos el registro actual y lo almacenamos como una Serie
    registro_transpuesto = row.reset_index(drop=True)
    registro_transpuesto = registro_transpuesto.rename('Valor')
    registros_transpuestos.append(registro_transpuesto)

# Concatenamos las Series transpuestas en un nuevo DataFrame
EUR_MWh = pd.concat(registros_transpuestos, axis=0, ignore_index=True)

# Convertimos la Serie en un DataFrame con una columna llamada 'Valor'
EUR_MWh = EUR_MWh.to_frame(name='€_MWh')
EUR_MWh['€_MWh'] = EUR_MWh['€_MWh'].str.replace(',', '.')
EUR_MWh = pd.to_numeric(EUR_MWh['€_MWh'], errors='coerce')

df_precio = pd.concat([df_date, EUR_MWh], axis = 1)
df_precio['€_KWh'] = df_precio['€_MWh']/1000
df_precio['kwh'] = 200
df_precio['€'] = round(df_precio['€_KWh'] * df_precio['kwh'], 2)


st.dataframe(df_precio)



