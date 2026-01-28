// Funções auxiliares e interatividade global

// Formata número para exibição
function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals);
}

// Formata data para exibição
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

// Mostra mensagem de sucesso
function showSuccess(message) {
    alert('✅ ' + message);
}

// Mostra mensagem de erro
function showError(message) {
    alert('❌ ' + message);
}

// Valida formulário
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value) {
            input.style.borderColor = 'var(--danger-color)';
            isValid = false;
        } else {
            input.style.borderColor = 'var(--border-color)';
        }
    });
    
    return isValid;
}

// Animação de scroll suave
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Adiciona classe active ao link do menu atual
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.color = 'var(--primary-color)';
            link.style.background = 'var(--bg-color)';
        }
    });
});

// Função para fazer requisições à API
async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(endpoint, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// Função para atualizar progresso em tempo real
async function updateProgress() {
    try {
        const progress = await apiRequest('/api/get-progress');
        
        // Atualiza elementos na página se existirem
        const elements = {
            'pesoAtual': progress.peso_atual,
            'pesoPerdido': progress.peso_perdido,
            'pesoRestante': progress.peso_restante,
            'percentualCompleto': progress.percentual_completo
        };
        
        Object.keys(elements).forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = elements[id];
            }
        });
        
        // Atualiza barra de progresso
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar && progress.percentual_completo) {
            progressBar.style.width = progress.percentual_completo + '%';
        }
        
    } catch (error) {
        console.error('Erro ao atualizar progresso:', error);
    }
}

// Função para carregar histórico de pesos
async function loadWeightHistory() {
    try {
        const history = await apiRequest('/api/get-weight-history');
        return history;
    } catch (error) {
        console.error('Erro ao carregar histórico:', error);
        return [];
    }
}

// Validação de inputs numéricos
document.addEventListener('DOMContentLoaded', function() {
    const numberInputs = document.querySelectorAll('input[type="number"]');
    
    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            const min = parseFloat(this.min);
            const max = parseFloat(this.max);
            const value = parseFloat(this.value);
            
            if (value < min) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
            }
        });
    });
});

// Adiciona efeito de loading aos botões
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Processando...';
                
                // Restaura o botão após 3 segundos (caso algo dê errado)
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.textContent = submitBtn.getAttribute('data-original-text') || 'Enviar';
                }, 3000);
            }
        });
    });
});

// Salva texto original dos botões
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('button[type="submit"]');
    buttons.forEach(btn => {
        btn.setAttribute('data-original-text', btn.textContent);
    });
});

// Função para calcular IMC localmente (validação)
function calculateIMC(peso, altura) {
    return peso / (altura * altura);
}

// Função para validar peso
function isValidWeight(peso) {
    return peso >= 30 && peso <= 300;
}

// Função para validar altura
function isValidHeight(altura) {
    return altura >= 1.0 && altura <= 2.5;
}

// Adiciona tooltips informativos
document.addEventListener('DOMContentLoaded', function() {
    const labels = document.querySelectorAll('label');
    
    const tooltips = {
        'TMB': 'Taxa Metabólica Basal - calorias queimadas em repouso',
        'TDEE': 'Total Daily Energy Expenditure - gasto calórico total diário',
        'IMC': 'Índice de Massa Corporal - relação entre peso e altura',
        'Déficit': 'Redução de calorias necessária para emagrecer'
    };
    
    labels.forEach(label => {
        const text = label.textContent;
        Object.keys(tooltips).forEach(key => {
            if (text.includes(key)) {
                label.title = tooltips[key];
                label.style.cursor = 'help';
            }
        });
    });
});

// Previne envio duplicado de formulários
let formSubmitting = false;

document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (formSubmitting) {
                e.preventDefault();
                return false;
            }
            formSubmitting = true;
            
            setTimeout(() => {
                formSubmitting = false;
            }, 2000);
        });
    });
});

// Função para exportar dados (futura implementação)
function exportData() {
    console.log('Exportar dados - funcionalidade futura');
}

// Função para imprimir relatório (futura implementação)
function printReport() {
    window.print();
}

// Console log de boas-vindas
console.log('%c💪 FitLife - Aplicativo de Emagrecimento', 'color: #3b82f6; font-size: 20px; font-weight: bold;');
console.log('%cVersão 1.0.0', 'color: #64748b; font-size: 12px;');
