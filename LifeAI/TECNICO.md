# 🔬 Documentação Técnica - LifeAI

## 📚 Índice
1. [Arquitetura](#arquitetura)
2. [Modelo de IA](#modelo-de-ia)
3. [Fluxo de Análise](#fluxo-de-análise)
4. [API Endpoints](#api-endpoints)
5. [Estrutura de Dados](#estrutura-de-dados)
6. [Desenvolvimento](#desenvolvimento)

---

## 🏗️ Arquitetura

### Stack Tecnológico
- **Backend:** Flask 2.3.3 (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **IA/ML:** PyTorch + TorchXRayVision
- **Processamento:** Scikit-Image, NumPy

### Componentes Principais

```
┌─────────────────────────────────────────────────┐
│                  LIFEAI                         │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐      ┌──────────────┐       │
│  │  Frontend    │◄────►│   Flask API  │       │
│  │  (HTML/JS)   │      │              │       │
│  └──────────────┘      └──────────────┘       │
│                              ▲                 │
│                              │                 │
│                        ┌─────▼─────┐          │
│                        │   Modelo   │          │
│                        │    de IA   │          │
│                        │            │          │
│                        │ DenseNet121│          │
│                        └────────────┘          │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🤖 Modelo de IA

### Modelo Utilizado: DenseNet121

**Características:**
- Pré-treinado no dataset NIH ChestX-ray14
- 18 patologias detectáveis
- Input: 224x224 pixels em escala de cinza
- Output: Score de confiança (0-1) para cada patologia

### Patologias Detectadas

| # | Patologia (EN) | Patologia (PT) | Gravidade |
|---|---|---|---|
| 1 | Atelectasis | Atelectasia | Moderada |
| 2 | Consolidation | Consolidação | Urgente |
| 3 | Infiltration | Infiltrado | Urgente |
| 4 | Pneumothorax | Pneumotórax | Crítica |
| 5 | Edema | Edema Pulmonar | Urgente |
| 6 | Emphysema | Enfisema | Moderada |
| 7 | Fibrosis | Fibrose | Atenção |
| 8 | Effusion | Derrame Pleural | Crítica |
| 9 | Pneumonia | Pneumonia | Crítica |
| 10 | Pleural Thickening | Espessamento Pleural | Atenção |
| 11 | Cardiomegaly | Cardiomegalia | Crítica |
| 12 | Nodule | Nódulo | Atenção |
| 13 | Mass | Massa | Urgente |
| 14 | Hernia | Hérnia | Atenção |
| 15 | Lung Lesion | Lesão Pulmonar | Moderada |
| 16 | Fracture | Fratura | Urgente |
| 17 | Lung Opacity | Opacidade Pulmonar | Urgente |
| 18 | Enlarged Cardiomediastinum | Alargamento Cardiomediastinal | Crítica |

### Algoritmo de Classificação de Prioridade

```python
def determinar_prioridade(pathologies_scores):
    if (patologia_critica AND score > 0.60):
        return "CRÍTICO" (Risco 85%)
    elif (patologia_urgente AND score > 0.50):
        return "URGENTE" (Risco 65%)
    elif (max_score > 0.50):
        return "ATENÇÃO" (Risco 45%)
    else:
        return "NORMAL" (Risco 15%)
```

---

## 📊 Fluxo de Análise

### Passo a Passo

```
1. UPLOAD DA IMAGEM
   │
   ├─ Validação de tipo (PNG, JPG, JPEG, GIF, DICOM, BMP)
   ├─ Validação de tamanho (máx. 50MB)
   └─ Salvamento em /uploads/{timestamp}_{filename}
   
2. PRÉ-PROCESSAMENTO
   │
   ├─ Leitura da imagem (skimage.io)
   ├─ Conversão para escala de cinza (se RGB)
   ├─ Normalização (0-1)
   ├─ Redimensionamento (224x224)
   └─ Conversão para tensor PyTorch
   
3. ANÁLISE COM IA
   │
   ├─ Carregamento do modelo (cache)
   ├─ Forward pass (predição)
   └─ Obtenção de scores (18 valores)
   
4. PÓS-PROCESSAMENTO
   │
   ├─ Filtro de confiança (score > 0.40)
   ├─ Tradução de nomes (EN → PT)
   ├─ Classificação de gravidade
   ├─ Determinação de prioridade
   └─ Geração de recomendações
   
5. ARMAZENAMENTO
   │
   └─ Salvamento em exames_armazenados[]
   
6. RESPOSTA AO CLIENTE
   │
   └─ JSON com resultado da análise
```

### Tempo de Processamento

- **Carregamento do modelo:** 5-10s (primeira execução)
- **Processamento de imagem:** 0.5-1s
- **Análise com IA:** 2-5s
- **Total:** 2.5-6s (com cache do modelo)

---

## 🔌 API Endpoints

### 1. POST `/novo-exame`

**Descrição:** Submeter um novo exame para análise

**Método:** POST (formulário multipart)

**Parâmetros:**
```
arquivo_exame          [File]   - Imagem radiológica (obrigatório)
nome_paciente          [String] - Nome completo (obrigatório)
cpf_paciente           [String] - CPF (obrigatório)
data_nascimento        [Date]   - Data (obrigatório)
sexo                   [Select] - masculino/feminino/outro (obrigatório)
hospital               [String] - Hospital (obrigatório)
sintomas               [Text]   - Sintomas (opcional)
observacoes            [Text]   - Observações (opcional)
```

**Resposta (200 OK):**
```html
<!-- Página HTML renderizada com resultado -->
```

**Erros:**
```
400 - Arquivo não selecionado
400 - Tipo de arquivo não permitido
413 - Arquivo muito grande
500 - Erro ao processar análise
```

### 2. POST `/api/analisar-exame`

**Descrição:** API REST para análise de exame (apenas a imagem)

**Método:** POST (multipart/form-data)

**Parâmetros:**
```
arquivo_exame [File] - Imagem radiológica
```

**Resposta (200 OK):**
```json
{
  "sucesso": true,
  "gravidade": "Moderada",
  "percentual_risco": 65,
  "prioridade": "URGENTE",
  "recomendacao": "Avaliação urgente recomendada",
  "tempo_estimado": "15-30 minutos",
  "pathologias": [
    {
      "nome": "Consolidação",
      "confianca": 0.72,
      "confianca_percentual": "72.0%",
      "gravidade": "Moderada"
    },
    {
      "nome": "Infiltrado",
      "confianca": 0.65,
      "confianca_percentual": "65.0%",
      "gravidade": "Moderada"
    }
  ],
  "total_patologias_detectadas": 2
}
```

**Erros:**
```json
{
  "sucesso": false,
  "erro": "Nenhum arquivo enviado"
}
```

### 3. GET `/api/dados-dashboard`

**Descrição:** Obter dados em tempo real do dashboard

**Método:** GET

**Resposta (200 OK):**
```json
{
  "total_exames": 15,
  "urgentes": 3,
  "atenção": 6,
  "normais": 4,
  "criticos": 2
}
```

---

## 📦 Estrutura de Dados

### Exame Armazenado

```python
{
  'id': int,                           # ID único
  'nome_paciente': str,                # Nome completo
  'cpf': str,                          # CPF
  'data_nascimento': str,              # YYYY-MM-DD
  'sexo': str,                         # masculino/feminino/outro
  'hospital': str,                     # Nome do hospital
  'sintomas': str,                     # Texto descritivo
  'observacoes': str,                  # Texto descritivo
  'data_registro': str,                # DD/MM/YYYY HH:MM
  'resultado': {                       # Resultado da IA
    'sucesso': bool,
    'gravidade': str,                  # Leve/Moderada/Grave
    'percentual_risco': int,           # 0-100
    'prioridade': str,                 # CRÍTICO/URGENTE/ATENÇÃO/NORMAL
    'recomendacao': str,               # Recomendação médica
    'tempo_estimado': str,             # Tempo estimado
    'pathologias': [                   # Lista de patologias
      {
        'nome': str,
        'confianca': float,            # 0-1
        'confianca_percentual': str,   # "X.X%"
        'gravidade': str               # Leve/Moderada/Grave
      }
    ],
    'total_patologias_detectadas': int
  }
}
```

---

## 🛠️ Desenvolvimento

### Estrutura de Arquivos

```
LifeAI/
├── app.py                      # Aplicação principal
├── config.py                   # Configurações
├── requirements.txt            # Dependências
├── modelo/
│   └── modelo.py              # Modelo de IA
├── static/
│   ├── css/
│   │   ├── estilo.css
│   │   ├── estilo-dashboard.css
│   │   ├── estilo-paginas.css
│   │   └── estilo-utilitarios.css
│   ├── js/
│   │   └── aplicativo.js
│   └── img/
├── templates/
│   ├── base.html
│   ├── novo_exame.html
│   ├── exames.html
│   ├── fila_prioridade.html
│   ├── painel_controle.html
│   ├── relatorios.html
│   ├── perfil.html
│   ├── configuracoes.html
│   ├── login.html
│   ├── cadastro.html
│   ├── 404.html
│   ├── 500.html
│   └── partials/
│       ├── barra_lateral.html
│       ├── barra_superior.html
│       └── rodape.html
├── uploads/                    # Pasta de uploads (criada dinamicamente)
└── README.md
```

### Como Adicionar Nova Patologia

1. **Atualizar `modelo.py`:**
```python
TRADUCAO_PATOLOGIAS = {
    # ... patologias existentes ...
    "NovaPatologia": "Nova Patologia PT",
}

# Atualizar lógica de prioridade em determinar_prioridade()
patologias_criticas = [..., "NovaPatologia"]
```

2. **Atualizar documentação** - Este arquivo

### Como Integrar Banco de Dados

1. **Instalar SQLAlchemy:**
```bash
pip install flask-sqlalchemy
```

2. **Criar modelo:**
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Exame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_paciente = db.Column(db.String(255), required=True)
    # ... outros campos ...
    resultado = db.Column(db.JSON)
```

3. **Substituir listas em memória** por queries ao DB

### Como Fazer Deploy em Produção

1. **Configurar variáveis de ambiente:**
```bash
export FLASK_ENV=production
export SECRET_KEY='sua_chave_muito_segura_aqui'
```

2. **Usar servidor de produção (Gunicorn):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **Configurar reverse proxy (Nginx):**
```nginx
server {
    listen 80;
    server_name seu_dominio.com;
    
    location / {
        proxy_pass http://localhost:5000;
    }
}
```

---

## 📝 Logs

Logs são salvos em: `logs/lifeai.log`

Formato:
```
[TIMESTAMP] [LEVEL] Message
2024-01-15 14:30:45 INFO Modelo carregado com sucesso
2024-01-15 14:31:22 INFO Analisando arquivo: xyz123.jpg
2024-01-15 14:31:28 INFO Análise concluída - Prioridade: URGENTE
```

---

## 🔐 Segurança

### Implementado
- ✅ Validação de tipo de arquivo
- ✅ Limite de tamanho (50MB)
- ✅ Sessão HTTP-only
- ✅ CSRF protection (quando em produção com HTTPS)

### TODO
- ❌ Autenticação com banco de dados
- ❌ Rate limiting
- ❌ Criptografia de dados sensíveis
- ❌ Backup automático de exames

---

## 🐛 Troubleshooting

### Erro: "CUDA out of memory"
- GPU sem memória suficiente
- **Solução:** Use CPU (automático se CUDA falhar) ou reduza batch size

### Erro: "Modelo não carrega"
- Dependências não instaladas corretamente
- **Solução:** `pip install --force-reinstall torchxrayvision`

### Imagens muito grandes/lentas
- Pré-processe as imagens antes de enviar
- **Solução:** Redimensione para < 2MB

---

## 📚 Referências

- [TorchXRayVision](https://github.com/mlmed/torchxrayvision)
- [PyTorch](https://pytorch.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [NIH ChestX-ray14 Dataset](https://www.nih.gov/news-events/news-releases/nih-clinical-center-provides-one-largest-publicly-available-chest-x-ray-datasets-scientific-community)

---

**Última atualização:** Janeiro 2024
**Versão:** 1.0.0
