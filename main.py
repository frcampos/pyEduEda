# Este é um exemplo de uma amostra em Python script, para realizar de forma
# sistemática a conversão de imagens com uma determinada resolução, normalmente retiradas de máquinas fotográfica, telemóveis
# e outros tipos de dispositivos, para a preparação de imagens a colocar em sítios web.
# Foi usado nos testes o PyCharm - help at https://www.jetbrains.com/help/pycharm/
# Assim o exemplo de script para em "batch" converter imagens em formato jpg a partir de imagens de maior resolução para colocação
# no sitio de acordo com largura e altura programavel, assim como qualidade
# Nota: No PyCharm para instalar modulos ir à opção "Terminal"
# PIL é a livraria de manipulação de imagem
# os, glob e errno é relativamente ao trabalho com ficheiros e códigos de erro do sistema Operativo
# criado por Fernando Rui Campos 13- 22 fevereiro 2023. Testes realizados com mais de 2000 imagens de diversas resoluções de
# origem, tendo como final a qualidade programada na variável valor_perc_qualidade = 75 e dimensões através das
# variáveis, resol_valor_largura = 900 e resol_valor_altura = 735.
# Os valores acima são meramente indicativos para as notícias
# utilizar o ficheiro de configuração de forma a ser possivel realizar executáveis para windows e MacOs.

import PIL
import os
import glob
import errno
from PIL import Image

import os
import configparser

# Aplicação para converter imagens para a web a partir de parametros de entrada em ficheiro
# que deverá estar na mesma pasta da aplicação e que tem a designação configimagens.ini .
# cria uma instância do objeto ConfigParser

FICHEIRO_CONFIGURACAO = 'config.ini'
# pasta com imagens de origem
global pasta_imagem
#
global caminho_img_nresolucao
global caminho_imgs_comprimido
global num_files_max
global valor_perc_qualidade
global resol_valor_largura
global resol_valor_altura
global ALGORITMO_RESIZED
ADD_name_file_compressed = ''
ADD_name_file_resized = ''

# Caso seja criado um executável é necessário obter o caminho onde este corre para que o congig.ini seja encontrado

# Obter o diretório onde o script está a ser executado
script_dir = os.path.dirname(os.path.abspath(__file__))

# Obter o caminho completo para o arquivo de configuração
config_file = os.path.join(script_dir, FICHEIRO_CONFIGURACAO)

# Carreguar o arquivo de configuração usando o configparser
config = configparser.ConfigParser()

# lê o arquivo de configuração
arquivos_lidos = config.read(config_file)

# verifica se o arquivo foi lido com sucesso
if not arquivos_lidos:
    raise ValueError(
        'Não foi possível ler o arquivo de configuração com os caminhos onde se encontram as imagens a converter')

# verifica se a seção e as variáveis de configuração existem
if not config.has_section('imagens'):
    raise ValueError('A seção "imagens" não existe no arquivo de configuração')
if not config.has_option('imagens', 'caminho'):
    raise ValueError('A variável "caminho" não existe na seção "imagens" do arquivo de configuração')
if not config.has_option('imagens', 'caminhocomprimido'):
    raise ValueError('A variável "caminhocomprimido" não existe na seção "imagens" do arquivo de configuração')
if not config.has_option('imagens', 'caminhocomprimidonresolucao'):
    raise ValueError(
        'A variável "caminhocomprimidonresolucao" não existe na seção "imagens" do arquivo de configuração')
if not config.has_option('imagens', 'largura'):
    largura = 1270
    raise ValueError('A variável "largura" não existe na seção "imagens" do arquivo de configuração')
if not config.has_option('imagens', 'altura'):
    altura = 720
    raise ValueError('A variável "altura" não existe na seção "imagens" do arquivo de configuração')
if not config.has_option('imagens', 'qualidade'):
    qualidade = 75
    raise ValueError('A variável "qualidade" não existe na seção "imagens" do arquivo de configuração')
if not config.has_option('imagens', 'numeroficheiros'):
    numeroficheirosnumeroficheiros = 20
    raise ValueError('A variável "numeroficheiros" não existe na seção "imagens" do arquivo de configuração')

# acessa as variáveis de configuração
try:

    pasta_imagem = config.get('imagens', 'caminho')
    caminho_imgs_comprimido = config.get('imagens', 'caminhocomprimido')
    caminho_img_nresolucao = config.get('imagens', 'caminhocomprimidonresolucao')
    resol_valor_largura = config.getint('imagens', 'largura')
    resol_valor_altura = config.getint('imagens', 'altura')
    valor_perc_qualidade = config.getint('imagens', 'qualidade')
    num_files_max = config.getint('imagens', 'numeroficheiros')

except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as epa:
    raise ValueError('Erro ao obter as variáveis de configuração: não é possivel continual. A sair ...' + str(epa))
    exit(2)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'{name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('A processar script Phython para converter e otimizar imagens para a web a partir de uma pasta')

# pasta de origem onde se encontram os ficheiros a comprimir. Apenas deverá ter ficheiros de imagem
# Variaveis globais não necessita de acordo com a Linguagem Python, mas é apenas para referência da existência


# Numero máximo de ficheiros a converter, se colocar valor superior ao número de ficheiros não tem qualquer efeito
# valor_perc_qualidade deve ser teóricamente ser superior a 30 e inferior a 90, dependendo do tipo de imagem
# Valor de 75 equivale a 75% de qualidade o que segundo autores não se nota alteração. No entanto em alguns casos
# e dependendo da imagem de onde se deve usar (noticias,  carroussel) a que corresponde a 400x320 ou 860x420 px
# resol_valor_largura em pixeis - px
# resol_valor_altura em pixeis  - px
# possibilidade de programação do tipo de algoritmo utilizado para a alteração da resolução
# A livraria/modulo Pillow, permite vários,  NEAREST, BOX, BILINEAR, HAMMING, BICUBIC, LANCZOS
# A constituição da variável é por exemplo  Image.Resampling.BOX ou Image.Resampling.LANCZOS
# A variável ALGORITMO_RESIZED permite alterar o tipo de algoritmo de alteração de tamanho
# Testes de largura 1350x422 no carroussel e 900x720 nas noticias (valor máximo), i.e. relação , r= 1,25.
# No caso do carrousel principal o valor máximo é de 1344x420 , i.e. relação , r= 3.2.
# A densidade máxima a usar deve ser de :  ppi 150 por causa dos novos equipamentos, embora o satandard seja de 72x72 minimo.
# O valor máximo para a densidade deve ser  de 150 ppi por imagem. Testes realizados com 2626 imagens.

# De momento o algoritmo é fixo
ALGORITMO_RESIZED = Image.Resampling.BICUBIC

# pasta de origem dos ficheiros antes da  compressão - "pasta_imagem"

# pasta de destino dos ficheiros após compressão
# caminho_imgs_comprimido = '/Users/fernandocampos/testes/comprimidosite/'
# Caminho onde se encontram as imagens a converter. Deve ser adaptado de acordo com a configuração
# pasta_imagem = '/Users/fernandocampos/testes/naocomprimido/'
# caminho_img_nresolucao = '/Users/fernandocampos/testes/comprimidoresized/'


print(f"A verificar os requisitos para conversão de imagens para a Web")
if os.path.exists(pasta_imagem):
    print(f"Existe a pasta de origem de imagens para conversão em {pasta_imagem}")
else:
    print(
        f"O caminho ou pasta de imagens fonte não  existe ou está em outo caminho de acordo com o definido em {pasta_imagem}. A sair...")
    exit(2)
if os.path.exists(caminho_imgs_comprimido):
    print(f"Existe o caminho ou pasta de imagens destino após compressão nivel 1 imagens para conversão em {caminho_imgs_comprimido}")
else:
    print(
        f"O caminho ou pasta de imagens destino após compressão nivel 1  não  existe ou está em outro caminho de acordo com o definido em {caminho_imgs_comprimido}. A sair...")
    exit(2)
if os.path.exists(caminho_img_nresolucao):
    print(f"Existe o caminho ou pasta de imagens destino após compressão e ajuste imagens nivel 2 para conversão em {caminho_img_nresolucao}")
else:
    print(
        f"O caminho ou pasta de imagens destino após compressão e ajuste nivel 2 não  existe ou está em outo caminho de acordo com o definido em {caminho_img_nresolucao}. A sair...")
    exit(2)
# Obtem a lista de ficheiros de imagem
# Criação de lista com ficheiros

files = os.listdir(pasta_imagem)

# Listar todos os ficheiros e pastas utilizando a função os.listdir()

print(f'Estes são os ficheiros da diretoria corrente: {files}')
# Obter o numero de ficheiros encontrados
# atenção que a posição 0 conta!
# Criar Loop de manipulação ficheiros
# definir img_size_width e img_size_height , i.e. largura e altura da imagem

# Verifica o numero de interações pelo numero de ficheiros existentes na pasta ou entao pelo numero máximo definido em
# num_files_max enquanto variavel global
# Só pode conter ficheiros do tipo jpg

if num_files_max <= 3:
    print(
        f"Numero de ficheiros máximos introduzidos na variável num_files_max {num_files_max} é inferior ao valor minimo, a ajustar ...")
    num_files_max = 3
if valor_perc_qualidade <= 29:
    print(
        f" Valor de qualidade tem de ser superior ou igual a 50. a ajustar valor minimo da qualidade {valor_perc_qualidade} da imagem final para 50 ")
    valor_perc_qualidade = 50

numero_itens = len(files) - 1

if numero_itens <= 0:
    print(
        f"O numero de imagens existentes para processamento na pasta de origem {pasta_imagem} é inferior a 1. A sair...")
    exit(2)

if num_files_max > numero_itens + 1:
    num_files_max = numero_itens + 1
    print(
        f"O numero de imagens para processamento programado na variável num_files_max  {num_files_max} é inferior ao existente em na pasta de origem {pasta_imagem}. A ajustar numero de ficheiros a processar ")
i = 0
while (i <= numero_itens and i <= num_files_max - 1):

    print("O ficheiro encontrado corresponde a posição", i, "da lista de ficheiros é:", files[i])
    if files[i] == '.DS_Store':
        print(f'Não processado ', files[i])
        i = i + 1
        caminho_completo_imagem = pasta_imagem + files[i]
    else:
        caminho_completo_imagem = pasta_imagem + files[i]

    image = Image.open(caminho_completo_imagem)

    # rgb_im = image.convert("RGB")
    name_file_compressed = caminho_imgs_comprimido + ADD_name_file_compressed + files[i]
    name_file_resized = caminho_img_nresolucao + ADD_name_file_resized + files[i]
    try:

        image.save(name_file_compressed, 'webp', optimize=True, quality=valor_perc_qualidade)

        img_resize = image.resize((resol_valor_largura, resol_valor_altura), ALGORITMO_RESIZED)
        img_resize.save(name_file_compressed)

    except IOError as exc:

        if exc.errno == errno.ENOENT:
            print(exc.strerror)
            print("this will print")
            # handle one way
        elif exc.errno == errno.EBADF:
            print(exc.strerror)
            print("this will not print")
            # handle another way

    i = i + 1

# Vai ser aplicado a alteração para a resolução final a partir do ficheiro comprimido
# Os ficheiros encontram-se na pasta

# Necessário ler a pasta e aplicar o algoritmo de resize sem compressão


files_new = os.listdir(caminho_imgs_comprimido)
numero_itens = len(files_new) - 1
# Feito compensação para efeitos de simplificação quando existe ficheiro DSTORE e duas pastas não passiveis
# de serem processadas.
i = 0


while (i <= numero_itens + 3 and i <= num_files_max - 1):
    if i > numero_itens:
        print("Atingido o numero máximo de imagens a processar")
        exit (0)
    print(f"O ficheiro ***comprimido*** corresponde a posição", {i}, "da lista de ficheiros é:", {files_new[i]},
          "em caso de sucesso é gravado na pasta ", caminho_imgs_comprimido)
    if files_new[i] == '.DS_Store' or files_new[i] == caminho_img_nresolucao or files_new[i] == caminho_imgs_comprimido:
        print(f'Não processado  por ser .DS_STORE ou resized, ou rescomprimido - pastas e ficheiros não processados',
              files_new[i])
        i = i + 1
        # por existirem duas pastas e 1 ficheiro não reconhecido na pasta
    else:
        caminho_completo_imagem = caminho_imgs_comprimido + files_new[i]

    caminho_completo_imagem = caminho_imgs_comprimido + files_new[i]
    image = Image.open(caminho_completo_imagem)

    # rgb_im = image.convert("RGB")
    name_file_compressed = caminho_img_nresolucao + '' + files_new[i]

    try:

        img_resize_compressed = image.resize((resol_valor_largura, resol_valor_altura), ALGORITMO_RESIZED)

        img_resize_compressed.save(name_file_compressed)
        # comprimir , fazer testes com e sem abertura previa do ficheiro
        # image = Image.open(name_file_compressed)

        image.save(name_file_compressed, 'webp', optimize=True, quality=valor_perc_qualidade)


    except IOError as exc:

        if exc.errno == errno.ENOENT:
            print(exc.strerror)
            print("this will print")
            # handle one way
        elif exc.errno == errno.EBADF:
            print(exc.strerror)
            print("this will not print")
            # handle another way

    i = i + 1

exit(0)
