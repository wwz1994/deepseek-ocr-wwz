"""
Modelos de cálculo para o aplicativo de emagrecimento
"""
from datetime import datetime
from typing import Dict, List, Tuple


class HealthCalculator:
    """Calculadora de métricas de saúde e emagrecimento"""
    
    @staticmethod
    def calculate_imc(peso: float, altura: float) -> Tuple[float, str, str]:
        """
        Calcula o IMC (Índice de Massa Corporal)
        
        Args:
            peso: Peso em kg
            altura: Altura em metros
            
        Returns:
            Tupla com (IMC, classificação, descrição)
        """
        imc = peso / (altura ** 2)
        
        if imc < 18.5:
            classificacao = "Abaixo do peso"
            descricao = "Você está abaixo do peso ideal. Consulte um nutricionista."
        elif 18.5 <= imc < 25:
            classificacao = "Peso normal"
            descricao = "Parabéns! Você está no peso ideal."
        elif 25 <= imc < 30:
            classificacao = "Sobrepeso"
            descricao = "Você está com sobrepeso. Considere uma dieta balanceada."
        elif 30 <= imc < 35:
            classificacao = "Obesidade Grau I"
            descricao = "Obesidade leve. Procure orientação profissional."
        elif 35 <= imc < 40:
            classificacao = "Obesidade Grau II"
            descricao = "Obesidade moderada. Consulte um médico."
        else:
            classificacao = "Obesidade Grau III"
            descricao = "Obesidade mórbida. Procure ajuda médica urgente."
            
        return round(imc, 2), classificacao, descricao
    
    @staticmethod
    def calculate_tmb(peso: float, altura: float, idade: int, sexo: str) -> float:
        """
        Calcula a TMB (Taxa Metabólica Basal) usando a fórmula de Harris-Benedict
        
        Args:
            peso: Peso em kg
            altura: Altura em cm
            idade: Idade em anos
            sexo: 'M' para masculino, 'F' para feminino
            
        Returns:
            TMB em calorias/dia
        """
        if sexo.upper() == 'M':
            tmb = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * idade)
        else:
            tmb = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * idade)
            
        return round(tmb, 2)
    
    @staticmethod
    def calculate_tdee(tmb: float, nivel_atividade: str) -> float:
        """
        Calcula o TDEE (Total Daily Energy Expenditure)
        
        Args:
            tmb: Taxa Metabólica Basal
            nivel_atividade: Nível de atividade física
            
        Returns:
            TDEE em calorias/dia
        """
        fatores = {
            'sedentario': 1.2,
            'leve': 1.375,
            'moderado': 1.55,
            'intenso': 1.725,
            'muito_intenso': 1.9
        }
        
        fator = fatores.get(nivel_atividade, 1.2)
        return round(tmb * fator, 2)
    
    @staticmethod
    def calculate_deficit(tdee: float, objetivo: str) -> Dict[str, float]:
        """
        Calcula o déficit calórico necessário
        
        Args:
            tdee: Total Daily Energy Expenditure
            objetivo: 'lento', 'moderado', 'rapido'
            
        Returns:
            Dicionário com calorias diárias e déficit
        """
        deficits = {
            'lento': 0.10,      # 10% de déficit (0.25-0.5kg/semana)
            'moderado': 0.20,   # 20% de déficit (0.5-0.75kg/semana)
            'rapido': 0.25      # 25% de déficit (0.75-1kg/semana)
        }
        
        deficit_percentual = deficits.get(objetivo, 0.20)
        deficit_calorias = tdee * deficit_percentual
        calorias_diarias = tdee - deficit_calorias
        
        return {
            'tdee': tdee,
            'deficit_percentual': deficit_percentual * 100,
            'deficit_calorias': round(deficit_calorias, 2),
            'calorias_diarias': round(calorias_diarias, 2),
            'perda_semanal_kg': round(deficit_calorias * 7 / 7700, 2)
        }
    
    @staticmethod
    def calculate_peso_ideal(altura: float, sexo: str) -> Dict[str, float]:
        """
        Calcula o peso ideal usando diferentes fórmulas
        
        Args:
            altura: Altura em metros
            sexo: 'M' para masculino, 'F' para feminino
            
        Returns:
            Dicionário com diferentes estimativas de peso ideal
        """
        altura_cm = altura * 100
        
        # Fórmula de Devine
        if sexo.upper() == 'M':
            devine = 50 + 2.3 * ((altura_cm / 2.54) - 60)
        else:
            devine = 45.5 + 2.3 * ((altura_cm / 2.54) - 60)
        
        # Fórmula de Robinson
        if sexo.upper() == 'M':
            robinson = 52 + 1.9 * ((altura_cm / 2.54) - 60)
        else:
            robinson = 49 + 1.7 * ((altura_cm / 2.54) - 60)
        
        # Fórmula de Miller
        if sexo.upper() == 'M':
            miller = 56.2 + 1.41 * ((altura_cm / 2.54) - 60)
        else:
            miller = 53.1 + 1.36 * ((altura_cm / 2.54) - 60)
        
        # Baseado no IMC ideal (21.5)
        imc_ideal = 21.5 * (altura ** 2)
        
        return {
            'devine': round(devine, 1),
            'robinson': round(robinson, 1),
            'miller': round(miller, 1),
            'imc_ideal': round(imc_ideal, 1),
            'media': round((devine + robinson + miller + imc_ideal) / 4, 1)
        }


class ProgressTracker:
    """Rastreador de progresso de emagrecimento"""
    
    @staticmethod
    def calculate_progress(peso_inicial: float, peso_atual: float, peso_meta: float) -> Dict:
        """
        Calcula o progresso do emagrecimento
        
        Args:
            peso_inicial: Peso inicial em kg
            peso_atual: Peso atual em kg
            peso_meta: Peso meta em kg
            
        Returns:
            Dicionário com estatísticas de progresso
        """
        peso_perdido = peso_inicial - peso_atual
        peso_restante = peso_atual - peso_meta
        total_perder = peso_inicial - peso_meta
        
        if total_perder > 0:
            percentual_completo = (peso_perdido / total_perder) * 100
        else:
            percentual_completo = 100
        
        return {
            'peso_perdido': round(peso_perdido, 2),
            'peso_restante': round(peso_restante, 2),
            'percentual_completo': round(percentual_completo, 1),
            'meta_atingida': peso_atual <= peso_meta
        }
    
    @staticmethod
    def estimate_time_to_goal(peso_atual: float, peso_meta: float, 
                             deficit_diario: float) -> Dict:
        """
        Estima o tempo para atingir a meta
        
        Args:
            peso_atual: Peso atual em kg
            peso_meta: Peso meta em kg
            deficit_diario: Déficit calórico diário
            
        Returns:
            Dicionário com estimativas de tempo
        """
        peso_restante = peso_atual - peso_meta
        
        if peso_restante <= 0:
            return {
                'dias': 0,
                'semanas': 0,
                'meses': 0,
                'data_estimada': datetime.now().strftime('%d/%m/%Y')
            }
        
        # 1kg de gordura = aproximadamente 7700 calorias
        calorias_totais = peso_restante * 7700
        dias = calorias_totais / deficit_diario
        
        data_estimada = datetime.now()
        from datetime import timedelta
        data_estimada = data_estimada + timedelta(days=int(dias))
        
        return {
            'dias': round(dias, 0),
            'semanas': round(dias / 7, 1),
            'meses': round(dias / 30, 1),
            'data_estimada': data_estimada.strftime('%d/%m/%Y')
        }
