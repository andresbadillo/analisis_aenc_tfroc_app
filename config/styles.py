"""Estilos CSS personalizados para la aplicación."""

CUSTOM_CSS = """
<style>
/* Estilos generales */
.main-header {
    text-align: center;
    color: #1f77b4;
    margin-bottom: 2rem;
}

.titulo-principal {
    text-align: center;
    color: #64B43F;
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.subtitulo {
    color: #333;
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    border-bottom: 2px solid #64B43F;
    padding-bottom: 0.5rem;
}

/* Estilos para botones */
.stButton > button {
    background-color: #64B43F;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: #4a8c2f;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.stButton > button:disabled {
    background-color: #cccccc;
    color: #666666;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

/* Estilos para contenedores de pasos */
.step-container {
    background-color: #f8f9fa;
    border: 2px solid #e9ecef;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.step-container:hover {
    border-color: #64B43F;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.step-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
}

.step-number {
    background-color: #64B43F;
    color: white;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-right: 1rem;
}

.step-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #333;
}

/* Estilos para mensajes de estado */
.status-message {
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    font-weight: 500;
}

.status-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.status-error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.status-warning {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}

.status-info {
    background-color: #d1ecf1;
    color: #0c5460;
    border: 1px solid #bee5eb;
}

/* Estilos para barras de progreso */
.progress-container {
    margin: 1rem 0;
}

.progress-label {
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #333;
}

/* Estilos para el sidebar */
.sidebar .sidebar-content {
    background-color: #f8f9fa;
}

.sidebar-header {
    text-align: center;
    margin-bottom: 2rem;
}

/* Estilos para tablas */
.dataframe {
    font-size: 0.9rem;
}

/* Estilos para métricas */
.metric-container {
    background-color: white;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    text-align: center;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    color: #64B43F;
}

.metric-label {
    font-size: 0.9rem;
    color: #666;
    margin-top: 0.5rem;
}

/* Estilos para el footer */
.footer {
    text-align: center;
    padding: 2rem 0;
    color: #666;
    font-size: 0.9rem;
    border-top: 1px solid #e9ecef;
    margin-top: 3rem;
}
</style>
"""
