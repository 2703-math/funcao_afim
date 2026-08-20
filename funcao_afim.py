import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Função de 1º Grau",
    page_icon="📈",
    layout="wide"
)

# ============================================
# CSS PERSONALIZADO
# ============================================
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #555;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .concept-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 4px solid;
        margin-bottom: 1rem;
    }
    .equation-box {
        background: #1a1a2e;
        color: #fff;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-family: 'Courier New', monospace;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .param-box {
        background: #fff;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÕES DE PLOTAGEM (PLOTLY)
# ============================================
def criar_layout_cartesiano(fig, title="Plano Cartesiano"):
    """Aplica o estilo de 'papel milimetrado' com eixos fixos"""
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20),
        height=500,
        showlegend=True,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.8)")
    )
    
    # Eixo X fixo e destacado
    fig.update_xaxes(
        range=[-10, 10],
        zeroline=True, zerolinewidth=2, zerolinecolor='#2c3e50',
        gridcolor='#e0e0e0', dtick=1
    )
    
    # Eixo Y fixo e destacado
    fig.update_yaxes(
        range=[-10, 10],
        zeroline=True, zerolinewidth=2, zerolinecolor='#2c3e50',
        gridcolor='#e0e0e0', dtick=1
    )
    return fig

def plot_funcao_unica(a, b):
    fig = go.Figure()
    
    # Valores de X e Y
    x = np.linspace(-12, 12, 100)
    y = a * x + b
    
    # Reta Principal
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='lines',
        name=f'f(x) = {a}x + {b}',
        line=dict(color='#3498db', width=4)
    ))
    
    # Ponto: Intercepto Y (0, b)
    fig.add_trace(go.Scatter(
        x=[0], y=[b], mode='markers+text',
        name='Coeficiente Linear (b)',
        marker=dict(color='#e74c3c', size=12, line=dict(color='white', width=2)),
        text=[f'b = {b}'], textposition='top right', textfont=dict(color='#e74c3c', size=14)
    ))
    
    # Ponto: Raiz (-b/a, 0)
    if a != 0:
        raiz = -b / a
        if -10 <= raiz <= 10: # Só desenha se estiver dentro da tela
            fig.add_trace(go.Scatter(
                x=[raiz], y=[0], mode='markers+text',
                name='Raiz da Função',
                marker=dict(color='#2ecc71', size=12, line=dict(color='white', width=2)),
                text=[f'Raiz = {raiz:.1f}'], textposition='bottom right', textfont=dict(color='#2ecc71', size=14)
            ))
            
    # Triângulo da Taxa de Variação (Mostra o significado de 'a')
    # Pegamos um ponto x0 (ex: 1) para x1 (ex: 2)
    x0 = 1
    y0 = a * x0 + b
    x1 = 2
    y1 = a * x1 + b
    
    # Desenha o triângulo pontilhado se estiver dentro da tela
    if -10 <= y0 <= 10 and -10 <= y1 <= 10:
        fig.add_trace(go.Scatter(
            x=[x0, x1, x1], y=[y0, y0, y1],
            mode='lines+text', name='Taxa de Variação (a)',
            line=dict(color='#f39c12', width=2, dash='dot'),
            text=['', 'Δx = +1', f'Δy = {a}'],
            textposition=['middle center', 'bottom center', 'middle right'],
            textfont=dict(color='#f39c12', size=12),
            hoverinfo='skip'
        ))

    return criar_layout_cartesiano(fig, title="Comportamento Gráfico")

def plot_comparacao(a1, b1, a2, b2):
    fig = go.Figure()
    
    x = np.linspace(-12, 12, 100)
    y1 = a1 * x + b1
    y2 = a2 * x + b2
    
    # Reta 1
    fig.add_trace(go.Scatter(
        x=x, y=y1, mode='lines',
        name=f'f(x) = {a1}x + {b1}',
        line=dict(color='#3498db', width=3)
    ))
    
    # Reta 2
    fig.add_trace(go.Scatter(
        x=x, y=y2, mode='lines',
        name=f'g(x) = {a2}x + {b2}',
        line=dict(color='#9b59b6', width=3)
    ))
    
    # Ponto de Interseção
    if a1 != a2:
        x_int = (b2 - b1) / (a1 - a2)
        y_int = a1 * x_int + b1
        
        if -10 <= x_int <= 10 and -10 <= y_int <= 10:
            fig.add_trace(go.Scatter(
                x=[x_int], y=[y_int], mode='markers+text',
                name='Interseção',
                marker=dict(color='#e74c3c', size=14, symbol='star', line=dict(color='white', width=2)),
                text=[f'({x_int:.1f}, {y_int:.1f})'], textposition='top center',
                textfont=dict(color='#c0392b', size=14, family="Arial Black")
            ))
            
            # Linhas guias até os eixos
            fig.add_trace(go.Scatter(
                x=[x_int, x_int, 0], y=[0, y_int, y_int],
                mode='lines', line=dict(color='#e74c3c', width=1, dash='dot'),
                showlegend=False, hoverinfo='skip'
            ))

    return criar_layout_cartesiano(fig, title="Sistemas e Interseção")

# ============================================
# TÍTULO E MENU LATERAL
# ============================================
st.markdown('<div class="main-title">📈 Estudo da Função de 1º Grau</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interaja com os coeficientes e veja o gráfico se transformar em tempo real</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Navegação")
    topico = st.radio(
        "Escolha o cenário:",
        ["1. Explorando a Função", "2. Comparando Funções (Sistemas)"],
        index=0
    )
    st.markdown("---")
    st.markdown("""
    <div style='color:#777; font-size:0.9rem;'>
        <b>Dica:</b><br>
        Arraste os sliders que estão na tela principal. O gráfico responde instantaneamente!
    </div>
    """, unsafe_allow_html=True)

# ============================================
# CENÁRIO 1: EXPLORANDO A FUNÇÃO
# ============================================
if topico == "1. Explorando a Função":
    st.markdown("""
    <div class="concept-card" style="border-left-color: #3498db;">
        <b>O que é?</b> A Função de 1º Grau (ou função afim) é definida pela lei <b>f(x) = ax + b</b>. 
        Seu gráfico é sempre uma reta. O parâmetro <b>a</b> controla a inclinação e o <b>b</b> controla onde a reta corta o eixo vertical.
    </div>
    """, unsafe_allow_html=True)
    
    # LAYOUT: Controles à esquerda, Gráfico à direita
    col_controles, col_grafico = st.columns([1, 2.5])
    
    with col_controles:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Controles")
        
        a = st.slider("Coeficiente Angular (a)", -5.0, 5.0, 2.0, step=0.5)
        st.markdown("<span style='font-size:0.85rem; color:#777;'>Controla a inclinação (taxa de crescimento). Se a > 0 é crescente, se a < 0 é decrescente.</span>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        b = st.slider("Coeficiente Linear (b)", -10.0, 10.0, -2.0, step=0.5)
        st.markdown("<span style='font-size:0.85rem; color:#777;'>Controla o ponto onde a reta cruza o eixo Y. É o 'valor inicial' da função.</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Mostrador dinâmico da fórmula
        sinal_b = f"+ {b}" if b >= 0 else f"- {abs(b)}"
        st.markdown(f"""
        <div class="equation-box">
            f(x) = {a}x {sinal_b}
        </div>
        """, unsafe_allow_html=True)

    with col_grafico:
        fig = plot_funcao_unica(a, b)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# CENÁRIO 2: COMPARANDO FUNÇÕES
# ============================================
elif topico == "2. Comparando Funções (Sistemas)":
    st.markdown("""
    <div class="concept-card" style="border-left-color: #9b59b6;">
        <b>Sistemas de Equações:</b> Quando plotamos duas funções no mesmo plano, o ponto onde elas se cruzam (interseção) é a solução exata 
        do sistema formado pelas duas equações. É o momento em que <b>f(x) = g(x)</b>!
    </div>
    """, unsafe_allow_html=True)
    
    # LAYOUT: Controles em cima (duas colunas), Gráfico embaixo (para ter mais espaço lateral para as duas)
    col_f, col_g = st.columns(2)
    
    with col_f:
        st.markdown("""
        <div style="background:#eaf2f8; padding:1rem; border-radius:10px; border-top: 4px solid #3498db;">
            <h4 style="color:#2980b9; margin-top:0;">🔵 Função f(x)</h4>
        """, unsafe_allow_html=True)
        a1 = st.slider("Coeficiente a₁", -5.0, 5.0, 1.0, step=0.5)
        b1 = st.slider("Coeficiente b₁", -10.0, 10.0, 2.0, step=0.5)
        sinal_b1 = f"+ {b1}" if b1 >= 0 else f"- {abs(b1)}"
        st.markdown(f"<div style='text-align:center; font-size:1.3rem; font-weight:bold; color:#2980b9;'>f(x) = {a1}x {sinal_b1}</div></div>", unsafe_allow_html=True)

    with col_g:
        st.markdown("""
        <div style="background:#f4ecf7; padding:1rem; border-radius:10px; border-top: 4px solid #9b59b6;">
            <h4 style="color:#8e44ad; margin-top:0;">🟣 Função g(x)</h4>
        """, unsafe_allow_html=True)
        a2 = st.slider("Coeficiente a₂", -5.0, 5.0, -1.0, step=0.5)
        b2 = st.slider("Coeficiente b₂", -10.0, 10.0, 6.0, step=0.5)
        sinal_b2 = f"+ {b2}" if b2 >= 0 else f"- {abs(b2)}"
        st.markdown(f"<div style='text-align:center; font-size:1.3rem; font-weight:bold; color:#8e44ad;'>g(x) = {a2}x {sinal_b2}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráfico pega a largura total abaixo dos controles
    fig = plot_comparacao(a1, b1, a2, b2)
    st.plotly_chart(fig, use_container_width=True)
    
    # Card inferior de explicação
    if a1 == a2:
        if b1 == b2:
            st.warning("⚠️ **Retas Coincidentes!** Elas têm a mesma inclinação e o mesmo ponto de corte. É exatamente a mesma reta (infinitas soluções).")
        else:
            st.error("🛑 **Retas Paralelas!** Elas têm a mesma inclinação (a₁ = a₂), mas cruzam o eixo Y em lugares diferentes. Elas nunca vão se tocar (sistema sem solução).")
    else:
        st.success("✅ **Retas Concorrentes!** Como as inclinações são diferentes, elas obrigatoriamente se cruzam em um único ponto.")

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    📈 <b>Matemática Visual</b> — Explore as funções brincando com os controles.
</div>
""", unsafe_allow_html=True)