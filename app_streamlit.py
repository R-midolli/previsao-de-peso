import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# Função para carregar a animação Lottie
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Função para calcular o TDEE
def calcular_tdee(peso, altura, idade, sexo, nivel_atividade):
    if sexo == "Masculino":
        bmr = 10 * peso + 6.25 * altura - 5 * idade + 5
    else:
        bmr = 10 * peso + 6.25 * altura - 5 * idade - 161

    nivel_atividade_fatores = {
        "Sedentário": 1.2,
        "Levemente ativo": 1.375,
        "Moderadamente ativo": 1.55,
        "Muito ativo": 1.725,
        "Extremamente ativo": 1.9
    }

    return bmr * nivel_atividade_fatores[nivel_atividade]

# Função para calcular a evolução do peso
def calcular_evolucao_peso(peso_atual, peso_alvo, deficit_calorico, tdee):
    calorias_por_kg = 7700
    deficit_calorico_semanal = (deficit_calorico / 100) * tdee * 7
    
    calorias_a_perder = (peso_atual - peso_alvo) * calorias_por_kg
    semanas_necessarias = calorias_a_perder / deficit_calorico_semanal
    
    semanas_lista = np.arange(0, semanas_necessarias + 1)
    pesos = np.linspace(peso_atual, peso_alvo, len(semanas_lista))
    
    df = pd.DataFrame({
        'Semanas': semanas_lista,
        'Peso (kg)': pesos
    })
    return df, semanas_necessarias

def main():
    st.title("Previsão de Peso")
    
    # Carregar animação Lottie
    lottie_url = "https://lottie.host/7cd3da48-3e96-456b-ba7f-c9ea4caf0ece/xhcBXANzWS.json"
    lottie_animation = load_lottieurl(lottie_url)
    
    # Mostrar animação
    st_lottie(lottie_animation, height=200, key="balanca")
    
    # Entradas do usuário
    peso = st.sidebar.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
    altura = st.sidebar.number_input("Altura (cm)", min_value=100.0, max_value=250.0, value=170.0, step=1.0)
    idade = st.sidebar.number_input("Idade", min_value=10, max_value=120, value=30, step=1)
    sexo = st.sidebar.radio("Sexo", ["Masculino", "Feminino"])
    nivel_atividade = st.sidebar.selectbox("Nível de atividade", ["Sedentário", "Levemente ativo", "Moderadamente ativo", "Muito ativo", "Extremamente ativo"])
    peso_alvo = st.sidebar.number_input("Peso alvo (kg)", min_value=30.0, max_value=200.0, value=peso-5.0, step=0.1)
    deficit_calorico = st.sidebar.selectbox("Déficit calórico (%)", [10, 15, 20])
    
    # Calculando o TDEE
    tdee = calcular_tdee(peso, altura, idade, sexo, nivel_atividade)
    
    # Calculando a evolução do peso
    pesos_df, semanas_necessarias = calcular_evolucao_peso(peso, peso_alvo, deficit_calorico, tdee)
    
    # Criando gráfico de linha interativo
    fig = px.line(
        pesos_df,
        x='Semanas',
        y='Peso (kg)',
        title='Evolução do Peso',
        labels={'Semanas': 'Semanas', 'Peso (kg)': 'Peso (kg)'}
    )
    
    # Adicionando anotação de peso alvo
    fig.add_annotation(
        x=semanas_necessarias,
        y=peso_alvo,
        text=f'Peso alvo: {peso_alvo} kg',
        showarrow=True,
        arrowhead=2
    )
    
    # Ajustando o intervalo do gráfico
    fig.update_yaxes(range=[peso_alvo - 10, peso + 10])
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detalhes do Plano de Emagrecimento
    st.subheader("Detalhes do Plano de Emagrecimento")
    calorias_necessarias = tdee - (deficit_calorico / 100) * tdee
    st.write(f"Déficit calórico selecionado: {deficit_calorico}%")
    st.write(f"Semanas necessárias para atingir o peso alvo: {int(semanas_necessarias)}")
    st.write(f"Calorias diárias recomendadas: {calorias_necessarias:.2f}")
    st.write(f"Para atingir seu peso alvo de {peso_alvo:.1f} kg, você precisará de um déficit de {deficit_calorico}% para atingir seu peso alvo em aproximadamente {int(semanas_necessarias)} semanas.")

if __name__ == "__main__":
    main()
