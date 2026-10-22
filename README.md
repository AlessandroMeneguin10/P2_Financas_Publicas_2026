# P2 — Finanças do Setor Público: Suíça, Quixadá e Canindé

**Matrícula:** 242026481  
**Unidades atribuídas:** Suíça; Quixadá/CE; Canindé/CE  
**Prazo informado:** 25/10/2026

## Situação deste pacote
Este pacote é uma estrutura de trabalho reproduzível construída a partir do material da P1 disponibilizado na conversa e de fontes oficiais localizadas. **Não é uma versão final pronta para entrega**: os valores municipais transcritos da P1 estão guardados apenas como referência histórica e ainda precisam ser validados contra as bases oficiais. Não se deve chamar esses números de valores reais até confirmar o deflator aplicado.

## Conteúdo
- `dados/base_p1_transcrita_nao_validada.csv`: tabela de receitas e despesas transcrita do material anterior; preservar como referência, não usar como base oficial final sem validação.
- `dados/dicionario_variaveis.csv`: dicionário inicial de variáveis, unidades e tratamentos.
- `dados/log_atualizacoes.csv`: registro de mudanças e pendências.
- `dados/matriz_literatura_candidata.csv`: matriz de artigos candidatos, organizada por eixo temático e estado de verificação. Não equivale a 80 artigos já lidos/discutidos.
- `codigo/analise_p2.py`: pipeline exploratório para checagem, indicadores, gráficos e exportação.
- `codigo/requirements.txt`: bibliotecas Python.
- `artigo/rascunho_artigo.md`: estrutura e redação-base a ser completada após validar os dados e revisar a literatura.
- `analise_p2.ipynb`: notebook de execução equivalente.

## Fontes oficiais prioritárias
1. SICONFI / Tesouro Nacional — DCA, RREO e dados fiscais municipais: https://apidatalake.tesouro.gov.br/docs/siconfi/ e https://siconfi.tesouro.gov.br/
2. IBGE — população, PIB municipal e IPCA: https://www.ibge.gov.br/ e https://sidra.ibge.gov.br/
3. Administração Federal das Finanças da Suíça (FFA/EFV) — estatísticas fiscais FS/GFS, níveis federal, cantonal e municipal: https://www.efv.admin.ch/en/overview-financial-statistics-data
4. Dados oficiais suíços em formato aberto: https://www.efv.admin.ch/en/open-government-data-en

## Como executar
Instale Python 3.10+ e execute:
```bash
pip install -r codigo/requirements.txt
python codigo/analise_p2.py
```
O script lê a tabela histórica transcrita e executa auditorias e gráficos descritivos. Para resultados finais, acrescente os dados oficiais baixados, guarde os arquivos brutos sem alteração e registre URLs, datas de acesso, cobertura, unidades e eventuais revisões.

## Regras metodológicas
- Não substituir valores ausentes por zero.
- Não comparar valores nominais de anos diferentes como se fossem reais.
- Não comparar diretamente R$ e CHF sem uma métrica comum e justificativa.
- Comparar a Suíça em nível nacional com municípios brasileiros exige reconhecer a diferença de escala e de competências fiscais. Sempre que possível, usar proporções do PIB, valores per capita e conceitos harmonizados.
- Correlação não demonstra causalidade.
- A literatura científica precisa conter pelo menos 80 artigos de periódicos distintos, citados e discutidos no texto conforme as instruções da disciplina. A lista bibliográfica não deve ser preenchida com referências inventadas; o rascunho mantém essa etapa explícita como pendência.

## Integridade e reaproveitamento
O material da P1 é usado como base de continuidade, não como evidência automaticamente validada. Registre no artigo e no log quais arquivos/códigos foram reaproveitados, quais mudanças foram feitas e quais números foram conferidos de novo nas fontes oficiais. Confira as regras do professor sobre atribuição do trabalho anterior.

## Atualização desta versão
- Acrescentado `codigo/baixar_dados_oficiais.py`, que tenta obter dados brutos da DCA/SICONFI para Canindé (2302800) e Quixadá (2311306), exercícios 2015–2024, além de arquivos de estatísticas financeiras suíças publicados pela Federal Finance Administration. Respeita intervalo de 1,1 s entre chamadas SICONFI, salva logs e não imputa valores.
- Acrescentado `dados/fontes_oficiais_e_cientificas.csv` e `dados/LEIA-ME_fontes.md`, com fontes oficiais e artigos identificados em páginas de periódicos/portais acadêmicos.
- A execução de download depende de acesso à internet no computador do usuário e ainda precisa ser seguida por seleção do anexo/conta, conferência de homologação e retificações, normalização e documentação de unidades. Não afirmar que os arquivos foram baixados até verificar os logs.
- A bibliografia continua abaixo da exigência de 80 artigos científicos distintos. Não entregar como versão final até completar a revisão bibliográfica e incorporar citações reais no texto.

### Execução do extrator
Na raiz do projeto:
```bash
pip install -r codigo/requirements.txt
python codigo/baixar_dados_oficiais.py
```
Os arquivos baixados são gravados em `dados/brutos_oficiais/`. A série inicial usa 2015–2024 como janela de trabalho para tentar garantir período fechado e comum entre fontes; se a cobertura definitiva não permitir, documentar a janela efetivamente usada em vez de preencher lacunas.


### Pesquisa bibliográfica acrescentada (20/10/2026)
- Incluída síntese crítica inicial sobre efeito flypaper, crowding-out/crowding-in, equalização, autonomia e diferenças institucionais Brasil–Suíça.
- Incluída matriz de artigos candidatos construída a partir de metadados de periódicos e da revisão aberta de Lago, Lago-Peñas e Martinez-Vazquez (2024), DOI https://doi.org/10.1007/s10797-023-09816-7.
- Muitos registros ainda precisam de leitura integral e verificação individual de DOI/paginação; a exigência de 80 artigos efetivamente citados e discutidos não está concluída.
- Não foi possível baixar dados oficiais nesta execução porque o ambiente não resolveu os domínios externos por DNS. Nenhum arquivo oficial bruto deve ser considerado presente sem conferir `dados/brutos_oficiais/` e os logs do extrator.
