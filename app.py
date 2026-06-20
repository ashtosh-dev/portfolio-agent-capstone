import streamlit as st
import asyncio
import os
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables (.env file)
load_dotenv()

# Set page configuration with premium styling layout
st.set_page_config(
    page_title="Autonomous Portfolio & ETF Strategist",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS injection for glassmorphism and modern dark aesthetics
st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Main background */
    .stApp {
        background: radial-gradient(circle at top right, #121826 0%, #090b11 100%);
        color: #f3f4f6;
    }
    
    /* Sidebar premium styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid #1f293d;
    }
    
    /* Custom Card container for report output */
    .report-card {
        background: rgba(17, 25, 40, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-top: 24px;
    }
    
    /* Sidebar inputs */
    .stTextInput>div>div>input {
        background-color: #161f30 !important;
        border: 1px solid #2d3b55 !important;
        color: #f3f4f6 !important;
        border-radius: 8px !important;
    }
    
    .stSlider>div>div>div>div {
        background-color: #00F0FF !important;
    }
    
    /* Generate button styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00F0FF 0%, #00a8cc 100%);
        color: #0E1117;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0 4px 14px 0 rgba(0, 240, 255, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #00a8cc 0%, #007d99 100%);
        box-shadow: 0 6px 20px 0 rgba(0, 240, 255, 0.6);
        transform: translateY(-2px);
    }
    
    /* Header Gradient Text */
    .header-title {
        background: linear-gradient(to right, #00F0FF, #00a8cc, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 8px;
    }
    
    .header-subtitle {
        color: #9ca3af;
        font-size: 1.1rem;
        margin-bottom: 32px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title & Subtitle
st.markdown('<div class="header-title">Autonomous Portfolio & ETF Strategist</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Multi-Agent AI team fetching live market metrics, executing quantitative code, and planning allocations.</div>', unsafe_allow_html=True)

# Sidebar for controls
st.sidebar.markdown("### 🛠️ Portfolio Configuration")

equity_ticker = st.sidebar.text_input("Equity Ticker", value="VOO", help="Enter ETF or Stock Ticker (e.g., VOO, QQQ, SPY)")
bond_ticker = st.sidebar.text_input("Bond Ticker", value="AGG", help="Enter Bond Ticker (e.g., AGG, BND)")

equity_allocation = st.sidebar.slider("Equity Allocation (%)", min_value=0, max_value=100, value=60, step=5)
bond_allocation = 100 - equity_allocation

st.sidebar.markdown(f"**Target Mix:** {equity_allocation}% {equity_ticker} / {bond_allocation}% {bond_ticker}")

# Dynamic Donut Chart in the sidebar showing allocations
allocation_df = pd.DataFrame({
    "Asset": [equity_ticker, bond_ticker],
    "Allocation": [equity_allocation, bond_allocation]
})

fig = px.pie(
    allocation_df,
    names="Asset",
    values="Allocation",
    hole=0.45,
    color_discrete_sequence=["#00F0FF", "#1E2127"]
)

fig.update_layout(
    showlegend=False,
    margin=dict(t=0, b=0, l=10, r=10),
    height=180,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
st.sidebar.plotly_chart(fig, use_container_width=True)

# Display active API Key alert if missing
api_key_set = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key_set:
    st.sidebar.warning("⚠️ API Key not found. Please set GEMINI_API_KEY in your environment or .env file.")

generate_button = st.sidebar.button("Generate Strategy")

# Import execution logic
from main_workflow import run_portfolio_workflow

if not generate_button:
    # 4. The "Empty State" Architecture
    st.markdown("### 🏛️ System Architecture")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(
            "**🕵️ Context Agent**\n\n"
            "Uses Model Context Protocol (MCP) to pull live Yahoo Finance data, including prices, yields, returns, and summaries."
        )
    with col2:
        st.info(
            "**🧮 Quant Agent**\n\n"
            "Writes and executes sandbox Python code to calculate MPT metrics: annualized volatility, Sharpe ratio, beta, and max drawdown."
        )
    with col3:
        st.info(
            "**📝 Strategist Agent**\n\n"
            "Orchestrates and synthesizes the live data and mathematical metrics into a comprehensive, client-ready markdown report."
        )
    
    st.info("👈 Configure your portfolio allocation in the sidebar and click **Generate Strategy** to launch the multi-agent pipeline.")
else:
    if not api_key_set:
        st.error("Cannot proceed: Please set the GEMINI_API_KEY environment variable to authenticate Gemini models.")
    else:
        # Construct the detailed request prompt
        prompt = (
            f"Create an investment portfolio with {equity_allocation}% {equity_ticker} (equity) "
            f"and {bond_allocation}% {bond_ticker} (bonds). "
            f"Download 5 years of historical data for {equity_ticker}, {bond_ticker}, and S&P 500 (^GSPC). "
            f"Calculate the annualized volatility, Sharpe ratio (using 4% risk-free rate), beta, maximum drawdown, "
            f"and present a client-ready synthesized portfolio report."
        )
        
        # Display spinner with premium text
        with st.spinner("🤖 AI Agents are pulling live Yahoo Finance data, executing calculations, and drafting the report..."):
            try:
                # Execute async workflow
                report = asyncio.run(run_portfolio_workflow(prompt))
                
                # 5. Tabbed Output
                tab1, tab2 = st.tabs(["📊 Client Report", "🤖 System Logs"])
                
                with tab1:
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    if report.strip():
                        st.markdown(report)
                    else:
                        st.error("No report output was generated by the Strategist Agent. Please check the terminal logs.")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with tab2:
                    st.markdown("### Agent Execution Log")
                    st.json({
                        "session_id": "default_session",
                        "user_id": "default_user",
                        "requested_portfolio": {
                            "equity": {
                                "ticker": equity_ticker,
                                "allocation": f"{equity_allocation}%"
                            },
                            "bond": {
                                "ticker": bond_ticker,
                                "allocation": f"{bond_allocation}%"
                            }
                        },
                        "orchestrator_node": "portfolio_orchestrator",
                        "execution_steps": [
                            {"step": 1, "node": "context_agent", "action": "Fetched live market profiles via yfinance"},
                            {"step": 2, "node": "quant_agent", "action": "Calculated portfolio volatility, Sharpe ratio, beta, and max drawdown via sandbox Python executor"},
                            {"step": 3, "node": "strategist_agent", "action": "Synthesized MPT metrics and ETF information into the final investment report"}
                        ]
                    })
                    
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
