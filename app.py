
import streamlit as st
import utils
from pandas import read_csv

icon = 'https://bluefocus.com.br/sites/default/files/styles/medium/public/icon-financeiro.png'

st.set_page_config(
	layout='wide', 
	page_title='Tratamento das Fontes de Dados',
	page_icon=icon,
	initial_sidebar_state='collapsed'
)

st.write('''
# Tratamento das Fontes de Dados - SES/MA
''')

c1, c2, c3, c4 = st.columns(4)
with c1:
	type_problem = st.selectbox(
			label='Fonte de dados:',
			options=[
				'FNS', 'Extrato Bancário', 'SIGEF - Listar Ordem',
				'SIGEF - PP', 'SIGEF - Execução Financeira', 'SIGEF - NL',
				'SIGEF - Execução Orçamentária', 'SIGEF - Empenho',
				'SIGEF - Observação', 'SIGEF - Detalhar Conta (Saldo)'
			]
		)
with c2:
	info_skip = st.number_input(label = 'Linhas para pular:', value=0)
with c3:
	info_range1 = st.text_input(label='Coluna Inicial:', help='ex: A ou a')
with c4:
	info_range2 = st.text_input(label='Coluna Final:', help='ex: B ou b')

c5, c6 = st.columns(2)

with c5:
	file = st.file_uploader('Navegar pelo Computador:', ['xlsx', 'xls'])
	st.image('logo_ses.png')
with c6:
	st.write('''
	### Documentação
	Dúvidas sobre as informações apresentadas? Leia a [Documentação](https://github.com/tiagolofi/sesma_app/raw/main/Documenta%C3%A7%C3%A3o%20de%20Dados%20Fornecidos%20pelo%20SESMA.pdf)

	### Descrição do App
	Aplicação para limpeza de dados das principais bases de dados usadas 
	pelo Controle Financeiro da Secretaria de Estado da Saúde do Maranhão. 
	Esta aplicação possui diretrizes de segurança e recebe manutenção constante.
	### Sugestões de Consulta
	PP - Em média pula 21 linhas, começa em B e termina em M;
	
	Listar Ordem - Varia entre 19 e 26 linhas para pular, começa em A e termina em H;
	
	Execução Financeira - Em média pula 19 linhas, começa sempre em C e termina em L;
	(Obs: é possível tratar o relatório 'Nota Empenho Célula' imprimindo apenas a nível de poder.)

	Extrato Bancário - Pula duas linhas, começa em A e termina em J;

	NL - Em média pula 13 linhas, começa em B e termina em P.

	Execução Orçamentária - pula 17 linhas, começa em B e termina em Z.

	Empenho - pula 15 linhas, começa em C e termina em M.

	Observação - pula 8 linhas, começa em C e termina em J.

	Detalhar Conta - pula 20, começa com B e termina com G.
	''')

try:
	info_range = info_range1.upper()+':'+info_range2.upper()
except:
	pass

def create_data():
	if type_problem == 'FNS':
		st.warning(
			'Selecione uma linha antes do cabeçalho da planilha (onde ficam os nomes das colunas).'
		)
		tabela = utils.fns(
			file = file,
			skip = info_skip,
			range_cols = info_range
		)
	elif type_problem == 'SIGEF - PP':
		st.warning(
			'Selecione a linha onde apareça o nome do primeiro credor.'
		)
		tabela = utils.sigef(
			file=file,
			skip=info_skip,
			range_cols=info_range
		)
	elif type_problem == 'SIGEF - Listar Ordem':
		st.warning(
			'Selecione a linha onde apareça a primeira ordem bancária.'
		)
		tabela = utils.sigef2(
			file=file,
			skip=info_skip,
			range_cols=info_range
		)
	elif type_problem == 'SIGEF - Execução Financeira':
		st.warning(
			'Selecione a primeira linha onde apareça o número do empenho e a partir da coluna C.'
		)
		tabela = utils.sigef3(
			file=file,
			skip=info_skip,
			range_cols=info_range
		)
	elif type_problem == 'SIGEF - NL':
		st.warning(
			'Selecione a linha do cabeçalho da planilha (onde ficam os nomes das colunas).'
		)
		tabela = utils.sigef4(
			file=file,
			skip=info_skip,
			range_cols=info_range
		)
	elif type_problem == 'SIGEF - Execução Orçamentária':
		st.warning(
			'Selecione a linha do cabeçalho da planilha (onde ficam os nomes das colunas).'
		)
		tabela = utils.sigef5(
			file=file,
			skip=info_skip,
			range_cols=info_range
		)
	elif type_problem == 'SIGEF - Empenho':
		st.warning(
			'Selecione a linha onde apareça o valor total empenhado.'
		)
		tabela = utils.sigef6(
			file=file,
			skip=info_skip,
			range_cols=info_range
		)
	elif type_problem == 'SIGEF - Observação':
		st.warning(
			'Selecione a linha onde apareça o primeiro número de ordem bancária.'
		)
		tabela = utils.sigef7(
			file=file,
			skip=info_skip,
			range_cols=info_range
		)
	elif type_problem == 'SIGEF - Detalhar Conta (Saldo)':
		st.warning(
			'Selecione a linha onde apareça o primeiro número de conta'
		)
		tabela = utils.sigef8(
			file=file,
			skip=info_skip,
			range_cols=info_range
		)
	elif type_problem == 'Extrato Bancário':
		st.warning(
			'Selecione uma linha antes do primeiro valor de Fonte de Recurso.'
		)
		tabela = utils.extrato(
			file=file,
			skip=info_skip,
			range_cols=info_range
		)
	return tabela

try:
	if st.button('Visualizar planilha'):
		try:
			tabela = create_data()
			st.success('Limpeza feita com sucesso!')
		except:
			st.error('Insira um arquivo excel ou defina corretamente as características da planilha!')
			st.stop()
		try:
			exportable = utils.export_data(data=tabela)
		except:
			st.error('Sem arquivo para exportar...')
			st.stop() 
		try:
			with st.spinner('Tratando informações...'):
				st.write(tabela)
		except:
			st.error('Não é possível exibir a planilha!')
			st.stop()
		st.download_button(
				'Exportar planilha', 
				data=exportable,
				file_name=type_problem+'.csv',
				mime='text/csv'
			)
	else:
		st.stop()	
except:
	st.stop()
