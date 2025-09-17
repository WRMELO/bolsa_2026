showtime—vou “pensar alto” e organizar a estratégia para casar **previsão de tendências** com a sua **política de preservação** (venda compulsória, compra opcional, meta 8% a.a., piso inaceitável de +3%).

---

# 1) Alcance de dados e por que IBOV-only não basta

Você usou **IBOV por 3 anos** para “achar o caminho”. Funcionou como _spike_, mas limita:

- **Pobreza de regimes**: 3 anos podem não conter bear, crash, euforia e lateralidade suficientes; isso afeta muito D+3/D+5.
    
- **Classe ausente em blocos** (o que já vimos): splits iniciais sem as 3 classes → blocos “skipados”.
    
- **Sinal fraco** em índice agregado: IBOV “suaviza” ruídos dos componentes; o modelo aprende neutralidade com facilidade e sofre para ↑/↓.
    

➡️ Recomendo **ampliar a base**:

- **Treino**: 8–12 anos (se disponível) para **IBOV** e, na sequência, **24 tickers** (multivariado).
    
- **Validação/Teste**: os **últimos 3 anos** continuam sendo o “campo de prova” comparável ao seu baseline atual.
    

Isso reduz “classe ausente” por bloco, melhora robustez de khk_h, e expõe o modelo a mais regimes.

---

# 2) Rótulos e neutralidade: manter 3 classes no **dataset**

Já combinamos: **sem banda neutra extra na decisão**.  
O dataset Gold define 3 classes (↓, 0, ↑) via:

- rt,h=Closet+h−ClosetClosetr_{t,h} = \frac{Close_{t+h}-Close_t}{Close_t}
    
- “Zona de ruído” ∣rt,h∣≤kh⋅σt,h|r_{t,h}| \le k_h \cdot \sigma_{t,h} (com metas de fração neutra).
    

Se você quiser **elevar o viés conservador**, podemos **subir a meta de neutros** (ex.: D+1: 55–65%), **na rotulagem**, não na decisão.

---

# 3) Objetivo de negócio (8% a.a.) e piso (+3%)

Traduza a sua meta de 8% a.a. para **horizontes curtos** (aprox, base 252 pregões/ano):

- **D+1 (1d)**: h1≈(1+0.08)1/252−1≈0,030%h_1 \approx (1{+}0.08)^{1/252} - 1 \approx 0{,}030\%
    
- **D+3 (3d)**: h3≈0,092%h_3 \approx 0{,}092\%
    
- **D+5 (5d)**: h5≈0,153%h_5 \approx 0{,}153\%
    

Use isso como **hurdle mínimo** de expectativa líquida por trade.

O **piso de +3%** (“inaceitável ficar abaixo”) pode ser tratado de duas formas, a escolher:

- **Piso absoluto**: Ft=1,03×capital inicialF_t = 1{,}03 \times \text{capital inicial}. Nunca permitir que Vt<FtV_t < F_t.
    
- **Piso de trajetória** (_mais rígido_): Ft=V0×(1+0,08)t/252F_t = V_0 \times (1{+}0{,}08)^{t/252}. Você “trava” o patrimônio para nunca ficar **abaixo da curva** do dinheiro+8% a.a. (muito conservador).
    

Na prática, recomendo **absoluto de 3%** no começo e, quando o patrimônio superar bem esse nível, migrar para um **CPPI leve** (ver §6).

---

# 4) Separar “vender” de “comprar” (e pesos de erro)

O seu **viés é conservador**: não perder o que já ganhou.

- **Venda é compulsória**: queremos **altíssima sensibilidade** a sinais de queda (evitar FNs de ↓).
    
- **Compra é opcional**: queremos **alta precisão** para ↑ (evitar FPs de ↑).
    

Isso pede **dois limiares** distintos, sobre **probabilidades calibradas** do classificador (3 classes):

### 4.1. Gatilho de **Venda** (compulsório)

Use um agregador “pior caso” dos horizontes curtos:

St↓=max⁡{ pt,1(↓), λ pt,3(↓), μ pt,5(↓)}S^\downarrow_t = \max\{\,p_{t,1}(\downarrow),\ \lambda\, p_{t,3}(\downarrow),\ \mu\, p_{t,5}(\downarrow)\}

- Comece com λ=0,7, μ=0,5\lambda=0{,}7,\ \mu=0{,}5.
    
- Venda se St↓≥θ↓S^\downarrow_t \ge \theta_\downarrow.
    
- **θ↓\theta_\downarrow alto?** → poucas vendas, risco de dar “carona” em quedas.
    
- **θ↓\theta_\downarrow baixo?** → vendas precoces, mas preserva capital (seu viés).
    
- Afinar θ↓\theta_\downarrow para manter **probabilidade de violar o piso** < 1% (ver §6).
    

### 4.2. Filtro de **Compra** (opcional)

Exija **consistência** e **hurdle**:

- Sinal coerente: pt,1(↑)≥θ1, pt,3(↑)≥θ3p_{t,1}(\uparrow) \ge \theta_{1},\ p_{t,3}(\uparrow) \ge \theta_{3} **e** pt,5(↓)<θ5−p_{t,5}(\downarrow) < \theta_{5}^{-}.
    
- **Hurdle esperado**:
    
    E[rt,h]≈rˉt,h_↑⏟retorno cond.⋅pt,h(↑)  −  ∣rˉt,h_↓∣⏟_risco cond.⋅pt,h(↓)  −  custos\mathbb{E}[r_{t,h}] \approx \underbrace{\bar r_{t,h}\_{\uparrow}}_{\text{retorno cond.}} \cdot p_{t,h}(\uparrow) \;-\; \underbrace{|\bar r_{t,h}\_{\downarrow}|}\_{\text{risco cond.}} \cdot p_{t,h}(\downarrow) \;-\; \text{custos}
    
    Exigir E[rt,h]≥hh\mathbb{E}[r_{t,h}] \ge h_h (0,03%/0,09%/0,15% dependendo do horizonte escolhido).
    
- **Caixa**: só comprar se houver caixa (regra do projeto), com **position sizing** em §6.
    

---

# 5) Modelo preditivo: qual usar?

- **XGBoost** ainda é um **baseline excelente** pela robustez/tabular e velocidade.
    
- **CatBoost** costuma entregar **probabilidades mais estáveis**; vale testar lado a lado.
    
- **LogReg multinomial (elastic net)** é um _sanity check_: se empatar com XGB, o limite é **informação**, não o modelo.
    
- **DL tabular (MLP)** só vale se ampliarmos bastante dados e/ou formos **multivariado** (24 ativos juntos, capturando co-movimentos). Com apenas o IBOV ou poucos anos, tende a sobreajustar.
    

Sugestão: **Benchmark triplo** (XGB, CatBoost, LogReg) no IBOV expandido e, em seguida, **multivariado** (24). Escolha pelo **MCC macro por bloco** e **qualidade das probabilidades** (Brier/NLL).

---

# 6) Overlay de risco para garantir o **piso +3%**

Imponha uma camada **determinística** por cima do sinal, para que o portfólio respeite o piso **sempre**:

### 6.1. **CPPI leve** (Constant Proportion Portfolio Insurance)

- Defina o **piso** FtF_t (ex.: 1.03×capital inicial).
    
- Defina a **almofada** Ct=max⁡(Vt−Ft, 0)C_t = \max(V_t - F_t,\, 0).
    
- Exposição ao risco Et=m⋅CtE_t = m \cdot C_t, com **multiplicador** mm pequeno (ex.: 2–4).
    
- Se Vt→FtV_t \to F_t, Ct→0C_t \to 0 ⇒ **você zera risco** e preserva o piso.
    
- Ajuste mm para que o **VaR de 1 dia** a 99% **não atravesse o piso**.
    

### 6.2. **Dimensionamento por volatilidade**

- Para cada compra, dimensione:
    
    w∝Cushionσ^he limite w≤wmax⁡w \propto \frac{\text{Cushion}}{\widehat{\sigma}_{h}} \quad \text{e limite } w \le w_{\max}
- **Stops “estatísticos”**: se \Delta \text{P&L} intradiária ~ >nσ> n \sigma contra a posição **ou** St↓S^\downarrow_t cruzar θ↓ \theta_\downarrow, **desaloca** (venda compulsória).
    

### 6.3. **Kill switch** (violação iminente)

- Se a probabilidade de perfurar FtF_t nas próximas 24–48h (via vol prevista) exceder α\alpha (ex.: 1%), **força caixa**.
    

---

# 7) Avaliação e critérios de aceitação

Métricas **técnicas** (por bloco e horizonte):

- **MCC macro > 0** em todos os blocos.
    
- **Acurácia balanceada > trivial**.
    
- **F1(↑)** e **F1(↓)** > 0.
    

Métricas **de negócio** (com overlay de risco e custos):

- **Nenhuma violação do piso** FtF_t (+3% absoluto, ou o que definirmos).
    
- **Underwater** controlado: drawdown **sempre** acima de +3%.
    
- **Retorno líquido ≥ trajetória de 8% a.a.** nos últimos 12m rolling (ou justificar regime).
    
- **Turnover** e **custo efetivo** dentro de limites.
    

---

# 8) Próximos passos concretos (para o agente executar depois que você validar)

1. **Expandir dados do IBOV** para 8–12 anos (se disponível) → reconstruir Gold (mesmos rótulos, possivelmente ajustando metas de neutro).
    
2. **Re-treinar OptA** com walk-forward “expanding” + embargo e **mínimo por classe** no treino (evita “skip”).
    
3. **Benchmark XGB vs CatBoost vs LogReg** (mesmo split, mesma calibração) → escolher 1.
    
4. **Implementar overlay CPPI leve** + position sizing por vol + kill switch.
    
5. **Backtest de política**: venda compulsória com St↓S^\downarrow_t, compra opcional com hurdle E[r]≥hh\mathbb{E}[r]\ge h_h, custos.
    
6. **Checar critérios**: piso +3% nunca violado; comparação com 8% a.a.; métricas por bloco.
    

---

## TL;DR

- **Dados**: amplie (anos e, depois, 24 ativos).
    
- **Modelo**: mantenha 3 classes no dataset e **decisão por argmax**; teste XGB vs CatBoost vs LogReg.
    
- **Venda**: gatilho compulsório via agregador de p(↓)p(\downarrow) (D+1/D+3/D+5).
    
- **Compra**: opcional, exige coerência de ↑ e **hurdle** ≥ 8% a.a. prorata.
    
- **Risco**: **CPPI leve + sizing por vol + kill switch** para garantir o **piso +3%** em todo o caminho.
    

Se topar essa arquitetura, eu transformo isso em duas TASKs:  
(1) **Rebuild Gold (IBOV ampliado)** + **OptA robusto**;  
(2) **Backtest da política com overlay de risco**.