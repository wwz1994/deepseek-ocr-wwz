"""
Aplicativo Web de Emagrecimento
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import HealthCalculator, ProgressTracker
from data_manager import DataManager
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'seu-secret-key-aqui'

# Inicializa o gerenciador de dados
data_manager = DataManager()
calculator = HealthCalculator()
tracker = ProgressTracker()


@app.route('/')
def index():
    """Página inicial - Dashboard"""
    profile = data_manager.get_user_profile()
    weight_history = data_manager.get_weight_history()
    
    stats = None
    if profile and weight_history:
        latest_weight = weight_history[-1]['peso']
        peso_inicial = profile.get('peso_inicial', latest_weight)
        peso_meta = profile.get('peso_meta', latest_weight)
        
        stats = tracker.calculate_progress(peso_inicial, latest_weight, peso_meta)
        stats['peso_atual'] = latest_weight
        stats['peso_inicial'] = peso_inicial
        stats['peso_meta'] = peso_meta
    
    return render_template('index.html', 
                         profile=profile, 
                         stats=stats,
                         weight_history=weight_history[-7:])  # Últimos 7 registros


@app.route('/calculators')
def calculators():
    """Página de calculadoras"""
    profile = data_manager.get_user_profile()
    return render_template('calculators.html', profile=profile)


@app.route('/progress')
def progress():
    """Página de progresso"""
    profile = data_manager.get_user_profile()
    weight_history = data_manager.get_weight_history()
    
    return render_template('progress.html', 
                         profile=profile,
                         weight_history=weight_history)


@app.route('/meal-plans')
def meal_plans():
    """Página de planos alimentares"""
    profile = data_manager.get_user_profile()
    return render_template('meal_plans.html', profile=profile)


# API Endpoints

@app.route('/api/calculate-imc', methods=['POST'])
def api_calculate_imc():
    """Calcula o IMC"""
    data = request.json
    peso = float(data.get('peso'))
    altura = float(data.get('altura'))
    
    imc, classificacao, descricao = calculator.calculate_imc(peso, altura)
    
    return jsonify({
        'imc': imc,
        'classificacao': classificacao,
        'descricao': descricao
    })


@app.route('/api/calculate-tmb', methods=['POST'])
def api_calculate_tmb():
    """Calcula a TMB e TDEE"""
    data = request.json
    peso = float(data.get('peso'))
    altura = float(data.get('altura'))  # em cm
    idade = int(data.get('idade'))
    sexo = data.get('sexo')
    nivel_atividade = data.get('nivel_atividade', 'sedentario')
    
    tmb = calculator.calculate_tmb(peso, altura, idade, sexo)
    tdee = calculator.calculate_tdee(tmb, nivel_atividade)
    
    return jsonify({
        'tmb': tmb,
        'tdee': tdee
    })


@app.route('/api/calculate-deficit', methods=['POST'])
def api_calculate_deficit():
    """Calcula o déficit calórico"""
    data = request.json
    peso = float(data.get('peso'))
    altura = float(data.get('altura'))  # em cm
    idade = int(data.get('idade'))
    sexo = data.get('sexo')
    nivel_atividade = data.get('nivel_atividade', 'sedentario')
    objetivo = data.get('objetivo', 'moderado')
    
    tmb = calculator.calculate_tmb(peso, altura, idade, sexo)
    tdee = calculator.calculate_tdee(tmb, nivel_atividade)
    deficit_info = calculator.calculate_deficit(tdee, objetivo)
    
    return jsonify(deficit_info)


@app.route('/api/calculate-peso-ideal', methods=['POST'])
def api_calculate_peso_ideal():
    """Calcula o peso ideal"""
    data = request.json
    altura = float(data.get('altura'))  # em metros
    sexo = data.get('sexo')
    
    peso_ideal = calculator.calculate_peso_ideal(altura, sexo)
    
    return jsonify(peso_ideal)


@app.route('/api/save-profile', methods=['POST'])
def api_save_profile():
    """Salva o perfil do usuário"""
    data = request.json
    
    profile = {
        'nome': data.get('nome'),
        'idade': int(data.get('idade')),
        'sexo': data.get('sexo'),
        'altura': float(data.get('altura')),
        'peso_inicial': float(data.get('peso_inicial')),
        'peso_meta': float(data.get('peso_meta')),
        'nivel_atividade': data.get('nivel_atividade'),
        'objetivo': data.get('objetivo'),
        'data_criacao': datetime.now().isoformat()
    }
    
    data_manager.save_user_profile(profile)
    
    # Adiciona o peso inicial ao histórico
    data_manager.add_weight_entry(profile['peso_inicial'])
    
    return jsonify({'success': True, 'message': 'Perfil salvo com sucesso!'})


@app.route('/api/add-weight', methods=['POST'])
def api_add_weight():
    """Adiciona uma entrada de peso"""
    data = request.json
    peso = float(data.get('peso'))
    data_entrada = data.get('data')  # Opcional
    
    data_manager.add_weight_entry(peso, data_entrada)
    
    return jsonify({'success': True, 'message': 'Peso registrado com sucesso!'})


@app.route('/api/get-weight-history', methods=['GET'])
def api_get_weight_history():
    """Obtém o histórico de pesos"""
    history = data_manager.get_weight_history()
    return jsonify(history)


@app.route('/api/delete-weight/<data>', methods=['DELETE'])
def api_delete_weight(data):
    """Remove uma entrada de peso"""
    data_manager.delete_weight_entry(data)
    return jsonify({'success': True, 'message': 'Peso removido com sucesso!'})


@app.route('/api/get-progress', methods=['GET'])
def api_get_progress():
    """Obtém estatísticas de progresso"""
    profile = data_manager.get_user_profile()
    weight_history = data_manager.get_weight_history()
    
    if not profile or not weight_history:
        return jsonify({'error': 'Dados insuficientes'}), 400
    
    latest_weight = weight_history[-1]['peso']
    peso_inicial = profile.get('peso_inicial', latest_weight)
    peso_meta = profile.get('peso_meta', latest_weight)
    
    progress = tracker.calculate_progress(peso_inicial, latest_weight, peso_meta)
    
    # Calcula estimativa de tempo
    if 'objetivo' in profile:
        altura = profile['altura']
        idade = profile['idade']
        sexo = profile['sexo']
        nivel_atividade = profile.get('nivel_atividade', 'sedentario')
        objetivo = profile['objetivo']
        
        tmb = calculator.calculate_tmb(latest_weight, altura, idade, sexo)
        tdee = calculator.calculate_tdee(tmb, nivel_atividade)
        deficit_info = calculator.calculate_deficit(tdee, objetivo)
        
        time_estimate = tracker.estimate_time_to_goal(
            latest_weight, 
            peso_meta, 
            deficit_info['deficit_calorias']
        )
        
        progress['estimativa_tempo'] = time_estimate
    
    return jsonify(progress)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
