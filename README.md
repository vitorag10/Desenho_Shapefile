Documentação Completa da API Flask para Conversão de Coordenadas em Shapefile (Com Integração Front-End)
Descrição Geral
Esta API permite converter um conjunto de coordenadas geográficas (latitude e longitude) para um arquivo shapefile no formato .shp. O shapefile gerado pode ser baixado posteriormente através de um endpoint específico. A API está conectada a um front-end, permitindo que o usuário escolha onde deseja salvar o arquivo no seu computador ou notebook local.

A aplicação é construída com o framework Flask, utilizando as bibliotecas Fiona e Shapely para manipulação de dados geoespaciais.

Tecnologias Utilizadas
Flask: Framework web para construção de APIs.
Fiona: Biblioteca para leitura e gravação de dados geoespaciais no formato shapefile.
Shapely: Biblioteca para manipulação e análise de geometria espacial.
OS: Biblioteca padrão do Python para operações no sistema de arquivos (criação de diretórios).
Front-End: A API está integrada a uma interface de usuário (UI) que permite interações mais intuitivas, como a escolha de onde o arquivo será salvo no dispositivo local do usuário.
Estrutura do Projeto
O projeto tem a seguinte estrutura de arquivos e pastas:

bash
Copiar código
/<diretório-do-projeto>
│
├── app.py              # Código da API em Flask
├── /uploads            # Pasta para arquivos enviados (não utilizada diretamente)
├── /outputs            # Pasta onde os shapefiles gerados serão armazenados
└── requirements.txt    # Arquivo com as dependências do projeto
Requisitos
Criar e ativar o ambiente virtual (se necessário):

bash
Copiar código
python3 -m venv venv        # Cria o ambiente virtual
source venv/bin/activate    # Ativa o ambiente no Linux/macOS
venv\Scripts\activate       # Ativa o ambiente no Windows
Instalar as dependências:

bash
Copiar código
pip install -r requirements.txt
Ou, se o arquivo requirements.txt não estiver presente:

bash
Copiar código
pip install flask fiona shapely
Iniciar a API
Após a instalação das dependências, execute o seguinte comando no terminal para iniciar o servidor da API:

bash
Copiar código
python app.py
Isso iniciará o servidor Flask no endereço http://127.0.0.1:5000, permitindo que a API seja acessada via front-end.

Integração Front-End
A API está projetada para ser consumida por um front-end, que fornece uma interface de usuário interativa. O front-end permite que o usuário forneça as coordenadas geográficas e o nome do arquivo desejado, e então interaja com o endpoint para gerar o shapefile.

Funcionalidade de Download no Front-End
Quando o shapefile é gerado, o usuário tem a opção de escolher onde deseja salvar o arquivo no seu computador ou notebook local. Isso é possível devido ao uso do navegador para solicitar o download do arquivo.

O front-end se comunica com o backend da API, recebendo o nome do arquivo e o caminho de download gerado, e então usa a funcionalidade do navegador para baixar o arquivo diretamente para o local escolhido pelo usuário.

Descrição dos Endpoints da API
1. POST /convert
Este endpoint recebe as coordenadas geográficas e gera um arquivo shapefile do tipo LineString.

URL: /convert

Método HTTP: POST

Parâmetros da Requisição (JSON):

coordinates (necessário): Lista de coordenadas no formato [[lat1, lon1], [lat2, lon2], ...].
filename (necessário): Nome do arquivo de saída (sem a extensão .shp, ela será adicionada automaticamente).
Exemplo de Corpo da Requisição:

json
Copiar código
{
    "coordinates": [[-15.7801, -47.9292], [-15.7800, -47.9291]],
    "filename": "linha"
}
Resposta:

Se os dados forem válidos, a resposta incluirá o caminho para o shapefile gerado.
Caso contrário, retornará um erro com código 400.
Exemplo de Resposta:

json
Copiar código
{
    "shapefilePath": "linha.shp"
}
2. GET /download/<filename>
Este endpoint permite que o usuário faça o download do shapefile gerado.

URL: /download/<filename>

Método HTTP: GET

Parâmetros:

filename (necessário): Nome do arquivo .shp a ser baixado (por exemplo, linha.shp).
Exemplo de URL:

text
Copiar código
GET /download/linha.shp
Resposta:

O shapefile será enviado como um anexo para download.
Funções Detalhadas
Criação de Diretórios
No início do código, garantimos que os diretórios ./uploads e ./outputs existam:

python
Copiar código
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
Processamento de Dados para Criação do Shapefile
A função convert() processa a requisição e cria o shapefile, que é salvo no diretório ./outputs:

python
Copiar código
with fiona.open(shapefile_path, 'w', driver='ESRI Shapefile', schema=schema, crs=from_epsg(4326)) as shp:
    line = LineString([(lon, lat) for lat, lon in coordinates])
    shp.write({
        'geometry': {
            'type': 'LineString',
            'coordinates': list(line.coords),
        },
        'properties': {'id': 1},
    })
Download do Shapefile
A função download() permite que o usuário faça o download do shapefile gerado, utilizando o navegador para escolher o local de destino no dispositivo local do usuário:

python
Copiar código
return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)
Conclusão
Esta API permite a conversão de coordenadas geográficas para o formato shapefile, com a funcionalidade adicional de permitir ao usuário escolher onde deseja salvar o arquivo gerado no seu computador ou notebook. A integração com o front-end oferece uma interface intuitiva para a entrada de dados e download do arquivo.

A API pode ser facilmente utilizada para automação de tarefas geoespaciais e integração com outras ferramentas e plataformas.
