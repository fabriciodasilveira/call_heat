from flask import Flask, render_template, request
import pandas as pd
import folium
from folium.plugins import HeatMap
from io import BytesIO
import base64

app = Flask(__name__)

# Carregar o DataFrame de cidades
df_cidades = pd.read_csv("municipios.csv")
df_cidades['municipio'] = df_cidades['municipio'].str.strip().str.lower()

@app.route('/', methods=['GET', 'POST'])
def index():
    mapa_html = None
    try:
        if request.method == 'POST':
            # Processa o arquivo de chamados enviado
            file_chamados = request.files['file_chamados']
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

            df_pontos_chamados = df_pontos_chamados[['CHAMADO', 'AGE', 'CLIENTES', 'FILIAL', 'NOME_TECNICO', 
                                                       'SLA_HOJE', 'MUNICIPIO', 'DENTRO_SLA', 'FORA_SLA', 
                                                       'BREAK_FIX', 'ELEGIVEL', 'longitude', 'latitude']]

            df_pontos_chamados = df_pontos_chamados.dropna(subset=['longitude', 'latitude'])

            # Criação do mapa
            latitude_brasil = -15.8267
            longitude_brasil = -47.9218
            mapa = folium.Map(location=[latitude_brasil, longitude_brasil], zoom_start=5)

            # Preparação dos dados para o HeatMap
            heat_data = [[row['latitude'], row['longitude']] for index, row in df_pontos_chamados.iterrows()]

            # Adiciona a camada de HeatMap ao mapa
            HeatMap(heat_data, radius=15, blur=10, min_opacity=0.4).add_to(mapa)

            # Salvar o mapa em um objeto BytesIO
            mapa_io = BytesIO()
            mapa.save(mapa_io, close_file=False)

            # Codificar em base64
            mapa_html = base64.b64encode(mapa_io.getvalue()).decode()
            mapa_html = f"data:text/html;base64,{mapa_html}"

            return render_template('index.html', mapa=mapa_html)

    except Exception as e:
        return f"Ocorreu um erro: {str(e)}", 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
