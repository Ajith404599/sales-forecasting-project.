import os
import sys
import streamlit as st

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from utils.api_client import APIClient, APIError
from utils.ui_theme import apply_custom_theme, render_hero, render_kpi, render_sidebar

st.set_page_config(
    page_title="Retail Intelligence Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_theme()

if "token" not in st.session_state:
    st.session_state["token"] = None
if "user" not in st.session_state:
    st.session_state["user"] = None


def login_screen():
    _, col, _ = st.columns([1, 1.8, 1])
    with col:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 28px; padding-top: 20px;">
            <div style="display: inline-flex; width: 68px; height: 68px; border-radius: 22px; background: linear-gradient(135deg, #4F46E5, #EC4899); align-items: center; justify-content: center; font-size: 2.2rem; box-shadow: 0 12px 30px -8px rgba(79, 70, 229, 0.45); margin-bottom: 14px;">
                ⚡
            </div>
            <h1 style="font-size: 2.4rem; margin-bottom: 6px; letter-spacing: -0.03em;">Retail Enterprise OS</h1>
            <p style="color: #64748B; font-size: 1rem;">Unified Management Portal & Predictive Analytics Hub</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("#### 🔐 Authenticate Account")
            username = st.text_input("Username or Account Email", placeholder="admin@store.com")
            password = st.text_input("Password", type="password", placeholder="••••••••••••")
            
            submit = st.form_submit_button("🚀 Launch Workspace", use_container_width=True)

            if submit:
                if not username.strip() or not password.strip():
                    st.error("Please supply valid account credentials.")
                else:
                    try:
                        result = APIClient.login(username.strip(), password.strip())
                        st.session_state["token"] = result["access_token"]
                        st.session_state["user"] = result["user"]
                        st.toast("Authenticated successfully!", icon="✅")
                        st.rerun()
                    except APIError as e:
                        st.error(f"Authentication failed: {e.message}")
                    except Exception as e:
                        st.error(f"Cannot connect to API service: {e}")

        st.markdown("""
        <div style="background: #FFFFFF; border-radius: 14px; padding: 16px 20px; border: 1px dashed #CBD5E1; margin-top: 20px;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">
                Quick Verification Accounts
            </div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap; font-size: 0.8rem;">
                <span class="pill-badge pill-admin">Admin: admin@store.com / adminpassword123</span>
                <span class="pill-badge pill-manager">Manager: alex.manager@store.com / managerpassword123</span>
                <span class="pill-badge pill-staff">Staff: emma.staff@store.com / staffpassword123</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


if not st.session_state.get("token"):
    login_screen()
else:
    render_sidebar()
    user = st.session_state.get("user") or {}
    uname = user.get("username", "Partner")
    
    render_hero(
        title=f"Command Center — Welcome, {uname} 👋",
        subtitle="Real-time operational dashboard for catalog health, sales velocity, and audit compliance.",
        badge="Live Telemetry"
    )

    try:
        summary = APIClient.get_analytics_summary()
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_kpi("Gross Revenue", f"${summary.get('total_revenue', 0.0):,.2f}", "💎", "indigo", "All-time processed revenue")
        with c2:
            render_kpi("Total Orders", f"{summary.get('total_sales_count', 0):,}", "📦", "cyan", "Validated customer checkouts")
        with c3:
            render_kpi("Avg Ticket Value", f"${summary.get('average_order_value', 0.0):,.2f}", "📈", "emerald", "Mean cart valuation")
        with c4:
            render_kpi("Active Catalog", f"{summary.get('active_products_count', 0)} Items", "🏷️", "amber", "Available for retail dispatch")
    except Exception as e:
        st.warning(f"Telemetry metrics temporarily unavailable: {e}")

    st.write("---")
    st.markdown("### 🧭 Interactive Workspaces")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown("""
        <div class="module-card">
            <div>
                <span style="font-size: 2.2rem;">📦</span>
                <h4 style="margin: 10px 0 6px 0; color: #1E293B;">Product Hub</h4>
                <p style="font-size: 0.85rem; color: #64748B; margin: 0 0 14px 0;">
                    Manage active items, adjust unit base pricing, catalog taxonomies, and live inventory.
                </p>
            </div>
            <span class="pill-badge pill-prod" style="width: fit-content;">INVENTORY MGMT</span>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Open Catalog →", key="nav_prod_btn", use_container_width=True):
            st.switch_page("pages/1_Products.py")

    with m2:
        st.markdown("""
        <div class="module-card">
            <div>
                <span style="font-size: 2.2rem;">📊</span>
                <h4 style="margin: 10px 0 6px 0; color: #1E293B;">Sales BI</h4>
                <p style="font-size: 0.85rem; color: #64748B; margin: 0 0 14px 0;">
                    Interactive revenue curves, monthly trends, Pareto rankings, and price elasticity scatter views.
                </p>
            </div>
            <span class="pill-badge pill-staff" style="width: fit-content;">EXECUTIVE BI</span>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Open Analytics →", key="nav_bi_btn", use_container_width=True):
            st.switch_page("pages/2_Analytics.py")

    with m3:
        st.markdown("""
        <div class="module-card">
            <div>
                <span style="font-size: 2.2rem;">👤</span>
                <h4 style="margin: 10px 0 6px 0; color: #1E293B;">Identity & RBAC</h4>
                <p style="font-size: 0.85rem; color: #64748B; margin: 0 0 14px 0;">
                    Security credentials, personal encryption tokens, and administrative role assignments.
                </p>
            </div>
            <span class="pill-badge pill-user" style="width: fit-content;">SECURITY GOVERNANCE</span>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Open Identity →", key="nav_iam_btn", use_container_width=True):
            st.switch_page("pages/3_Profile.py")

    with m4:
        st.markdown("""
        <div class="module-card">
            <div>
                <span style="font-size: 2.2rem;">📜</span>
                <h4 style="margin: 10px 0 6px 0; color: #1E293B;">Audit Records</h4>
                <p style="font-size: 0.85rem; color: #64748B; margin: 0 0 14px 0;">
                    Chronological compliance logging, mutation detection, and security access trails.
                </p>
            </div>
            <span class="pill-badge pill-auth" style="width: fit-content;">COMPLIANCE TRAIL</span>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Open Audit Logs →", key="nav_audit_btn", use_container_width=True):
            st.switch_page("pages/4_Audit_Logs.py")