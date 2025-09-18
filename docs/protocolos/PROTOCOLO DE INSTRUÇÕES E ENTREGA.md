# Protocolo de Instruções e Entrega

## 1. Objetivo
Definir como deve ocorrer a comunicação entre **Estrategista** e **Agente**, assegurando clareza, disciplina e rastreabilidade em todos os projetos.  
Este protocolo se conecta diretamente ao **Protocolo de Papéis e Responsabilidades** (quem faz o quê) e ao **Protocolo de Governança e Continuidade** (como garantir memória e perenidade).

---

## 2. Estrutura da Instrução do Estrategista
Toda instrução enviada ao Agente deve conter:

1. **Cabeçalho LLM↔LLM**  
   - Labels = ↓, 0, ↑  
   - Decisão = argmax(p↓, p0, p↑)  
   - Proibido criar banda neutra adicional  

2. **Objetivo da Etapa**  
   - Clareza sobre o que deve ser implementado.  
   - Nunca ambíguo, nunca genérico demais.  

3. **Requisitos Técnicos**  
   - Definições precisas sobre entradas, saídas, formatos e restrições.  
   - Quando necessário, incluir dtypes, formatos de arquivo, mensagens normativas ou thresholds de qualidade.  

4. **Execução Inicial**  
   - Sempre `dry_run=True`.  
   - Nenhum efeito persistente é autorizado sem validação explícita.  

5. **Persistência**  
   - Permitida somente quando explicitamente instruído.  
   - Deve incluir convenções de versionamento, manifesto e hashing (quando aplicável).  

6. **Checklist Obrigatório**  
   - Cada instrução deve terminar com um checklist enumerado.  
   - O Agente deve garantir que todos os itens do checklist estejam atendidos.  

---

## 3. Regras para o Agente
- Deve responder **exclusivamente** com um bloco único de código (ex.: Python).  
- Esse bloco deve ser **auto-contido** (inclui imports, funções auxiliares e execução).  
- Não pode haver explicações fora do bloco.  
- A primeira entrega de cada etapa é sempre em **modo de simulação** (`dry_run=True`).  
- Se o mesmo erro se repetir **duas vezes consecutivas**, o Agente deve **parar** e formular **dúvidas objetivas** ao Estrategista.  
- O Agente não pode alterar requisitos, antecipar decisões ou improvisar soluções.  

---

## 4. Logs e Relatórios Obrigatórios
Toda execução deve devolver:  
- Estrutura do resultado (ex.: `info()` ou equivalente).  
- Amostra inicial dos dados/outputs (ex.: primeiras linhas ou itens).  
- Intervalo temporal ou dimensional coberto.  
- Contagem total de elementos.  
- Relatório de completude/qualidade (ex.: proporção de campos válidos).  
- Mensagens normativas de erro, quando aplicável.  

---

## 5. Mensagens Normativas
Erros, warnings ou exceções devem sempre ser devolvidos em formato normativo, padronizado. Exemplos genéricos:  

- `VALIDATION_ERROR: estrutura divergente do esperado.`  
- `CHECKLIST_FAILURE: item X não atendido.`  
- `DUPLICATE_ERROR: repetição de resultado detectada.`  

Essas mensagens não mudam entre projetos: cada implementação deve segui-las como contrato de comunicação.

---

## 6. Conexão com os Outros Protocolos
- **Com Papéis e Responsabilidades**: este protocolo regula *como* o Estrategista e o Agente interagem dentro dos papéis já definidos.  
- **Com Governança e Continuidade**: este protocolo fornece o padrão operacional cujos resultados (logs, checklists, mensagens normativas) alimentam a auditoria, os checkpoints e a memória perene.  

Assim, os três documentos juntos garantem que:  
- Ninguém sai do seu papel.  
- Toda comunicação é padronizada.  
- O histórico de decisões e falhas é auditável e reprodutível.  
