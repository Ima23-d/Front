#!/bin/bash

# Script de inicialização do LifeAI para Linux/macOS

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║         LIFEAI - SISTEMA DE ANÁLISE RADIOLÓGICA           ║"
echo "║           Inicializador para Linux/macOS                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Erro: Python não encontrado!"
    echo ""
    echo "Por favor instale Python 3.8+ em:"
    echo "https://www.python.org/downloads/"
    echo ""
    exit 1
fi

echo "✅ Python encontrado"
echo ""

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao criar ambiente virtual"
        exit 1
    fi
    echo "✅ Ambiente virtual criado"
    echo ""
fi

# Ativar venv
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Erro ao ativar ambiente virtual"
    exit 1
fi
echo "✅ Ambiente virtual ativo"
echo ""

# Criar pasta de uploads
if [ ! -d "uploads" ]; then
    echo "📁 Criando pasta de uploads..."
    mkdir uploads
    echo "✅ Pasta de uploads criada"
    echo ""
fi

# Instalar/atualizar dependências
echo "📥 Instalando/Atualizando dependências..."
echo "(Isso pode levar alguns minutos...)"
echo ""
pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    echo ""
    echo "Tente executar manualmente:"
    echo "  pip install -r requirements.txt"
    exit 1
fi

echo "✅ Dependências instaladas com sucesso"
echo ""

# Iniciar a aplicação
echo "🚀 Iniciando LifeAI..."
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║  Acesse a aplicação em: http://127.0.0.1:5000           ║"
echo "║                                                            ║"
echo "║  Credenciais de teste:                                    ║"
echo "║  Email: usuario@hospital.com                             ║"
echo "║  Senha: qualquer valor                                   ║"
echo "║                                                            ║"
echo "║  Pressione Ctrl+C para encerrar                          ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

python3 app.py
