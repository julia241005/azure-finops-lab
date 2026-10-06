import json
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Azure FinOps Lab",
    page_icon="F",
    layout="wide",
    initial_sidebar_state="expanded",
)


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_FILE = PROJECT_ROOT / "data" / "costs.csv"


# ============================================================
# ESTILO
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #f7f8fa;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: #111827;
    }

    [data-testid="stSidebar"] * {
        color: #f9fafb;
    }

    .brand {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }

    .brand-subtitle {
        font-size: 13px;
        color: #9ca3af;
        margin-bottom: 30px;
    }

    .page-title {
        font-size: 34px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 4px;
    }

    .page-subtitle {
        font-size: 15px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        min-height: 120px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }

    .metric-label {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 27px;
        font-weight: 700;
        color: #111827;
    }

    .section-title {
        font-size: 20px;
        font-weight: 650;
        color: #111827;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    .recommendation-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    .resource-name {
        font-size: 16px;
        font-weight: 700;
        color: #111827;
    }

    .resource-meta {
        font-size: 13px;
        color: #6b7280;
        margin-top: 4px;
    }

    .badge {
        display: inline-block;
        padding: 5px 9px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        margin-top: 10px;
    }

    .badge-idle {
        background: #fef3c7;
        color: #92400e;
    }

    .badge-rightsizing {
        background: #dbeafe;
        color: #1e40af;
    }

    .saving {
        font-size: 18px;
        font-weight: 700;
        color: #047857;
        text-align: right;
    }

    .footer {
        color: #9ca3af;
        font-size: 12px;
        text-align: center;
        margin-top: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNÇÕES
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    df["cost"] = pd.to_numeric(
        df["cost"],
        errors="coerce"
    )

    df["cpu_usage"] = pd.to_numeric(
        df["cpu_usage"],
        errors="coerce"
    )

    return df


def analyze_resources(df):
    recommendations = []

    for _, row in df.iterrows():

        if row["service"] != "Virtual Machine":
            continue

        cpu = float(row["cpu_usage"])
        cost = float(row["cost"])

        if cpu < 10:

            recommendations.append({
                "resource": row["resource"],
                "environment": row["environment"],
                "classification": "POSSIBLE_IDLE_RESOURCE",
                "cpu_usage": cpu,
                "saving": cost,
                "recommendation": (
                    "Avaliar desligamento, remoção "
                    "ou agendamento."
                ),
            })

        elif cpu < 20:

            recommendations.append({
                "resource": row["resource"],
                "environment": row["environment"],
                "classification": "POSSIBLE_RIGHTSIZING",
                "cpu_usage": cpu,
                "saving": cost * 0.30,
                "recommendation": (
                    "Avaliar se a VM está "
                    "superdimensionada."
                ),
            })

    return recommendations


def money(value):
    return (
        f"R$ {value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# ============================================================
# DADOS
# ============================================================

df = load_data()

total_cost = float(df["cost"].sum())

recommendations = analyze_resources(df)

monthly_saving = sum(
    item["saving"]
    for item in recommendations
)

annual_saving = monthly_saving * 12


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">AZURE FINOPS LAB</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'Cloud Cost Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Navegação")

    page = st.radio(
        "",
        [
            "Visão geral",
            "Oportunidades",
            "Dados"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### Ambiente")

    st.caption("Dados simulados")
    st.caption("Python + Streamlit")
    st.caption("FinOps Analysis Engine")


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="page-title">'
    'Cloud Cost Intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Análise de custos e oportunidades de otimização Cloud'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# VISÃO GERAL
# ============================================================

if page == "Visão geral":

    cols = st.columns(4)

    metrics = [
        ("CUSTO MENSAL", money(total_cost)),
        ("ECONOMIA POTENCIAL / MÊS", money(monthly_saving)),
        ("ECONOMIA POTENCIAL / ANO", money(annual_saving)),
        ("RECURSOS ANALISADOS", str(len(df))),
    ]

    for col, (label, value) in zip(cols, metrics):

        with col:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        {label}
                    </div>
                    <div class="metric-value">
                        {value}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # GRÁFICOS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Cost Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("**Custo por serviço**")

        service_cost = (
            df.groupby("service")["cost"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(service_cost)


    with col2:

        st.markdown("**Custo por ambiente**")

        environment_cost = (
            df.groupby("environment")["cost"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(environment_cost)


    # --------------------------------------------------------
    # RESUMO
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Optimization Summary'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Oportunidades encontradas",
            len(recommendations)
        )

    with col2:
        st.metric(
            "VMs analisadas",
            len(
                df[
                    df["service"]
                    == "Virtual Machine"
                ]
            )
        )

    with col3:

        saving_percentage = (
            monthly_saving / total_cost * 100
            if total_cost
            else 0
        )

        st.metric(
            "Economia potencial",
            f"{saving_percentage:.1f}%"
        )


# ============================================================
# OPORTUNIDADES
# ============================================================

elif page == "Oportunidades":

    st.markdown(
        '<div class="section-title">'
        'Optimization Opportunities'
        '</div>',
        unsafe_allow_html=True
    )

    if not recommendations:

        st.success(
            "Nenhuma oportunidade identificada."
        )

    else:

        for item in recommendations:

            if item["classification"] == "POSSIBLE_IDLE_RESOURCE":

                badge_class = "badge-idle"
                badge_text = "POSSIBLE IDLE RESOURCE"

            else:

                badge_class = "badge-rightsizing"
                badge_text = "POSSIBLE RIGHTSIZING"


            col1, col2 = st.columns([4, 1])

            with col1:

                st.markdown(
                    f"""
                    <div class="recommendation-card">

                        <div class="resource-name">
                            {item["resource"]}
                        </div>

                        <div class="resource-meta">
                            Ambiente: {item["environment"]}
                            &nbsp;&nbsp; | &nbsp;&nbsp;
                            CPU: {item["cpu_usage"]:.0f}%
                        </div>

                        <span class="badge {badge_class}">
                            {badge_text}
                        </span>

                        <div class="resource-meta">
                            {item["recommendation"]}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                st.markdown(
                    f"""
                    <div class="recommendation-card">
                        <div class="metric-label">
                            ECONOMIA ESTIMADA
                        </div>
                        <div class="saving">
                            {money(item["saving"])}
                        </div>
                        <div class="resource-meta">
                            por mês
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# DADOS
# ============================================================

elif page == "Dados":

    st.markdown(
        '<div class="section-title">'
        'Analyzed Resources'
        '</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        '<div class="section-title">'
        'Dataset Summary'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        f"Total de registros analisados: **{len(df)}**"
    )


# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    """
    <div class="footer">
        Azure FinOps Lab · Educational Cloud Cost Optimization Project
        · Dados simulados
    </div>
    """,
    unsafe_allow_html=True
)