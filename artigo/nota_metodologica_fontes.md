# Nota metodológica de atualização — 20/10/2026

## Fontes e desenho de comparação

A página oficial da Administração Federal das Finanças da Suíça informa que o modelo GFS aplica o padrão de estatísticas fiscais do FMI (GFSM 2014) e atende à comparabilidade internacional, enquanto o modelo FS se baseia no modelo contábil harmonizado para cantões e comunas (HAM2) e prioriza comparabilidade nacional. A fonte informa também que há resultados provisórios publicados na primavera e resultados definitivos no verão. Na análise, registrar o status do ano mais recente e não tratar dados provisórios como definitivos.

Fontes oficiais principais:
- SICONFI / API e documentação: https://apidatalake.tesouro.gov.br/docs/siconfi/
- Portal de estatísticas financeiras da FFA/EFV: https://www.efv.admin.ch/en/overview-financial-statistics-data
- Dados abertos FFA/EFV: https://www.efv.admin.ch/en/open-government-data-en
- IBGE/SIDRA: https://sidra.ibge.gov.br/

## Situação de acesso aos dados nesta execução

O ambiente de execução atual não conseguiu resolver os domínios externos por DNS; portanto, os arquivos brutos oficiais não foram baixados aqui. O script `codigo/baixar_dados_oficiais.py` está preparado para execução em computador com acesso à internet, e seus logs deverão ser conferidos. Não declarar que o download foi concluído antes de verificar os arquivos e os registros de execução.

## Protocolo mínimo de validação
1. Preservar resposta bruta e URL exata de cada chamada.
2. Confirmar exercício, código do ente, anexo/conta, unidade, estágio e status de homologação/retificação.
3. Conferir paginação/limites da API e se a resposta contém dados, não apenas mensagem de erro.
4. Construir dicionário de rubricas e registrar qualquer quebra de classificação.
5. Deflacionar as séries monetárias brasileiras pelo IPCA até ano-base explícito, usando a mesma metodologia em todos os anos.
6. Para Suíça, registrar modelo (FS/GFS), nível de governo, unidade monetária e situação provisória/definitiva.
7. Comparar preferencialmente proporções e indicadores per capita apenas quando conceitos e denominadores forem compatíveis.
8. Manter ausências como ausências; nunca substituir automaticamente por zero.

## Literatura

A revisão de Lago, Lago-Peñas e Martinez-Vazquez (2024), DOI 10.1007/s10797-023-09816-7, foi usada como mapa bibliográfico para identificar literatura de transferências, esforço tributário, efeito flypaper, equalização, autonomia e accountability. A matriz candidata contém artigos identificados nas referências e em páginas editoriais; metadados sem DOI confirmado estão assinalados e devem ser conferidos. A matriz não equivale a leitura integral nem cumpre, por si só, a exigência de 80 artigos discutidos no texto.
