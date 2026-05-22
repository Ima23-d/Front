@echo off
REM Script de inicialização do LifeAI para Windows

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         LIFEAI - SISTEMA DE ANÁLISE RADIOLÓGICA           ║
echo ║              Inicializador para Windows                    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erro: Python não encontrado!
    echo.
    echo Por favor instale Python 3.8+ em:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Verificar se venv existe
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Erro ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo ✅ Ambiente virtual criado
    echo.
)

REM Ativar venv
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Erro ao ativar ambiente virtual
    pause
    exit /b 1
)
echo ✅ Ambiente virtual ativo
echo.

REM Criar pasta de uploads
if not exist "uploads" (
    echo 📁 Criando pasta de uploads...
    mkdir uploads
    echo ✅ Pasta de uploads criada
    echo.
)

REM Instalar/atualizar dependências
echo 📥 Instalando/Atualizando dependências...
echo (Isso pode levar alguns minutos...)
echo.
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo ❌ Erro ao instalar dependências
    echo.
    echo Tente executar manualmente:
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ Dependências instaladas com sucesso
echo.

REM Iniciar a aplicação
echo 🚀 Iniciando LifeAI...
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║  Acesse a aplicação em: http://127.0.0.1:5000           ║
echo ║                                                            ║
echo ║  Credenciais de teste:                                    ║
echo ║  Email: usuario@hospital.com                             ║
echo ║  Senha: qualquer valor                                   ║
echo ║                                                            ║
echo ║  Pressione Ctrl+C para encerrar                          ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

python app.py

pause
