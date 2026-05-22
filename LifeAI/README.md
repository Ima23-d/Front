# 🏥 LifeAI - Sistema de Análise de Radiografia com IA

Plataforma web para análise de imagens radiológicas usando inteligência artificial.

## 📋 Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- 4GB RAM mínimo (recomendado 8GB)
- GPU NVIDIA (opcional, para análise mais rápida)

## 🚀 Instalação

### 1. Clonar/Extrair o Projeto
```bash
cd d:\Arthur\Front-main\Front-main\LifeAI
```

### 2. Criar Ambiente Virtual (Recomendado)
```bash
python -m venv venv
```

**Ativar ambiente virtual:**
- **Windows:**
```bash
venv\Scripts\activate
```

- **Linux/macOS:**
```bash
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

Isso pode levar alguns minutos na primeira instalação devido ao tamanho das bibliotecas de IA.

### 4. Criar Pasta de Uploads
```bash
mkdir uploads
```

## ▶️ Executar a Aplicação

```bash
python app.py
```

A aplicação estará disponível em: **http://127.0.0.1:5000**

## 📁 Estrutura do Projeto

```
LifeAI/
├── app.py                 # Aplicação principal Flask
├── modelo/
│   └── modelo.py         # Modelo de IA para análise de radiografia
├── static/
│   ├── css/              # Arquivos de estilo
│   ├── js/               # JavaScript
│   └── img/              # Imagens
├── templates/            # Templates HTML
├── uploads/              # Pasta de uploads (criada automaticamente)
└── requirements.txt      # Dependências Python
```

## 🔐 Credenciais de Teste

**Email:** usuario@hospital.com  
**Senha:** qualquer valor (sem validação no modo teste)

## 🎯 Funcionalidades

- ✅ Login e autenticação
- ✅ Upload de imagens radiológicas
- ✅ Análise automática com IA
- ✅ Detecção de patologias
- ✅ Classificação por prioridade (CRÍTICO, URGENTE, ATENÇÃO, NORMAL)
- ✅ Fila de prioridade hospitalar
- ✅ Histórico de exames
- ✅ Relatórios e estatísticas

## 🤖 Modelo de IA

O sistema utiliza:
- **DenseNet121** pré-treinado no dataset NIH ChestX-ray14
- Detecção de 18 patologias diferentes
- Score de confiança para cada descoberta
- Análise em tempo real

## 📊 Patologias Detectadas

O modelo pode detectar:
- Pneumonia
- Pneumotórax
- Consolidação
- Edema Pulmonar
- Cardiomegalia
- Derrame Pleural
- Opacidade Pulmonar
- Infiltrado
- E mais 10 outras patologias...

## 🔧 Troubleshooting

### Erro: "Modelo não encontrado"
```bash
# Reinstale as dependências
pip install --force-reinstall torchxrayvision
```

### Erro: "Arquivo não permitido"
Formatos aceitos: PNG, JPG, JPEG, GIF, DICOM, BMP (máx. 50MB)

### Erro: "Memória insuficiente"
Reduza o tamanho da imagem ou aumente a RAM disponível

## 📝 Notas Importantes

⚠️ **Este é um sistema de auxílio diagnóstico**
- Sempre validar resultados com profissional médico qualificado
- A IA não substitui diagnóstico médico
- Use para triagem e priorização apenas

## 🔄 Atualizações

Para atualizar dependências:
```bash
pip install -r requirements.txt --upgrade
```

## 📞 Suporte

Para problemas ou sugestões, consulte a documentação do projeto.

---

**Desenvolvido com ❤️ para auxílio diagnóstico médico**
