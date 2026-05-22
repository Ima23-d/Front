# ==========================================
# CONFIGURAÇÕES DA APLICAÇÃO LIFEAI
# ==========================================

import os
from datetime import timedelta

# Caminho base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================
# CLASSES DE CONFIGURAÇÃO
# ==========================================

class Config:
    """Configuração base"""
    # Gerais
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'sua_chave_secreta_aqui_mudar_em_producao'
    
    # Upload de arquivos
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'dcm', 'bmp'}
    
    # Sessão
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # IA - CONFIGURAÇÕES DO MODELO
    IA_MODEL = 'densenet121-res224-nih'
    IA_CONFIDENCE_THRESHOLD = 0.40
    IA_ANALYSIS_TIMEOUT = 300
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = os.path.join(BASE_DIR, 'logs', 'lifeai.log')
    
    # API
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True


class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mudar-em-producao')


class TestingConfig(Config):
    """Configuração de testes"""
    DEBUG = True
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
