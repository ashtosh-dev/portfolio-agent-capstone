import streamlit as st
import asyncio
import os
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
        background-color: #4f46e5 !important;
    }
    
    /* Generate button styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.6);
        transform: translateY(-2px);
    }
    
    /* Header Gradient Text */
    .header-title {
        background: linear-gradient(to right, #a5b4fc, #818cf8, #6366f1);
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

# Display active API Key alert if missing
api_key_set = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key_set:
    st.sidebar.warning("⚠️ API Key not found. Please set GEMINI_API_KEY in your environment or .env file.")

generate_button = st.sidebar.button("Generate Strategy")

# Import execution logic
from main_workflow import run_portfolio_workflow

if generate_button:
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
                
                # Render in main column inside premium glassmorphic card container
                st.markdown('<div class="report-card">', unsafe_allow_html=True)
                if report.strip():
                    st.markdown(report)
                else:
                    st.error("No report output was generated by the Strategist Agent. Please check the terminal logs.")
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
else:
    # Default landing UI
    st.info("Configure your portfolio allocation in the sidebar and click **Generate Strategy** to trigger the multi-agent workflow.")
