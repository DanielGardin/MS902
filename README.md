# MS902
Trabalho final da disciplina MS902 - Tópicos em Ciência de Dados Aplicada a Negócios. O objetivo é criar o backend de um aplicativo de feed de notícias sobre investimento que categoriza as notícias por ativos da b3. 

## Arquivos

O projeto conta com alguns arquivos de configuração e chaves para a API do google sheets que não estão inclusos neste repo. A chave da conta de serviço para a qual insere as notícas no sheets deve ser requisitada na própria plataforma do Google API no formato JSON, renomeada para `key.json` e inserida no mesmo diretório do arquivo `main.py`

## Mudanças e features planejadas

Apesar do projeto não estar concluído em sua totalidade, ele funciona como um simples scrapper de páginas que armazena as notícias em um google sheets. Aqui listo uma sequência de mudanças e features que pretendo incluir ao projeto:

* Classificação simples das notícias pelo artigo resultado do scraping de cada notícia.
* Modelo simples de machine learning que tenta prever o assunto da notícia pelo seu conteúdo
* Classificação avançada para distinguir contextos (ex: 'Azul' pode remeter tanto à cor quanto à empresa)
* Mudança do tipo de armazenamento, visando uma possível integração com um Front.
