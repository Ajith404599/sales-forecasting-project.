import os
import sys
import streamlit as st
import pandas as pd

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from utils.api_client import APIClient, APIError
from utils.ui_theme import apply_custom_theme, render_hero, render_sidebar

st.set_page_config(page_title="User Profile & Identity", page_icon="👤", layout="wide")
apply_custom_theme()

# Authentication Guard: redirect directly to login page if token is missing
if not st.session_state.get("token"):
    st.switch_page("app.py")
    st.stop()

render_sidebar()

try:
    profile = APIClient.get_profile()
    st.session_state["user"] = profile
except Exception:
    profile = st.session_state.get("user", {})

user_role = str(profile.get("role", "staff")).lower()
is_admin = user_role == "admin"

render_hero(
    title="Profile & Identity Governance",
    subtitle="Manage your personal security credentials and administrative user privileges.",
    badge="IAM & Security"
)

c1, c2 = st.columns([1, 1.2])

with c1:
    st.markdown("### 🪪 Identity Card")
    role_class = f"pill-{user_role}"
    
    username_val = profile.get("username") or "User"
    initial_letter = username_val[0].upper()
    
    st.markdown(f"""
    <div style="background: #FFFFFF; border-radius: 16px; padding: 24px; border: 1px solid #E2E8F0; box-shadow: var(--card-shadow); margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 18px;">
            <div style="width: 56px; height: 56px; border-radius: 18px; background: linear-gradient(135deg, #6366F1, #EC4899); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.5rem; color: #FFFFFF; box-shadow: 0 8px 16px -4px rgba(99, 102, 241, 0.4);">
                {initial_letter}
            </div>
            <div>
                <h3 style="margin: 0; font-size: 1.35rem; color: #0F172A;">{username_val}</h3>
                <span class="pill-badge {role_class}">{profile.get('role', 'staff').upper()}</span>
            </div>
        </div>
        <div style="border-top: 1px solid #F1F5F9; padding-top: 14px; font-size: 0.9rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748B;">Email Address:</span>
                <span style="font-weight: 600; color: #1E293B;">{profile.get('email', 'N/A')}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748B;">Account Status:</span>
                <span class="pill-badge {'pill-active' if profile.get('is_active') else 'pill-inactive'}">
                    {'🟢 ACTIVE' if profile.get('is_active') else '🔴 INACTIVE'}
                </span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #64748B;">User ID:</span>
                <span style="font-weight: 600; color: #1E293B;">#{profile.get('user_id', '-')}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔑 Change Password & Contact Details", expanded=False):
        with st.form("update_profile_form"):
            st.markdown("##### 🔐 Security Settings")
            new_email = st.text_input("Email", value=profile.get("email", ""))
            current_pwd = st.text_input("Current Password", type="password", help="Required to authorize changes")
            new_pwd = st.text_input("New Password", type="password")
            confirm_pwd = st.text_input("Confirm New Password", type="password")
            
            save_profile_btn = st.form_submit_button("💾 Save Credentials", use_container_width=True)

            if save_profile_btn:
                update_payload = {}
                if new_email and new_email != profile.get("email"):
                    update_payload["email"] = new_email
                if new_pwd:
                    if new_pwd != confirm_pwd:
                        st.error("New password confirmation mismatch.")
                    elif not current_pwd:
                        st.error("Current password is required to update security credentials.")
                    else:
                        update_payload["current_password"] = current_pwd
                        update_payload["new_password"] = new_pwd

                if update_payload:
                    try:
                        updated_user = APIClient.update_profile(update_payload)
                        st.session_state["user"] = updated_user
                        st.success("🎉 Security settings updated successfully!")
                        st.rerun()
                    except APIError as e:
                        st.error(f"Update failed: {e.message}")
                else:
                    st.info("No modifications detected.")

with c2:
    if is_admin:
        st.markdown("### 👥 Administrator User Management")
        
        with st.expander("✨ + Provision New User Account", expanded=False):
            with st.form("admin_create_user_form"):
                st.markdown("##### Account Details")
                a1, a2 = st.columns(2)
                with a1:
                    admin_new_username = st.text_input("Username *", placeholder="jane_doe")
                    admin_new_email = st.text_input("Email Address *", placeholder="jane@company.com")
                with a2:
                    admin_new_pwd = st.text_input("Initial Password *", type="password")
                    admin_new_role = st.selectbox("Assigned Role", ["staff", "manager", "admin"])
                admin_new_active = st.checkbox("Account Active Status", value=True)
                
                create_user_btn = st.form_submit_button("🚀 Provision Account", use_container_width=True)
                if create_user_btn:
                    if not admin_new_username or not admin_new_email or not admin_new_pwd:
                        st.error("All marked fields are mandatory.")
                    else:
                        try:
                            APIClient.create_user({
                                "username": admin_new_username,
                                "email": admin_new_email,
                                "password": admin_new_pwd,
                                "role": admin_new_role,
                                "is_active": admin_new_active
                            })
                            st.success(f"✨ User '{admin_new_username}' created successfully!")
                            st.rerun()
                        except APIError as e:
                            st.error(f"Creation failed: {e.message}")

if is_admin:
    st.write("---")
    st.markdown("### 📋 Enterprise Directory Matrix")
    try:
        users_list = APIClient.get_users()
        if users_list:
            df_users = pd.DataFrame(users_list)
            
            # Ensure expected columns exist
            for col in ["user_id", "username", "email", "role", "is_active", "created_at"]:
                if col not in df_users.columns:
                    df_users[col] = None

            df_users_display = df_users[["user_id", "username", "email", "role", "is_active", "created_at"]].copy()
            df_users_display["role"] = df_users_display["role"].astype(str).str.upper()
            df_users_display["is_active"] = df_users_display["is_active"].apply(lambda x: "🟢 Active" if x else "🔴 Inactive")
            df_users_display.columns = ["ID", "Username", "Email", "Role", "Status", "Joined"]
            st.dataframe(df_users_display, use_container_width=True, hide_index=True)

            st.markdown("#### ⚙️ Edit User Roles & Reset Passwords")
            for u in users_list:
                roles = ["admin", "manager", "staff"]
                curr_role = str(u.get('role', 'staff')).lower()
                r_idx = roles.index(curr_role) if curr_role in roles else 2
                with st.expander(f"User #{u['user_id']} — {u['username']} ({curr_role.upper()})", expanded=False):
                    with st.form(f"edit_user_{u['user_id']}"):
                        e_email = st.text_input("Email", value=u.get('email', ''), key=f"eu_e_{u['user_id']}")
                        e_role = st.selectbox("Role", roles, index=r_idx, key=f"eu_r_{u['user_id']}")
                        e_active = st.checkbox("Active Status", value=bool(u.get('is_active', True)), key=f"eu_a_{u['user_id']}")
                        e_pwd = st.text_input("Reset Password (leave empty to keep unchanged)", type="password", key=f"eu_p_{u['user_id']}")
                        
                        save_u_btn = st.form_submit_button("💾 Save User Permissions", use_container_width=True)
                        if save_u_btn:
                            payload = {"email": e_email, "role": e_role, "is_active": e_active}
                            if e_pwd:
                                payload["password"] = e_pwd
                            try:
                                APIClient.update_user(u['user_id'], payload)
                                st.success(f"User '{u['username']}' updated successfully!")
                                st.rerun()
                            except APIError as e:
                                st.error(e.message)
    except Exception as e:
        st.error(f"Failed to fetch user directory: {e}")