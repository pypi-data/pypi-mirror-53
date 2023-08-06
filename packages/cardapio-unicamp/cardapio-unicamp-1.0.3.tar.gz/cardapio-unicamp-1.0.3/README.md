# cardapio-unicamp

## About

A menu fetcher for Unicamp's (University of Campinas) restaurant. 

Since this program is targeted at Unicamp's students and to make it more
accessible to them, the remaining of this document as well as the program's
parameter names and help text are written in portuguese.

## Sobre

Este programa oferece uma interface de linha de comando para obter o cardápio
do bandejão da Unicamp. 

Este não é um programa oficial da Unicamp e apenas obtém as informações do site
oficial da universidade, tendo como objetivo facilitar o acesso ao cardápio
pelos alunos sem que haja necessidade de utilizar o navegador de internet para
isso.

## Requisitos

É necessário ter o python 3 e seu gerenciador de pacotes, pip, instalados.

**Não há suporte para python 2.**

## Instalação

Para instalar o programa para o usuário atual, basta utilizar o seguinte
comando:

`pip install --user cardapio-unicamp`

Outra opção é instalar para todos os usuários da máquina.
Essa alternativa requer que o comando seja executado como administrador, por
meio do uso do comando `sudo` no caso de Linux, por exemplo.
Para instalar para todos os usuários:

`pip install cardapio-unicamp`

## Utilização

O uso mais básico do programa é digitar na linha de comando apenas o nome do
comando:

`cardapio-unicamp`

Esse comando mostrará o cardápio da próxima refeição.

### Parâmetros

É possível informar quais dos pratos das refeições deverão ser mostrados,
através dos parâmetros `--base`, `--principal`, `--salada`, `--sobremesa` ou
`--suco`, além do `--obs` para mostrar as observações.
Caso nenhum desses parâmetros seja utilizado, o padrão é mostrar todos os
pratos e as observações.

Caso o cardápio vegetariano seja o de interesse, basta utilizar `--vegetariano`
no comando.

O dia de interesse pode ser especificado através de `--dia DIA`, onde DIA deve
ser o dia especificado no formato `aaaa-mm-dd` (ano, mês e dia).
Existem, no entanto, duas macros, que podem ser utilizadas no lugar de
`aaaa-mm-dd`: `hoje`, para o dia de hoje, e `proximo`, para o próximo dia de
semana.

As refeições cujos cardápios serão mostrados podem ser escolhidas com os
parâmetros `--almoco`, `--jantar` e `--cafe`.
Caso nenhuma seja escolhida, e o dia tenha sido especificado, o padrão é
mostrar todas, enquanto que se o dia não tiver sido especificado, o padrão é
mostrar apenas a próxima refeição informada (próximo jantar, se tiver sido
passado `--jantar`, mas não `--dia`, por exemplo).

O parâmetro `--sem-cabecalho` pode ser utilizado para suprimir todos os
cabeçalhos, tanto o nome e dia de cada refeição quanto o nome de cada prato.
Útil caso deseje-se processar a saída com outro programa.

O parâmetro `--primeiro` faz com que apenas o primeiro item de cada prato seja
mostrado.
É principalmente útil para o prato principal, em que é comum haver mais de um
item.
Obs: Esse efeito se aplica também às observações.

O fato de o comportamento padrão depender dos parâmetros informados pode
parecer estranho à primeira vista, mas foi elaborado de forma a dar o resultado
mais próximo do que o usuário deseja.
Conforme o comando for utilizado, esse comportamento se mostrará conveniente.

## Autor

Nícolas F. R. A. Prado ([nfraprado](https://gitlab.com/nfraprado))
