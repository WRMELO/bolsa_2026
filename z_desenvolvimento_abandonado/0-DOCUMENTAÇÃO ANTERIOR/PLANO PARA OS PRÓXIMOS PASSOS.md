### 📝 Recomendação prática

1. **🚩 Congele PETR4 agora como “baseline unitário”**
    
    - Salve tudo em `/models_individuais/PETR4.SA/` (model, scaler, SHAP, métricas).
        
    - Commit no Git + log no `controles/log_arquivos_gerados.csv`.
        
2. **🔄 Generalize o notebook para ser “ticker-agnóstico”**
    
    - Substitua caminhos fixos por `TICKER = "<ativo>.SA"` e crie uma função `carregar_dados(ticker)`.
        
    - Mantenha as mesmas barras de progresso (`tqdm`) e cabeçalhos `# 🔧 ETAPA:`.
        
3. **📚 Loop pelos 9 ativos restantes**
    
    - Execução manual, um ativo de cada vez, respeitando o protocolo de validação a cada passo.
        
    - Mesmas saídas: `dataset_curado`, `scaler`, `modelo_t+1 / t+3 / t+5`, métricas.
        
4. **🗄️ Consolide um dataset “carteira”**
    
    - Combine as **probabilidades** ou **sinais normalizados** dos 10 modelos em um único DataFrame temporal (`date × 10 ativos`).
        
    - Inclua coluna `cash_available`.
        
5. **🤖 Só então avance para**
    
    - **ML conjunto** (ranking, meta-learner, stacking).
        
    - **RL de alocação** (agente que observa o vetor de sinais + caixa fixo).
        

> _Essa ordem (freezar PETR4 ➜ clonar nos demais ➜ consolidar ➜ ML/RL global) equilibra rapidez de entrega e consistência multi-ativo._

---

