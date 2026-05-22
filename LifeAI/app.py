from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime
import json
import os
from werkzeug.utils import secure_filename
import sys

# Carregar configurações
from config import config

# Adicionar pasta modelo ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modelo'))
from modelo import analisar_exame

# Inicializar Flask
app = Flask(__name__)

# Aplicar configurações
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# ==========================================
# CONFIGURAÇÃO DE UPLOAD
# ==========================================

# Usar valores do config
UPLOAD_FOLDER = app.config.get('UPLOAD_FOLDER', os.path.join(os.path.dirname(__file__), 'uploads'))
ALLOWED_EXTENSIONS = app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'dcm', 'bmp'})
MAX_CONTENT_LENGTH = app.config.get('MAX_CONTENT_LENGTH', 50 * 1024 * 1024)

# Criar pasta se não existir
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ==========================================
# DADOS DE EXEMPLO (Substituir por banco de dados real)
# ==========================================

usuarios_autenticados = {}
exames_armazenados = []
lista_fila_prioridade = []

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def arquivo_permitido(filename):
    """Verifica se arquivo é permitido"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==========================================
# ROTAS DE AUTENTICAÇÃO
# ==========================================

@app.route('/')
def indice():
    """Página inicial - redireciona para login se não autenticado"""
    if 'usuario_id' in session:
        return redirect(url_for('painel_controle'))
    return redirect(url_for('pagina_login'))


@app.route('/login', methods=['GET', 'POST'])
def pagina_login():
    """Página de login"""
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Validação simples (substituir por banco de dados real)
        if email and senha:
            session['usuario_id'] = email
            session['nome_usuario'] = 'Dr. João Silva'
            session['crm'] = '123456/SP'
            session['hospital'] = 'Hospital Clínico Central'
            return redirect(url_for('painel_controle'))
        
        return render_template('login.html', erro='Email ou senha inválidos')
    
    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def pagina_cadastro():
    """Página de cadastro"""
    if request.method == 'POST':
        nome_completo = request.form.get('nome_completo')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        crm = request.form.get('crm')
        hospital = request.form.get('hospital')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        # Validação
        if not all([nome_completo, email, cpf, crm, hospital, senha, confirmar_senha]):
            return render_template('cadastro.html', erro='Preencha todos os campos')
        
        if senha != confirmar_senha:
            return render_template('cadastro.html', erro='As senhas não coincidem')
        
        # Registrar usuário (substituir por banco de dados real)
        usuarios_autenticados[email] = {
            'nome': nome_completo,
            'cpf': cpf,
            'crm': crm,
            'hospital': hospital,
            'senha': senha
        }
        
        session['usuario_id'] = email
        session['nome_usuario'] = nome_completo
        session['crm'] = crm
        session['hospital'] = hospital
        
        return redirect(url_for('painel_controle'))
    
    return render_template('cadastro.html')


@app.route('/sair')
def sair():
    """Fazer logout"""
    session.clear()
    return redirect(url_for('pagina_login'))


# ==========================================
# ROTAS PRINCIPAIS
# ==========================================

@app.route('/painel-controle')
def painel_controle():
    """Dashboard principal"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    # Calcular dados em tempo real
    urgentes = sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') == 'URGENTE')
    criticos = sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') == 'CRÍTICO')
    atencao = sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') == 'ATENÇÃO')
    normais = sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') == 'NORMAL')
    
    contexto = {
        'total_exames': len(exames_armazenados),
        'urgentes': urgentes,
        'criticos': criticos,
        'atenção': atencao,
        'normais': normais,
        'ia_ativa': 1,
        'pacientes_fila': len(lista_fila_prioridade),
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'crm': session.get('crm'),
    }
    
    return render_template('painel_controle.html', **contexto)


@app.route('/novo-exame', methods=['GET', 'POST'])
def novo_exame():
    """Página para upload de novo exame"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    if request.method == 'POST':
        # Processar upload de exame
        nome_paciente = request.form.get('nome_paciente')
        cpf_paciente = request.form.get('cpf_paciente')
        data_nascimento = request.form.get('data_nascimento')
        sexo = request.form.get('sexo')
        hospital = request.form.get('hospital')
        sintomas = request.form.get('sintomas')
        observacoes = request.form.get('observacoes')
        
        # Processar arquivo de imagem
        arquivo_resultado = request.files.get('arquivo_exame')
        resultado_analise = None
        
        if arquivo_resultado and arquivo_permitido(arquivo_resultado.filename):
            try:
                # Salvar arquivo
                filename = secure_filename(arquivo_resultado.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                arquivo_resultado.save(caminho_arquivo)
                
                # Analisar com IA
                resultado_analise = analisar_exame(caminho_arquivo)
                
                if not resultado_analise.get('sucesso'):
                    resultado_analise = None
                    
            except Exception as e:
                print(f"Erro ao processar arquivo: {str(e)}")
                resultado_analise = None
        
        # Se análise falhar, usar valores padrão
        if not resultado_analise or not resultado_analise.get('sucesso'):
            resultado_analise = {
                'gravidade': 'Desconhecida',
                'percentual_risco': 0,
                'prioridade': 'NORMAL',
                'recomendacao': 'Erro na análise - contate o administrador',
                'tempo_estimado': 'Indisponível',
                'pathologias': [],
                'total_patologias_detectadas': 0,
                'sucesso': False
            }
        
        novo_registro = {
            'id': len(exames_armazenados) + 1,
            'nome_paciente': nome_paciente,
            'cpf': cpf_paciente,
            'data_nascimento': data_nascimento,
            'sexo': sexo,
            'hospital': hospital,
            'sintomas': sintomas,
            'observacoes': observacoes,
            'data_registro': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'resultado': resultado_analise
        }
        
        exames_armazenados.append(novo_registro)
        lista_fila_prioridade.append(novo_registro)
        
        return render_template('novo_exame.html', 
                             resultado_analise=resultado_analise,
                             dados_paciente=novo_registro,
                             usuario=session.get('nome_usuario'))
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
    }
    
    return render_template('novo_exame.html', **contexto)


@app.route('/exames')
def lista_exames():
    """Lista de todos os exames realizados"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'exames': exames_armazenados,
        'total_exames': len(exames_armazenados),
    }
    
    return render_template('exames.html', **contexto)


@app.route('/exames/<int:id_exame>')
def detalhes_exame(id_exame):
    """Página de detalhes de um exame específico"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    exame = next((e for e in exames_armazenados if e['id'] == id_exame), None)
    
    if not exame:
        return redirect(url_for('lista_exames'))
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'exame': exame,
    }
    
    return render_template('detalhes_exame.html', **contexto)


@app.route('/fila-prioridade')
def fila_prioridade():
    """Página da fila de prioridade hospitalar"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    # Ordenar exames por prioridade
    prioridades = {'CRÍTICO': 0, 'URGENTE': 1, 'ATENÇÃO': 2, 'NORMAL': 3}
    exames_ordenados = sorted(exames_armazenados, 
                              key=lambda x: prioridades.get(x['resultado'].get('prioridade', 'NORMAL'), 4))
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'exames_fila': exames_ordenados,
        'total_fila': len(exames_ordenados),
    }
    
    return render_template('fila_prioridade.html', **contexto)


@app.route('/relatorios')
def pagina_relatorios():
    """Página de relatórios e analytics"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    # Calcular dados reais
    total_exames = len(exames_armazenados)
    casos_graves = sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') in ['CRÍTICO', 'URGENTE'])
    
    # Calcular eficiência (percentual de análises bem-sucedidas)
    analises_sucesso = sum(1 for e in exames_armazenados if e['resultado'].get('sucesso', True))
    eficiencia = (analises_sucesso / total_exames * 100) if total_exames > 0 else 0
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'total_exames': total_exames,
        'total_pacientes': total_exames,
        'casos_graves': casos_graves,
        'tempo_medio_atendimento': '12 minutos',
        'eficiencia_ia': f'{eficiencia:.1f}%',
    }
    
    return render_template('relatorios.html', **contexto)


@app.route('/configuracoes')
def pagina_configuracoes():
    """Página de configurações"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'crm': session.get('crm'),
    }
    
    return render_template('configuracoes.html', **contexto)


@app.route('/perfil')
def pagina_perfil():
    """Página de perfil do usuário"""
    if 'usuario_id' not in session:
        return redirect(url_for('pagina_login'))
    
    contexto = {
        'usuario': session.get('nome_usuario'),
        'hospital': session.get('hospital'),
        'crm': session.get('crm'),
        'email': session.get('usuario_id'),
        'total_exames_realizados': len(exames_armazenados),
    }
    
    return render_template('perfil.html', **contexto)


# ==========================================
# ROTAS API (AJAX)
# ==========================================

@app.route('/api/analisar-exame', methods=['POST'])
def api_analisar_exame():
    """API para análise de exame com IA via upload"""
    try:
        if 'arquivo_exame' not in request.files:
            return jsonify({
                'sucesso': False,
                'erro': 'Nenhum arquivo enviado'
            }), 400
        
        arquivo = request.files['arquivo_exame']
        
        if arquivo.filename == '':
            return jsonify({
                'sucesso': False,
                'erro': 'Arquivo não selecionado'
            }), 400
        
        if not arquivo_permitido(arquivo.filename):
            return jsonify({
                'sucesso': False,
                'erro': 'Tipo de arquivo não permitido. Use: PNG, JPG, JPEG, GIF, DCM, BMP'
            }), 400
        
        # Salvar arquivo temporário
        filename = secure_filename(arquivo.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        arquivo.save(caminho_arquivo)
        
        # Analisar com IA
        resultado = analisar_exame(caminho_arquivo)
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': f'Erro ao processar análise: {str(e)}'
        }), 500


@app.route('/api/dados-dashboard')
def api_dados_dashboard():
    """API para dados do dashboard em tempo real"""
    dados = {
        'total_exames': len(exames_armazenados),
        'urgentes': sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') == 'URGENTE'),
        'atenção': sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') == 'ATENÇÃO'),
        'normais': sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') == 'NORMAL'),
        'criticos': sum(1 for e in exames_armazenados if e['resultado'].get('prioridade') == 'CRÍTICO'),
    }
    return jsonify(dados)


# ==========================================
# TRATAMENTO DE ERROS
# ==========================================

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    """Página 404"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def erro_interno(erro):
    """Página 500"""
    return render_template('500.html'), 500


# ==========================================
# INICIAR APLICAÇÃO
# ==========================================

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
