
from flask import Flask, render_template, request
import pandas as pd
import folium
from folium.plugins import HeatMap
from io import BytesIO
import base64

df_cidades = pd.read_csv("municipios.csv")
df_cidades['municipio'] = df_cidades['municipio'].str.strip().str.lower()

df_chamados = pd.read_excel("vitoria-23-09.xlsx")

# Processa os DataFrames
df_chamados['MUNICIPIO'] = df_chamados['MUNICIPIO'].str.strip().str.lower()

# Merge dos DataFrames
df_pontos_chamados = pd.merge(
    df_chamados,
    df_cidades[['municipio', 'longitude', 'latitude']],
    left_on='MUNICIPIO',
    right_on='municipio',
    how='left'
)

df_pontos_chamados = df_pontos_chamados[['CHAMADO', 'AGE_ABERTURA', 'CLIENTES', 'FILIAL', 'NOME DO TECNICO', 
                                            'SLA_HOJE', 'MUNICIPIO', 'DENTRO_SLA', 'FORA_SLA', 
                                            'BREAK_FIX', 'TOT_ELEGIVEL', 'longitude', 'latitude']]

df_pontos_chamados = df_pontos_chamados.dropna(subset=['longitude', 'latitude'])

print(df_pontos_chamados)