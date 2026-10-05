import os
import requests
import streamlit as st
from typing import Optional, Dict, Any, List

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class APIError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class APIClient:
    @staticmethod
    def _get_headers() -> Dict[str, str]:
        headers = {"Accept": "application/json"}
        token = st.session_state.get("token")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    @classmethod
    def _handle_response(cls, response: requests.Response) -> Any:
        try:
            data = response.json()
        except Exception:
            data = response.text

        if response.status_code == 401:
            st.session_state["token"] = None
            st.session_state["user"] = None
            raise APIError("Session expired or unauthorized. Please log in again.", 401)

        if not response.ok:
            detail = data.get("detail", str(data)) if isinstance(data, dict) else str(data)
            raise APIError(detail, response.status_code)

        return data

    @classmethod
    def login(cls, username: str, password: str) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/auth/token"
        response = requests.post(url, data={"username": username, "password": password})
        return cls._handle_response(response)

    @classmethod
    def refresh_token(cls, refresh_token: str) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/auth/refresh"
        response = requests.post(url, json={"refresh_token": refresh_token})
        return cls._handle_response(response)

    # Products API
    @classmethod
    def get_products(
        cls,
        category: Optional[str] = None,
        active_status: Optional[bool] = None,
        search: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        url = f"{API_BASE_URL}/products"
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if category and category != "All Categories":
            params["category"] = category
        if active_status is not None:
            params["active_status"] = "true" if active_status else "false"
        if search:
            params["search"] = search

        response = requests.get(url, headers=cls._get_headers(), params=params)
        return cls._handle_response(response)

    @classmethod
    def get_product(cls, product_id: int) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/products/{product_id}"
        response = requests.get(url, headers=cls._get_headers())
        return cls._handle_response(response)

    @classmethod
    def create_product(cls, product_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/products"
        response = requests.post(url, headers=cls._get_headers(), json=product_data)
        return cls._handle_response(response)

    @classmethod
    def update_product(cls, product_id: int, product_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/products/{product_id}"
        response = requests.put(url, headers=cls._get_headers(), json=product_data)
        return cls._handle_response(response)

    @classmethod
    def delete_product(cls, product_id: int) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/products/{product_id}"
        response = requests.delete(url, headers=cls._get_headers())
        return cls._handle_response(response)

    # Sales Transactions API
    @classmethod
    def record_sale(cls, sale_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/sales"
        response = requests.post(url, headers=cls._get_headers(), json=sale_data)
        return cls._handle_response(response)

    @classmethod
    def get_sales(cls, product_id: Optional[int] = None, limit: int = 50) -> List[Dict[str, Any]]:
        url = f"{API_BASE_URL}/sales"
        params: Dict[str, Any] = {"limit": limit}
        if product_id:
            params["product_id"] = product_id
        response = requests.get(url, headers=cls._get_headers(), params=params)
        return cls._handle_response(response)

    # Analytics API
    @classmethod
    def get_analytics_summary(cls) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/analytics/summary"
        response = requests.get(url, headers=cls._get_headers())
        return cls._handle_response(response)

    @classmethod
    def get_monthly_sales(cls) -> List[Dict[str, Any]]:
        url = f"{API_BASE_URL}/analytics/monthly"
        response = requests.get(url, headers=cls._get_headers())
        return cls._handle_response(response)

    @classmethod
    def get_products_analytics(cls, sort_by: str = "revenue_desc", limit: int = 20) -> List[Dict[str, Any]]:
        url = f"{API_BASE_URL}/analytics/products"
        params = {"sort_by": sort_by, "limit": limit}
        response = requests.get(url, headers=cls._get_headers(), params=params)
        return cls._handle_response(response)

    @classmethod
    def get_categories_analytics(cls) -> List[Dict[str, Any]]:
        url = f"{API_BASE_URL}/analytics/categories"
        response = requests.get(url, headers=cls._get_headers())
        return cls._handle_response(response)

    # Users & Profiles API
    @classmethod
    def get_profile(cls) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/profile"
        response = requests.get(url, headers=cls._get_headers())
        return cls._handle_response(response)

    @classmethod
    def update_profile(cls, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/profile"
        response = requests.put(url, headers=cls._get_headers(), json=profile_data)
        return cls._handle_response(response)

    @classmethod
    def get_users(cls, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        url = f"{API_BASE_URL}/users"
        response = requests.get(url, headers=cls._get_headers(), params={"limit": limit, "offset": offset})
        return cls._handle_response(response)

    @classmethod
    def create_user(cls, user_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/users"
        response = requests.post(url, headers=cls._get_headers(), json=user_data)
        return cls._handle_response(response)

    @classmethod
    def update_user(cls, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/users/{user_id}"
        response = requests.put(url, headers=cls._get_headers(), json=user_data)
        return cls._handle_response(response)

    # Audit Logs API
    @classmethod
    def get_audit_logs(
        cls,
        user_id: Optional[int] = None,
        module: Optional[str] = None,
        action: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        url = f"{API_BASE_URL}/audit-logs"
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if user_id:
            params["user_id"] = user_id
        if module and module != "All":
            params["module"] = module
        if action and action != "All":
            params["action"] = action
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        response = requests.get(url, headers=cls._get_headers(), params=params)
        return cls._handle_response(response)
    @classmethod
    def ask_ai_copilot(cls, question: str) -> Dict[str, Any]:
        url = f"{API_BASE_URL}/ai/query"
        response = requests.post(url, headers=cls._get_headers(), json={"question": question})
        return cls._handle_response(response)