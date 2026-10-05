import os
import sys
import streamlit as st

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


def apply_custom_theme():
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
    
    <style>
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #0F172A;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Space Grotesk', sans-serif !important;
            letter-spacing: -0.025em;
            font-weight: 700;
        }

        :root {
            --primary: #4F46E5;
            --primary-dark: #3730A3;
            --surface-card: #FFFFFF;
            --border-subtle: #E2E8F0;
            --card-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.05), 0 8px 10px -6px rgba(15, 23, 42, 0.03);
            --card-shadow-hover: 0 20px 30px -10px rgba(79, 70, 229, 0.15);
        }

        /* Hero Container */
        .premium-hero {
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.06) 0%, rgba(236, 72, 153, 0.06) 50%, rgba(6, 182, 212, 0.06) 100%);
            border: 1px solid rgba(79, 70, 229, 0.15);
            border-radius: 20px;
            padding: 28px 32px;
            margin-bottom: 24px;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.03);
        }

        .gradient-heading {
            background: linear-gradient(135deg, #1E1B4B 0%, #4F46E5 50%, #7C3AED 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }

        /* KPI Metric Container */
        .kpi-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px;
            border-radius: 16px;
            background: #FFFFFF;
            border: 1px solid var(--border-subtle);
            box-shadow: var(--card-shadow);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            height: 105px;
            box-sizing: border-box;
        }
        .kpi-container:hover {
            transform: translateY(-3px);
            box-shadow: var(--card-shadow-hover);
            border-color: #CBD5E1;
        }

        .kpi-indigo { border-left: 5px solid #4F46E5; }
        .kpi-cyan { border-left: 5px solid #0891B2; }
        .kpi-emerald { border-left: 5px solid #059669; }
        .kpi-amber { border-left: 5px solid #D97706; }

        .kpi-title {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #64748B;
            margin-bottom: 6px;
        }

        .kpi-number {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.85rem;
            font-weight: 800;
            color: #0F172A;
            line-height: 1.1;
        }

        .kpi-icon-badge {
            width: 48px;
            height: 48px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
        }
        .icon-indigo { background: rgba(79, 70, 229, 0.1); color: #4F46E5; }
        .icon-cyan { background: rgba(8, 145, 178, 0.1); color: #0891B2; }
        .icon-emerald { background: rgba(5, 150, 105, 0.1); color: #059669; }
        .icon-amber { background: rgba(217, 119, 6, 0.1); color: #D97706; }

        /* Badge Tokens */
        .pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
        .pill-admin { background: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }
        .pill-manager { background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; }
        .pill-staff { background: #E0E7FF; color: #3730A3; border: 1px solid #C7D2FE; }
        .pill-active { background: #DCFCE7; color: #166534; border: 1px solid #86EFAC; }
        .pill-inactive { background: #F1F5F9; color: #64748B; border: 1px solid #CBD5E1; }
        .pill-auth { background: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD; }
        .pill-prod { background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }
        .pill-user { background: #F3E8FF; color: #6B21A8; border: 1px solid #E9D5FF; }

        /* Unified Workspace Action Cards */
        .module-card {
            background: #FFFFFF;
            border: 1px solid var(--border-subtle);
            border-radius: 18px;
            padding: 22px;
            box-shadow: var(--card-shadow);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 250px;
            box-sizing: border-box;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 12px;
        }
        .module-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--card-shadow-hover);
            border-color: #818CF8;
        }

        .module-card p {
            min-height: 54px;
            line-height: 1.45;
            margin-top: 6px;
            margin-bottom: 12px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
        }

        /* Sidebar Identity Unit */
        .sidebar-card {
            background: linear-gradient(135deg, #1E1B4B 0%, #0F172A 100%);
            color: #FFFFFF;
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.3);
        }

        /* Streamlit Element Overrides */
        div[data-testid="stForm"] {
            background: #FFFFFF;
            border-radius: 16px;
            padding: 24px;
            border: 1px solid var(--border-subtle);
            box-shadow: var(--card-shadow);
        }

        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.5rem 1.25rem;
            transition: all 0.2s ease;
        }

        [data-testid="stDataFrame"] {
            border-radius: 12px;
            border: 1px solid var(--border-subtle);
            box-shadow: var(--card-shadow);
        }
    </style>
    """, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str, badge: str = "Enterprise Engine"):
    st.markdown(f"""
    <div class="premium-hero">
        <div style="margin-bottom: 8px;">
            <span class="pill-badge pill-staff">⚡ {badge}</span>
        </div>
        <h1 style="font-size: 2.2rem; margin: 0 0 8px 0;">
            <span class="gradient-heading">{title}</span>
        </h1>
        <p style="font-size: 1rem; color: #64748B; margin: 0; font-weight: 500;">
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_kpi(title: str, value: str, icon: str, color_scheme: str = "indigo", subtitle: str = ""):
    st.markdown(f"""
    <div class="kpi-container kpi-{color_scheme}">
        <div>
            <div class="kpi-title">{title}</div>
            <div class="kpi-number">{value}</div>
            {f'<div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">{subtitle}</div>' if subtitle else ''}
        </div>
        <div class="kpi-icon-badge icon-{color_scheme}">
            {icon}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        user = st.session_state.get("user")
        if user:
            role = str(user.get("role", "staff")).lower()
            uname = user.get("username") or "User"
            initial = uname[0].upper()
            
            st.markdown(f"""
            <div class="sidebar-card">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                    <div style="width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, #4F46E5, #EC4899); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.25rem;">
                        {initial}
                    </div>
                    <div style="overflow: hidden;">
                        <div style="font-weight: 700; font-size: 1.05rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{uname}</div>
                        <div style="font-size: 0.75rem; color: #94A3B8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{user.get('email', '')}</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1);">
                    <span style="font-size: 0.75rem; color: #94A3B8;">PRIVILEGE</span>
                    <span class="pill-badge pill-{role}">{role.upper()}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Sign Out", use_container_width=True):
                st.session_state.clear()
                st.switch_page("app.py")
            st.write("---")
