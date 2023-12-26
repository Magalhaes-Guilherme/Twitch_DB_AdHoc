import streamlit as st
import pandas as pd
import time
from DAO import *
from model import *
import pdfkit as pdf
import matplotlib.pyplot as plt

# Função para gerar o relatório a partir dos critérios selecionados
def geraRelatorio():
    if not relatorio_fields:
        return -1
    
    # Verifica se foi adicionado algum filtro  
    if st.session_state.filtros == "":
        st.session_state.filtros = None
    
    session = DAO.getSession()
    session.expire_on_commit = False

    # Verifica sobre qual tabela do banco será emitido um relatório
    if relatorio_type == 'Videos':
        query = DAORelatorioVideos.select(session, st.session_state.filtros, st.session_state.ordenacao, relatorio_fields)
    if relatorio_type == 'Streams':
        query = DAORelatorioStreams.select(session, st.session_state.filtros, st.session_state.ordenacao, relatorio_fields)
    if relatorio_type == 'Canais':
        query = DAORelatorioCanais.select(session, st.session_state.filtros, st.session_state.ordenacao, relatorio_fields)
    if relatorio_type == 'Usuários':
        query = DAORelatorioUsuarios.select(session, st.session_state.filtros, st.session_state.ordenacao, relatorio_fields)
    if relatorio_type == 'Categorias':
        query = DAORelatorioCategories.select(session, st.session_state.filtros, st.session_state.ordenacao, relatorio_fields)

    # Conexão
    connection = session.connection()
    df = pd.read_sql_query(query.statement, con = connection)
    session.commit()
    session.close()

    # Fazer com que o dataframe receba os dados da sql query recebida na linha 34
    st.session_state.dataframe = df

    # Convertendo o dataframe do relatorio para excel e html
    df.to_excel("DB/relatorio.xlsx", index=False)
    df.to_html('DB/relatorio.html', index=False)

# Função para limpar o campo do input do valor do filtro
def clear_form():
    st.session_state["bar"] = ""

# Define os campos que podem ser incluídos nos filtros e no relatório
def defineCampos():
    st.session_state.filtros = ""
    st.session_state.query = False
    st.session_state.qtdFiltros = 0

def defineOrdenacao():
    st.session_state.ordenacao = True

# Converter o relatório para pdf
def relatorioPDF():
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdf.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    pdf.from_file('DB/relatorio.html', 'relatorio.pdf', configuration=config)

# Aqui está sendo mostrado o título da página (na aba do navegador)
st.set_page_config(page_title="Relatório Twitch API")

# Estilização da página
app_style = """
    <style>
        /* Corpo principal da página*/
            [data-testid="stAppViewContainer"] {
                width: 100%;
                background: linear-gradient(141deg, #ff3e5f 0%, #6441a5 51%, #6441a5 75%);
                color: white;
                font-family: Arial, sans-serif;
            }

            /* Título da página */
            [data-testid="StyledLinkIconContainer"]  {
                text-align: center !important;
                font-size: 40px;
                color: white !important;
                margin-top: -50px;
                margin-bottom: 20px;
            }

            /* Textos da página principal */ 
            [data-testid="stAppViewContainer"] p {
                font-size: 17.2px;
                color: white;
                margin-top: 5px;
            }

            /* Formulário para adicionar filtros */ 
            [data-testid="stForm"]{
                margin-top: -15px;
                margin-bottom: 15px;
                border: 2px solid;
            }

            /* Botão para escolher o campo sobre o qual ordenar*/
            [data-testid="stForm"] .st-aw{
                width: 210px;
            }

            /* Botão para ordenar*/
            .e10yg2by2{
                text-align: center;
                align-content: center;
            }

            /* Botões de select */ 
            .st-av {
                background-color: #9146ff;
                border-color: white;
                color: white;
                font-size: 20px;
            }

            /* Campo de texto */ 
            .st-ci {
                background-color: #9146ff;
                font-size: 20px;
            }

            /* Filtros adicionados */
            [data-testid="stExpander"]{
                margin-top: -15px;
                margin-bottom: 15px;
                border: 2px solid;
            }

            /* Radio button de ordenação */
            .st-ef {
                margin-bottom: 0px;
            }            

            /* Botão para gerar o relatório*/
            .e1f1d6gn3{
                text-align: center;
                align-content: center;
            }

        /* Barra lateral*/
            [data-testid="stSidebar"] {
                background-color: #9146ff;
                display: flex;
                flex-direction: column;
                align-items: center;
                text-decoration: none;
                font-size: 30px;
                text-shadow: 2px 2px 2px black;
                text-align: center;
            }
            [data-testid="stSidebar"] img {
                margin-top: -20px;
                margin-bottom: 30px;
            }
            /* .e115fcil2 */

            [data-testid="stSidebar"] h2 {
                font-size: 30px;
                color: white;
                margin-top: -40px;
            }
            [data-testid="stSidebar"] * {
                align-items: center;
                font-size: 20px;
                font-weight: bold;
                color: white;
            }

            [data-testid="stSidebar"] p {
                margin-bottom: 20px;
            }

            [data-testid="stSidebar"] hr {
                margin-top: 2px;
                margin-bottom: 5px;
            }
    </style>
    """
st.markdown(app_style, unsafe_allow_html=True) 

# Barra lateral
st.sidebar.header("Twitch API")
st.sidebar.image('./img/twitch.png')
st.sidebar.write("\n")
st.sidebar.header("Desenvolvido por:")
st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
st.sidebar.write("Guilherme Ribeiro")
st.sidebar.write("Tales Oliveira")
st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)

# Título da página
st.title('Relatórios Twitch API\n')

# ===================================================================
# Se pagina=0, mostra a página inicial. Se pagina=1, mostra o relatório
if 'pagina' not in st.session_state:
    st.session_state.pagina = 0

# Para exibir o dataframe
if 'dataframe' not in st.session_state:
    st.session_state.dataframe = False

# Dados do dataframe do relatório
if 'df' not in st.session_state:
    st.session_state.df = False

# Filtros
if 'filtros' not in st.session_state:
    st.session_state.filtros = ""

# Conta a quantidade de filtros
if 'qtdFiltros' not in st.session_state:
    st.session_state.qtdFiltros = 0

# Ordenação
if 'ordenacao' not in st.session_state:
    st.session_state.ordenacao = None

# Query SQL a ser executada
if 'query' not in st.session_state:
    st.session_state.query = False

# Relatóio
if 'relatorio' not in st.session_state:
    st.session_state.relatorio = False

# Dados em PDF
if 'dataPdf' not in st.session_state:
    st.session_state.dataPdf = None

# Dados em XLSX
if 'dataXlsx' not in st.session_state:
    st.session_state.dataXlsx = None

# ==============================================================================================
# Página inicial, onde são selecionados os campos, filtros e ordenação para gerar o relatório
if st.session_state.pagina == 0:
    relatorio_type = st.selectbox(
    'Selecione a tabela para gerar o relatório:',
    ('Videos', 'Streams', 'Canais', 'Usuários', 'Categorias'), on_change=defineCampos)

    session = DAO.getSession()
    session.expire_on_commit = False

    if st.session_state.query is False:
        if relatorio_type == 'Videos':
            query = DAORelatorioVideos.select(session, None, None, None)    
        elif relatorio_type == 'Streams':
            query = DAORelatorioStreams.select(session, None, None, None)
        elif relatorio_type == 'Canais':
            query = DAORelatorioCanais.select(session, None, None, None)
        elif relatorio_type == 'Usuários':
            query = DAORelatorioUsuarios.select(session, None, None, None)
        elif relatorio_type == 'Categorias':
            query = DAORelatorioCategories.select(session, None, None, None)

        st.session_state.df = pd.read_sql_query(query.statement, con=session.bind)
        session.commit()
        session.close()
    st.session_state.query = True

    # Selecionar os campos das tabelas
    relatorio_fields = st.multiselect(f'Selecione os campos do relatório de {relatorio_type}:', options = st.session_state.df.columns, placeholder = 'Selecionar campo')
    
    # Formulário dos filtros
    st.write('\n')
    st.write("Filtrar por campos:")
    with st.form("myform"):
        f1, f2, f3 = st.columns([1, 1, 1])
        with f1:
            field = st.selectbox("Campo:", options = st.session_state.df.columns)
        with f2:
            comparison = st.selectbox("Comparação:", options = ('igual', 'maior', 'menor', 'maior ou igual', 'menor ou igual', 'diferente de', 'contendo a string'))
        with f3:
            comparison_value = st.text_input("Valor")

        f1, f2, f3 = st.columns([1, 1, 1])
        
        with f2:
            st.write('\n')
            submit = st.form_submit_button(label="Adicionar filtro", on_click=clear_form)

    # Tipo de comparação a ser feita
    if submit and comparison_value:
        map_operation = {
            'igual': f'= ',
            'maior': f'> ',
            'menor': f'< ',
            'maior ou igual': f'>= ',
            'menor ou igual': f'<= ',
            'diferente de': f'!= ',
            'contendo a string': 'LIKE \'%'
        }

        operation = map_operation[comparison]
            
        if st.session_state.df[f'{field}'].dtypes == 'object' and not comparison == 'contendo a string':
            value = f"'{comparison_value}'"
        elif comparison == 'contendo a string':
            value = f"{comparison_value}"
        else:
            value = f'{comparison_value}'

        # Adiciona os filtros
        if st.session_state.qtdFiltros == 0:
            st.session_state.filtros += f"{field} {operation}{value}"
        else:
            st.session_state.filtros += f" AND {field} {operation}{value}"

        # Se a opção "contendo a string" for utilizada
        if comparison == 'contendo a string':
            st.session_state.filtros += '%\''

        # Adiciona filtro
        st.session_state.qtdFiltros = 1
        container = st.empty()
        container.success('Filtro adicionado com sucesso!') 
        time.sleep(3) 
        container.empty() 

    # Caso o valor a ser comparado com o campo não seja preenchido
    if submit and not comparison_value: 
        container = st.empty()
        container.error('Preencha o valor da comparação!') 
        time.sleep(3) 
        container.empty() 

    st.write('\n\n\n\n\n\n')
    st.write('Filtros adicionados:')
    with st.expander(" "):
        st.write(st.session_state.filtros)


    # Formulário de ordenação do relatório
    st.write('\n')
    st.write("Ordenar relatório:")
    with st.form("myform2"):
        o1, o2 = st.columns([1.5, 1.5])
        with o1:
            camposOrdenacao = st.selectbox('Ordenar por:', options = st.session_state.df.columns)
        with o2:
            tipoOrdenacao = st.selectbox(f'Campo {camposOrdenacao} ordenado de modo:', options=('Crescente', 'Decrescente'), index=0)
            #tipoOrdenacao = st.radio(f'Campo {camposOrdenacao} ordenado de modo:', options = ('Crescente', 'Decrescente'), horizontal = True)
        
        st.write('\n\n\n\n\n')
        o1, o2 = st.columns([1, 1])
        
        st.write('\n')
        ordenacao_relatorio = st.form_submit_button(label='Ordenar relatório', on_click=defineOrdenacao)

    if ordenacao_relatorio == 'Crescente':
        ordenacao = 'ASC'
    else:
        ordenacao = 'DESC'
        
    if ordenacao_relatorio:
        st.session_state.ordenacao = f'{camposOrdenacao} {ordenacao}'
        container = st.empty()
        container.success(f'Relatório será ordenado pelo campo {camposOrdenacao} de forma {tipoOrdenacao}!') 
        time.sleep(3) 
        container.empty() 

    st.write('\n\n\n')
    f1, f2, f3 = st.columns([1, 1, 1])

    with f2:
        st.write('\n\n\n\n\n')
        relatorio = st.button('Gerar relatório')

    st.write('\n\n\n\n\n')

    if relatorio:
        status = geraRelatorio()
        if status == -1:
            st.error("Selecione os campos do relatório!")
        else:
            st.session_state.pagina = 1
            st.rerun()

# ==============================================================================================
# Página do relatório
else:
    if st.session_state.relatorio == False:
        # Gerar pdf do relatório
        relatorioPDF()
        with open("relatorio.pdf", "rb") as pdf_file:
            st.session_state.pdfData  = pdf_file.read()

        # Gerar xlsx do relatório
        with open("DB/relatorio.xlsx", "rb") as xlsx_file:
            st.session_state.xlsxData = xlsx_file.read()

    # Exibe dataframe
    st.session_state.relatorio = st.dataframe(st.session_state.dataframe, width=1000, height=500)

    f1, f2, f3 = st.columns([1, 1, 1])
    st.write('\n')

    with f1:
        relatorio_pdf = st.download_button('Exportar relátorio para PDF', data = st.session_state.pdfData,
        file_name="relatorio.pdf")

    with f2:
        relatorio_xlsx= st.download_button('Exportar relátorio para XLSX', data = st.session_state.xlsxData,
        file_name="relatorio.xlsx")

    with f3:
        new_relatorios = st.button("Criar mais relatórios")
    
    # Caso seja selecionada a opção de gerar mais relatórios
    if new_relatorios:
        st.session_state.pagina = 0
        st.session_state.qtdFiltros = 0
        st.session_state.filtros = ""
        st.session_state.ordenacao = None
        st.session_state.relatorio = False
        relatorio_fields = []
        st.rerun()

    with f1:
        relatorio_type = st.selectbox(
            'Selecione o relatório:',
            ('Videos', 'Streams', 'Canais', 'Usuários', 'Categorias'), on_change=defineCampos)

    with f2:
        st.session_state.relatorio_fields = st.multiselect(f'Selecione os campos do relatório de {relatorio_type}:', options=st.session_state.df.columns)

# ==============================================================================================
# Lógica para o gráfico
    if st.session_state.relatorio and 'relatorio_fields' in st.session_state and len(st.session_state.relatorio_fields) >= 2:
        x_column = st.session_state.relatorio_fields[0]
        y_column = st.session_state.relatorio_fields[1]
        grouped_data = st.session_state.df.groupby(x_column)[y_column].count().reset_index()

        st.write('\n\n')
        st.write(f"Gráfico de contagem de {y_column} agrupado por {x_column}:")

        # Use st.pyplot() para exibir a figura Matplotlib
        fig, ax = plt.subplots()
        grouped_data.plot(kind='bar', x=x_column, y=y_column, ax=ax)
        st.pyplot(fig)
