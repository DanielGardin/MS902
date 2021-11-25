# MS902
Trabalho final da disciplina MS902 - Tópicos em Ciência de Dados Aplicada a Negócios. O objetivo é criar o backend de um aplicativo de feed de notícias sobre investimento que categoriza as notícias por ativos da B3.<br>
Os arquivos `sheet.py` e `news.py` são módulos para o programa `main.py`. Para iniciar a coleta de notícias é necessário, primeiramente, inserir os arquivos de configuração.

## ⚙️ Arquivos de configuração
O projeto conta com alguns arquivos de configuração e chaves para a API do google sheets que não estão inclusos neste repo. A chave da conta de serviço para a qual insere as notícas no sheets deve ser requisitada na própria plataforma do Google API no formato JSON, renomeada para `key.json` e inserida no mesmo diretório do arquivo `main.py`. Outro arquivo nomeado `config.json` deve ser incluído. Nele, é necessário, nesta versão, apenas uma configuração, como mostra abaixo:
```json
{
  "sheet":"https://docs.google.com/spreadsheets/d/<planilha>"
}
```
Outro arquivo, já neste repo, mas que pode sofrer alterações como desejado é `fontes.json`. Nele está incluso as informações necessárias para buscarmos notícias de uma certa fonte, que são incluídas conforme a estrutura abaixo
```json
{
  ...,

  "<Nome da Fonte>": {
      "url":"<link do rss feed da fonte>",
      "attrs":{"class":"<classe do div do artigo>"}
  }

  ...
}
```

O campo `attrs` designa-se à classe no html da notícia em que o corpo da notícia se encontra. Esse campo será utilizado para a classificação - ainda não implementada.

## 💻 Estado atual e funcionamento
O resultado armazenado pode ser encontrado [neste link](https://docs.google.com/spreadsheets/d/1LHqCDO4NmmtEDAhJyJ0zTfRhE6cjKtJ_KXzyQGdzuxI "Planilha de armazenamento pessoal"). As notícias armazenadas neste link são atualizadas pelo programa em meu próprio computador pessoal com as credenciais do Google API geradas por mim.

## ➡️ Mudanças e features planejadas

Apesar do projeto não estar concluído em sua totalidade, ele funciona como um simples scrapper de páginas que armazena as notícias em um google sheets. Aqui listo uma sequência de mudanças e features que pretendo incluir ao projeto:

* Classificação simples das notícias pelo artigo resultado do scraping de cada notícia.
* Modelo simples de machine learning que tenta prever o assunto da notícia pelo seu conteúdo
* Classificação avançada para distinguir contextos (ex: 'Azul' pode remeter tanto à cor quanto à empresa)
* Mudança do tipo de armazenamento, visando uma possível integração com um Front.
