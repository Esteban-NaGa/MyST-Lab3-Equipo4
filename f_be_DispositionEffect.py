#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 21:35:44 2019

@author: Esteban
"""
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go #Libreria necesaria para usar plotly

#Ciclo para medir tiempo entre close time y open time manuales de tp y sl

#Ciclo para medir tiempo entre close time y open time manuales de tp y sl

def f_be_DispositionEffect(datos):
    """"
    Param datos: Data frame de entrada con el historico de trades
    
    Return: Diccionario con data frame final, grafica, explicacion y escala
    
    """
    datos = datos.drop(['Order', 'Size', 'Commission', 'Taxes', 'Swap'], 1)
            
    datos = datos.reset_index()
            
    # Renombramos las columnas en minusculas por convención
    datos.rename(columns={'Type' : 'type', 'Symbol': 'symbol',
                            'S/L' : 'sl', 'T/P':'tp', 'Profit': 'profit'},
                inplace=True)
            
    df_times= datos[['openTime','closeTime']]
            
    #Debido a que la librería datetime funciona con guiones, quitamos los puntos a las fechas
    # y los cambiamos por guiones
    df_times['openTime'] = df_times['openTime'].str.replace('.','-')
    df_times['closeTime'] = df_times['closeTime'].str.replace('.','-')


    datos['openTime'] = df_times['openTime']
    datos['closeTime'] = df_times['closeTime']
    
    
    df_datos = datos
    
    manualTime_tp = []
    manualTime_sl = []
    for i, row in df_datos.iterrows():
        if row['profit'] > 0 and row['tp'] > 0:
            if row['closePrice']-row['tp'] != 0:
                calc_temp = (datetime.strptime(df_datos.iloc[i,7], '%Y-%m-%d %H:%M:%S')
                -datetime.strptime(df_datos.iloc[i,1],'%Y-%m-%d %H:%M:%S')).total_seconds()/60/60
                manualTime_tp.append(calc_temp)
            else:
                pass
        elif row['profit'] < 0 and row['sl'] > 0:
            if row['closePrice']-row['sl'] != 0:
                calc_temp = (datetime.strptime(df_datos.iloc[i,7], '%Y-%m-%d %H:%M:%S')
                -datetime.strptime(df_datos.iloc[i,1],'%Y-%m-%d %H:%M:%S')).total_seconds()/60/60
                manualTime_sl.append(calc_temp)
            else:
                pass
    #Tiempos manuales de take profit y stop losing
    manualTime_tp = pd.DataFrame(manualTime_tp, columns=["manual_tp"])
    manualTime_sl = pd.DataFrame(manualTime_sl, columns=["manual_sl"])      
            
    
    #Dataframe final
    df_manualTimes = pd.concat([manualTime_tp, manualTime_sl], axis=1, sort=False)
    
    media_tp = round(np.mean(df_manualTimes['manual_tp']),2)
    media_sl = round(np.mean(df_manualTimes['manual_sl']),2)
    escala_sesgo = round((media_sl/media_tp)*100,2)
            
    
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=df_manualTimes.iloc[0:,0],
        name='Ganancias Manuales',
        marker_color='green',
        boxmean=True # represent mean
    ))
    fig.add_trace(go.Box(
        y=df_manualTimes.iloc[0:,1],
        name='Perdidas manuales',
        marker_color='red',
        boxmean=True # represent mean
    ))
    
    
    return {'datos': df_manualTimes,
            'grafica': fig,
            'explicacion': 'Las ganancias las mantuvo con una media de '+ str(media_tp)+ ' horas mientras que las perdidas '+ str(media_sl) + ' horas, por lo tanto si la media de horas de perdidas es mayor se cumple sesgo, de lo contrario no se cumple',
            'escala': str(escala_sesgo) + '% de las veces se cumplió el sesgo, ya que mantuvo por ese porcentaje las ganancias respecto a las perdidas'}