from flask import Flask, render_template, request
import pandas as pd
import folium
from folium.plugins import HeatMap

app = Flask(__name__)

# Carregar o DataFrame de cidades
df_cidades = pd.read_csv("municipios.csv")
df_cidades['municipio'] = df_cidades['municipio'].str.strip().str.lower()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Processa o arquivo de chamados enviado
        file_chamados = request.files['file_chamados']

        # Lê o arquivo de chamados
        df_chamados = pd.read_excel(file_chamados)

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

        # Criação do mapa
        latitude_brasil = -15.8267
        longitude_brasil = -47.9218
        mapa = folium.Map(location=[latitude_brasil, longitude_brasil], zoom_start=5)

        # Preparação dos dados para o HeatMap
        heat_data = [[row['latitude'], row['longitude']] for index, row in df_pontos_chamados.iterrows()]

        # Adiciona a camada de HeatMap ao mapa
        HeatMap(heat_data, radius=15, blur=10, min_opacity=0.4).add_to(mapa)

        # Salva o mapa em um arquivo HTML na pasta static
        mapa.save('static/mapa.html')
        print("Mapa salvo em static/mapa.html")

        return render_template('index.html', mapa='static/mapa.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
