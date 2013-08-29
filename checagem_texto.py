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



def checar_texto(nome_do_arquivo,codificacao="utf-8"):
    """
    
    python checagem_texto.py nome_do_arquivo [codificacao]

    >>> checar_texto("texto_teste.txt")
    linha 1
    fazendo o teste software com e suportar technical debt hack
    _______________________________________________________
    termo em inglês | tradução
    hack | gambiarra
    __________________________________________
    Termo em Inglês | Tradução Correta | Tradução Indesejável
    software (plural) | sistemas de software, programas | softwares
    support | prover, dar suporte, implementar, incluir, comportar, contemplar, oferecer, disponibilizar | suportar (não é errado se usado como sinônimo de sustentar; é apenas feio :-)
    technical debt | dívida técnica | débito técnico
    __________________________________________

    """
    dicionarios = lista_dicionarios()
    linhas_do_arquivo = []
    resultados = []
    with codecs.open(nome_do_arquivo,"r",codificacao) as arquivo:
        linhas_do_arquivo = arquivo.read().splitlines()
    for linha_numero,linha in enumerate(linhas_do_arquivo,1):
        resultado_consulta = consulta_dicionario(linha,dicionarios)
        if resultado_consulta: 
            resultados.append([resultado_consulta,linha_numero,linha])
    imprimir_resultados(resultados,dicionarios)


def imprimir_resultados(resultados,dicionarios):
    for resultado in resultados:
        resultado_dicionario = resultado[0]
        numero_linha = resultado[1]
        linha = resultado[2]
        print "linha "+str(numero_linha)
        try:
            print str(linha)
        except UnicodeEncodeError:
            print repr(linha)
        print "_______________________________________________________"
        for dicionario in resultado_dicionario:
            if resultado_dicionario[dicionario] != []:
                print " | ".join(dicionarios[dicionario][0])
                for linhas in resultado_dicionario[dicionario]:
                    print " | ".join(linhas)
                print "__________________________________________"


def consulta_dicionario(linha, lista_dicionarios):
    """ 
        >>> dicionarios = {"dicionario1":[[u"Termo em Ingles",u"Traducao Correta",u"Traducao Indesejavel"],["a", "b" , "c"]]} 
        >>> consulta_dicionario(u"aa",dicionarios)
        {'dicionario1': [['a', 'b', 'c']]}
        >>> consulta_dicionario(u"d",dicionarios)
        {}
    """
    lista_resultados = {}
    for nome_dicionario in lista_dicionarios:
        lista_resultados[nome_dicionario] = []
        dicionario = lista_dicionarios[nome_dicionario] 
        for linha_dicionario in dicionario:
            if verifica_linha(linha,linha_dicionario,dicionario):
                lista_resultados[nome_dicionario].append(linha_dicionario)
    remover_chaves_vazias(lista_resultados)
    return lista_resultados

def remover_chaves_vazias(dict):
    """
    >>> dicionario1 = {'dicionario1':["com coisa"]}
    >>> remover_chaves_vazias(dicionario1)
    >>> dicionario1 == {'dicionario1':["com coisa"]}
    True
    >>> dicionario2 = {'dicionario2':[]}
    >>> remover_chaves_vazias(dicionario2)
    >>> dicionario2 == {}
    True
    """
    chaves_vazias = [k for k,v in dict.iteritems() if v == []]
    for k in chaves_vazias:
	del dict[k]
    

def verifica_linha(linha_texto, linha_dicionario,dicionario):
    lista_palavra_dicionario = []
    lista_palavra_dicionario.append(linha_dicionario[0])
    if len(dicionario[0]) == 3:
        lista_palavra_dicionario.append(linha_dicionario[2])    
    for palavra_dicionario in lista_palavra_dicionario:
        if verifica_palavra(palavra_dicionario,linha_texto):
            return True
    return False

def verifica_palavra(palavra,linha):
    """
        verifica se a palavra aparece na linha
        >>> verifica_palavra("texto longo","um texto longo")
        True
        >>> verifica_palavra("texto curto","um texto longo")
        False
    """
    palavra_limpa =  limpa_texto(palavra)
    return palavra and re.search(palavra_limpa,linha) != None


def limpa_texto(texto):
    """
        limpa o texto retirando textos entre chaves e parenteses
    >>> limpa_texto("palavra (detalhe)")
    'palavra'
    >>> limpa_texto("[detalhe] palavra")
    'palavra'
    >>> limpa_texto(u"palavra_unicode (não é string comum)")
    u'palavra_unicode'
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


def csv_unireader(f, encoding="utf-8"):
    """
    abre um arquivo utf-8 com a lib csv
    """
    for row in csv.reader(codecs.iterencode(codecs.iterdecode(f, encoding), "utf-8"), delimiter="\t"):
        yield [e.decode("utf-8") for e in row]

def ler_dicionario(nome_do_arquivo):
    """
    >>> ler_dicionario("teste.txt")
    [[u'1', u'2', u'3'], [u'4', u'5', u'6']]
    """
    with open(nome_do_arquivo,"rU") as arquivo:
        reader = csv_unireader(arquivo)
        return [linhas for linhas in reader]

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    checar_texto(*argv)

if __name__ == "__main__":
    import sys
    sys.exit(main())
