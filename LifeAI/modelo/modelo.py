import numpy as np
from PIL import Image
import os

# =========================================
# TRADUÇÃO DAS PATOLOGIAS
# =========================================

TRADUCAO_PATOLOGIAS = {
    "Atelectasis": "Atelectasia",
    "Consolidation": "Consolidação",
    "Infiltration": "Infiltrado",
    "Pneumothorax": "Pneumotórax",
    "Edema": "Edema Pulmonar",
    "Emphysema": "Enfisema",
    "Fibrosis": "Fibrose",
    "Effusion": "Derrame Pleural",
    "Pneumonia": "Pneumonia",
    "Pleural_Thickening": "Espessamento Pleural",
    "Cardiomegaly": "Cardiomegalia",
    "Nodule": "Nódulo",
    "Mass": "Massa",
    "Hernia": "Hérnia",
    "Lung Lesion": "Lesão Pulmonar",
    "Fracture": "Fratura",
    "Lung Opacity": "Opacidade Pulmonar",
    "Enlarged Cardiomediastinum": "Alargamento Cardiomediastinal"
}

# =========================================
# ANÁLISE SIMULADA COM PADRÕES INTELIGENTES
# =========================================

def processar_imagem(caminho_arquivo):
    """Processa a imagem e extrai características"""
    try:
        img = Image.open(caminho_arquivo)
        img_array = np.array(img)
        
        # Calcular características básicas da imagem
        if len(img_array.shape) > 2:
            img_gray = np.mean(img_array, axis=2)
        else:
            img_gray = img_array
        
        # Normalizar
        img_gray = img_gray / 255.0
        
        # Calcular densidade (% de pixels escuros)
        densidade = np.mean(img_gray < 0.5)
        
        # Calcular variância (áreas com mais variação = anomalias potenciais)
        variancia = np.var(img_gray)
        
        return {
            'densidade': densidade,
            'variancia': variancia,
            'altura': img_array.shape[0],
            'largura': img_array.shape[1]
        }
    except Exception as e:
        raise Exception(f"Erro ao processar imagem: {str(e)}")


def analisar_exame(caminho_arquivo):
    """
    Simula análise de exame radiológico com padrões inteligentes
    
    Args:
        caminho_arquivo: caminho para a imagem
    
    Returns:
        dict com resultado da análise
    """
    try:
        # Verificar se arquivo existe
        if not os.path.exists(caminho_arquivo):
            return {
                'sucesso': False,
                'erro': 'Arquivo não encontrado'
            }
        
        # Processar imagem
        features = processar_imagem(caminho_arquivo)
        
        # Gerar resultado baseado em análise de features
        densidade = features.get('densidade', 0)
        variancia = features.get('variancia', 0)
        
        # Definir patologias detectadas baseado em características da imagem
        pathologies_detectadas = {}
        
        # Se densidade alta, pode indicar consolidação
        if densidade > 0.35:
            pathologies_detectadas['Consolidação'] = min(0.85, densidade + 0.2)
            pathologies_detectadas['Infiltrado'] = min(0.75, densidade + 0.1)
        
        # Se variância alta, pode indicar fibrose ou opacidade
        if variancia > 0.15:
            pathologies_detectadas['Opacidade Pulmonar'] = min(0.80, variancia * 2)
            pathologies_detectadas['Fibrose'] = min(0.65, variancia * 1.5)
        
        # Probabilidade base de outras patologias
        if densidade > 0.3:
            pathologies_detectadas['Pneumonia'] = min(0.70, 0.5 + densidade * 0.3)
            pathologies_detectadas['Edema Pulmonar'] = min(0.60, 0.4 + densidade * 0.2)
        
        if variancia > 0.10:
            pathologies_detectadas['Nódulo'] = min(0.55, variancia * 1.8)
            pathologies_detectadas['Massa'] = min(0.50, variancia * 1.5)
        
        # Se nada detectado, retornar normal
        if not pathologies_detectadas:
            pathologies_detectadas['Sem achados relevantes'] = 0.15
        
        # Filtrar por threshold (> 40%)
        pathologies_filtradas = {
            nome: score for nome, score in pathologies_detectadas.items()
            if score > 0.40
        }
        
        # Se vazio, incluir algo
        if not pathologies_filtradas:
            pathologies_filtradas = {'Achados inconclusivos': 0.42}
        
        # Ordenar por score
        pathologies_ordenadas = sorted(
            pathologies_filtradas.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Determinar prioridade e risco
        if pathologies_ordenadas:
            max_score = pathologies_ordenadas[0][1]
            
            if max_score > 0.75:
                prioridade = "CRÍTICO"
                risco = 85
                recomendacao = "Encaminhamento imediato para especialista"
            elif max_score > 0.60:
                prioridade = "URGENTE"
                risco = 70
                recomendacao = "Avaliação urgente recomendada"
            elif max_score > 0.50:
                prioridade = "ATENÇÃO"
                risco = 50
                recomendacao = "Acompanhamento recomendado"
            else:
                prioridade = "NORMAL"
                risco = 25
                recomendacao = "Sem achados relevantes"
            
            gravidade = "Grave" if max_score > 0.70 else "Moderada" if max_score > 0.50 else "Leve"
        else:
            prioridade = "NORMAL"
            risco = 15
            gravidade = "Leve"
            recomendacao = "Sem achados relevantes"
        
        # Tempos estimados
        tempo_estimado_map = {
            "CRÍTICO": "5-10 minutos",
            "URGENTE": "15-30 minutos",
            "ATENÇÃO": "1-2 horas",
            "NORMAL": "Agendamento normal"
        }
        
        resultado = {
            'sucesso': True,
            'pathologias': [
                {
                    'nome': nome,
                    'confianca': float(score),
                    'confianca_percentual': f"{float(score) * 100:.1f}%",
                    'gravidade': "Grave" if score > 0.70 else "Moderada" if score > 0.50 else "Leve"
                }
                for nome, score in pathologies_ordenadas
            ],
            'gravidade': gravidade,
            'percentual_risco': risco,
            'prioridade': prioridade,
            'recomendacao': recomendacao,
            'tempo_estimado': tempo_estimado_map.get(prioridade, "Desconhecido"),
            'total_patologias_detectadas': len(pathologies_ordenadas)
        }
        
        return resultado
    
    except Exception as e:
        print(f"Erro na análise: {str(e)}")
        return {
            'sucesso': False,
            'erro': str(e)
        }


# =========================================
# TESTE (se executado diretamente)
# =========================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        caminho = sys.argv[1]
        print(f"\nAnalisando: {caminho}\n")
        resultado = analisar_exame(caminho)
        
        if resultado['sucesso']:
            print("=" * 60)
            print("RESULTADO DA ANÁLISE")
            print("=" * 60)
            print(f"\nGravidade Geral: {resultado['gravidade']}")
            print(f"Prioridade: {resultado['prioridade']}")
            print(f"Percentual de Risco: {resultado['percentual_risco']}%")
            print(f"Tempo Estimado: {resultado['tempo_estimado']}")
            print(f"\nRecomendação: {resultado['recomendacao']}")
            
            if resultado['pathologias']:
                print(f"\nPatologias Detectadas ({resultado['total_patologias_detectadas']}):")
                for p in resultado['pathologias']:
                    print(f"  • {p['nome']}: {p['confianca_percentual']} ({p['gravidade']})")
            else:
                print("\nNenhuma patologia relevante detectada.")
        else:
            print(f"Erro na análise: {resultado['erro']}")
    else:
        print("Use: python modelo.py <caminho_imagem>")