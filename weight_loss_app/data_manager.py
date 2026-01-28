"""
Gerenciador de dados do usuário
"""
import json
import os
from datetime import datetime
from typing import Dict, List


class DataManager:
    """Gerencia os dados do usuário em arquivo JSON"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self.user_file = os.path.join(data_dir, 'user_data.json')
        self.weights_file = os.path.join(data_dir, 'weight_history.json')
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Garante que os arquivos de dados existam"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        if not os.path.exists(self.user_file):
            self._save_json(self.user_file, {})
        
        if not os.path.exists(self.weights_file):
            self._save_json(self.weights_file, [])
    
    def _load_json(self, filepath: str) -> any:
        """Carrega dados de um arquivo JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if filepath == self.user_file else []
    
    def _save_json(self, filepath: str, data: any):
        """Salva dados em um arquivo JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def save_user_profile(self, profile: Dict):
        """Salva o perfil do usuário"""
        self._save_json(self.user_file, profile)
    
    def get_user_profile(self) -> Dict:
        """Obtém o perfil do usuário"""
        return self._load_json(self.user_file)
    
    def add_weight_entry(self, peso: float, data: str = None):
        """
        Adiciona uma entrada de peso
        
        Args:
            peso: Peso em kg
            data: Data no formato 'YYYY-MM-DD' (opcional, usa data atual se não fornecida)
        """
        if data is None:
            data = datetime.now().strftime('%Y-%m-%d')
        
        weights = self._load_json(self.weights_file)
        
        # Verifica se já existe entrada para esta data
        existing_index = None
        for i, entry in enumerate(weights):
            if entry['data'] == data:
                existing_index = i
                break
        
        entry = {
            'data': data,
            'peso': peso,
            'timestamp': datetime.now().isoformat()
        }
        
        if existing_index is not None:
            weights[existing_index] = entry
        else:
            weights.append(entry)
        
        # Ordena por data
        weights.sort(key=lambda x: x['data'])
        
        self._save_json(self.weights_file, weights)
    
    def get_weight_history(self) -> List[Dict]:
        """Obtém o histórico de pesos"""
        return self._load_json(self.weights_file)
    
    def get_latest_weight(self) -> float:
        """Obtém o peso mais recente"""
        weights = self.get_weight_history()
        if weights:
            return weights[-1]['peso']
        return None
    
    def delete_weight_entry(self, data: str):
        """
        Remove uma entrada de peso
        
        Args:
            data: Data no formato 'YYYY-MM-DD'
        """
        weights = self._load_json(self.weights_file)
        weights = [w for w in weights if w['data'] != data]
        self._save_json(self.weights_file, weights)
    
    def clear_all_data(self):
        """Limpa todos os dados"""
        self._save_json(self.user_file, {})
        self._save_json(self.weights_file, [])
