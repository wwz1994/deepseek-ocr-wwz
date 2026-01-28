# 💪 FitLife - Aplicativo de Emagrecimento

Um aplicativo web completo e moderno para auxiliar no processo de emagrecimento saudável.

## 🎯 Funcionalidades

### 📊 Dashboard
- Visualização do progresso de emagrecimento
- Estatísticas em tempo real (peso atual, meta, peso perdido)
- Registro rápido de peso
- Histórico recente de medições
- Dicas motivacionais

### 🧮 Calculadoras
- **Calculadora de IMC**: Índice de Massa Corporal com classificação
- **Calculadora de TMB**: Taxa Metabólica Basal
- **Calculadora de TDEE**: Gasto calórico total diário
- **Calculadora de Déficit Calórico**: Planejamento de calorias para emagrecimento
- **Calculadora de Peso Ideal**: Baseada em múltiplas fórmulas científicas

### 📈 Progresso
- Gráfico interativo de evolução do peso
- Estatísticas detalhadas
- Estimativa de tempo para atingir a meta
- Histórico completo de medições

### 🥗 Planos Alimentares
- Sugestões de refeições para diferentes faixas calóricas
- Dicas nutricionais
- Lista de alimentos recomendados
- Orientações sobre alimentação saudável

## 🚀 Como Usar

### Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o aplicativo:
```bash
python app.py
```

3. Acesse no navegador:
```
http://localhost:5000
```

## 📁 Estrutura do Projeto

```
weight_loss_app/
├── app.py                 # Aplicação Flask principal
├── models.py              # Modelos de cálculo
├── data_manager.py        # Gerenciamento de dados
├── requirements.txt       # Dependências
├── templates/             # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── calculators.html
│   ├── progress.html
│   └── meal_plans.html
├── static/                # Arquivos estáticos
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── data/                  # Dados do usuário (gerado automaticamente)
    ├── user_data.json
    └── weight_history.json
```

## 🎨 Tecnologias Utilizadas

- **Backend**: Python + Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Gráficos**: Chart.js
- **Design**: CSS moderno com gradientes e animações

## 📝 Funcionalidades Técnicas

### Cálculos Implementados

1. **IMC (Índice de Massa Corporal)**
   - Fórmula: peso / (altura²)
   - Classificação automática

2. **TMB (Taxa Metabólica Basal)**
   - Fórmula de Harris-Benedict
   - Diferenciada por sexo

3. **TDEE (Total Daily Energy Expenditure)**
   - TMB × Fator de atividade
   - 5 níveis de atividade física

4. **Déficit Calórico**
   - 3 velocidades de emagrecimento
   - Cálculo de perda semanal estimada

5. **Peso Ideal**
   - Fórmula de Devine
   - Fórmula de Robinson
   - Fórmula de Miller
   - Baseado no IMC ideal

### Armazenamento de Dados

- Dados salvos em JSON
- Histórico completo de pesos
- Perfil do usuário persistente

## ⚠️ Aviso Importante

Este aplicativo é uma ferramenta de auxílio e não substitui o acompanhamento de profissionais de saúde. Sempre consulte um médico e/ou nutricionista antes de iniciar qualquer programa de emagrecimento.

## 🔮 Melhorias Futuras

- [ ] Sistema de login e múltiplos usuários
- [ ] Exportação de dados (PDF, CSV)
- [ ] Integração com dispositivos wearables
- [ ] Registro de exercícios físicos
- [ ] Diário alimentar
- [ ] Notificações e lembretes
- [ ] Modo escuro
- [ ] Aplicativo mobile (PWA)

## 📄 Licença

Este projeto é de código aberto e está disponível para uso pessoal e educacional.

## 👨‍💻 Desenvolvimento

Desenvolvido com ❤️ usando Python e Flask.

---

**Versão**: 1.0.0  
**Data**: 2025
