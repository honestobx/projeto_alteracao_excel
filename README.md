Este commit adiciona um comando que permite a atualização de informações em lote diretamente de um arquivo Excel. O arquivo Excel deve estar localizado na subpasta 'excel' e conter as seguintes colunas pegando pelo exemplo que foi feito no command:

- 'Numero' (para identificar registros na tabela ModelTeste1)
- 'Observação' (para atualizar o campo 'obs' da tabela ModelTeste1)
- 'Valor' (para atualizar o campo 'valor' da tabela ModelTeste2, relacionada a ModelTeste1)

### Fluxo do Comando:
1. O comando lê o arquivo Excel usando `pandas` e itera sobre as linhas.
2. Para cada linha:
    - Identifica o registro na tabela `ModelTeste1` usando o campo `numero`.
    - Se encontrar o registro, atualiza o campo 'obs' da `ModelTeste1` e, se aplicável, o campo 'valor' da tabela `ModelTeste2`, que está relacionada pelo campo `model_teste1_id`.
3. Se o registro em `ModelTeste1` ou `ModelTeste2` não for encontrado, uma mensagem de erro é exibida.

### Instruções:
Para executar o comando, coloque o arquivo `alteracao_excel.xlsx` na pasta `excel` dentro do diretório de comandos e rode:

python manage.py <nome_do_comando> (nesse caso python manage.py alteracao)