#coding: utf-8
#analise de textos em português de sistemas de software 
#dados retirados da página do professor Fabio Kon: 
# http://www.ime.usp.br/~kon/ResearchStudents/traducao.html
#
#para executar os teste: python -m doctest -v checagem_texto.py
import codecs
import csv
import re

PALAVRAS_QUE_DEVERIAM_TRADUZIR = "./palavras_deveriam_traduzir.txt"
PALAVRAS_QUE_PODERIAM_TRADUZIR = "./palavras_poderiam_traduzir.txt"
PALAVRAS_MAL_TRADUZIDAS = "./mal_traduzidos.txt"

def checar(nome_do_arquivo,codificacao="utf-8"):
    """
    
    checagem_texto.py nome_do_arquivo [codificacao]
    

    >>> checar("texto_teste.txt")
    linha 1
    fazendo o teste software com e suportar technical debt hack
    _______________________________________________________
    termo em inglês | tradução
    hack | gambiarra
    ________________________________________________
    Termo em Inglês | Tradução Correta | Tradução Indesejável
    software (plural) | sistemas de software, programas | softwares
    ________________________________________________
    Termo em Inglês | Tradução Correta | Tradução Indesejável
    to support | prover, dar suporte, implementar, incluir, comportar, contemplar, oferecer, disponibilizar | suportar (não é errado se usado como sinônimo de sustentar; é apenas feio :-)
    ________________________________________________
    Termo em Inglês | Tradução Correta | Tradução Indesejável
    technical debt | dívida técnica | débito técnico
    ________________________________________________

    """
    dicionarios = lista_dicionarios()
    linhas_do_arquivo = []
    resultados = []
    with codecs.open(nome_do_arquivo,"r",codificacao) as arquivo:
	linhas_do_arquivo = unicode(arquivo.read()).splitlines()
    for linha_numero,linha in enumerate(linhas_do_arquivo,1):
	resultado = consulta_dicionario(linha,dicionarios)
	if resultado != []:
	    resultados.append([resultado,linha_numero,linha])
    imprimir_resultados(resultados,dicionarios,codificacao)
 
def imprimir_resultados(resultados,dicionarios,codificacao):
    for resultado in resultados:
	print "linha "+str(resultado[1])
	try:
	    print str(resultado[2])
	except UnicodeEncodeError:
	    print repr(resultado[2])
	print "_______________________________________________________"
	for lista_dicionario in resultado[0]:
	    if lista_dicionario[0] in [PALAVRAS_QUE_DEVERIAM_TRADUZIR,PALAVRAS_QUE_PODERIAM_TRADUZIR,PALAVRAS_MAL_TRADUZIDAS]:
		print " | ".join(dicionarios[lista_dicionario[0]][0])
		print " | ".join(lista_dicionario[1])
		print "________________________________________________"


def consulta_dicionario(linha, lista_dicionarios):
    """ 
	>>> dicionarios = {"teste":[[u"Termo em Ingles",u"Traducao Correta",u"Traducao Indesejavel"],["a", "b" , "aa"]]} 
	>>> consulta_dicionario(u"aa",dicionarios)
	[['teste', ['a', 'b', 'aa']], ['teste', ['a', 'b', 'aa']]]
	>>> consulta_dicionario(u"a",dicionarios)
	[['teste', ['a', 'b', 'aa']]]
    """
    lista_dicionario = []
    for nome_dicionario in lista_dicionarios:
	dicionario = lista_dicionarios[nome_dicionario]	
	for linhas_dicionario in dicionario:
	    palavra_dicionario = limpa_texto(linhas_dicionario[0])
	    if palavra_dicionario != "" and re.search(palavra_dicionario,linha):
		lista_dicionario.append([nome_dicionario,linhas_dicionario])
	    if len(dicionario[0]) == 3:
		palavra_dicionario2 = limpa_texto(linhas_dicionario[2])
		if palavra_dicionario2 and re.search(palavra_dicionario2,linha):
		    lista_dicionario.append([nome_dicionario,linhas_dicionario])
    return lista_dicionario

def limpa_texto(texto):
    """
    >>> limpa_texto("asdasd (asdasd)")
    'asdasd'
    >>> limpa_texto("[dasd] asdasd")
    'asdasd'
    >>> limpa_texto(u"suportar (não é errado se usado como sinônimo de sustentar; é apenas feio :-)")
    u'suportar'
    """
    prog = re.compile(r"\([^)]*\)|\[[^]]*\]")
    texto =  re.sub(prog,"",texto).strip()
    return texto


def lista_dicionarios():
    """
	gera a lista de dicionarios
	>>> len(lista_dicionarios())
	3
    """
    lista_dicionario = {}
    for arquivo_dicionario in [PALAVRAS_QUE_DEVERIAM_TRADUZIR,PALAVRAS_QUE_PODERIAM_TRADUZIR,PALAVRAS_MAL_TRADUZIDAS]:
	lista_dicionario[arquivo_dicionario] = ler_dicionario(arquivo_dicionario)
    return lista_dicionario


def ler_dicionario(nome_do_arquivo):
    """
    >>> ler_dicionario("teste.txt")
    [['1   2', '3'], ['4   5', '6']]
    """
    with open(nome_do_arquivo,"rU") as arquivo:
	arquivo.seek(0)
	reader = csv.reader(arquivo, delimiter="\t")
	return [linhas for linhas in reader]

def main(argv=None):
    if argv is None:
	argv = sys.argv[1:]
    checar(*argv)

if __name__ == "__main__":
    import sys
    sys.exit(main())
