"""
Automated Test Suite for Backend User Authentication & Registration (Supabase).

Tests:
- User Registration (POST /api/v1/auth/register)
- User Login (POST /api/v1/auth/login)
- Invalid Credentials Handling
- Protected Profile Endpoint (GET /api/v1/auth/me)
- User Logout (POST /api/v1/auth/logout)

Run with:
    pytest tests/test_auth_api.py -v
"""

import uuid
import httpx
import pytest

BACKEND_URL = "http://localhost:8000"
API_KEY = "dev-secret-key-123"

# Unique test credentials
TEST_EMAIL = f"test.farmer.{uuid.uuid4().hex[:8]}@gmail.com"
TEST_PASSWORD = "StrongSecurePassword123!"
TEST_FULL_NAME = "Sarthak Pandey"
TEST_ORGANIZATION = "Green Valley Farms"


@pytest.fixture(scope="module")
def http_client():
    with httpx.Client(timeout=10.0) as client:
        yield client


class TestAuthAPI:
    """Test suite for Supabase-backed user authentication APIs."""

    def test_01_user_registration(self, http_client):
        """Test POST /api/v1/auth/register with valid user details."""
        payload = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "full_name": TEST_FULL_NAME,
            "role": "farmer",
            "organization": TEST_ORGANIZATION,
        }
        r = http_client.post(f"{BACKEND_URL}/api/v1/auth/register", json=payload)
        assert r.status_code in (200, 201), f"Registration failed with status {r.status_code}: {r.text}"
        data = r.json()

        assert "user" in data, "Missing 'user' field in registration response"
        user_info = data["user"]
        assert user_info["email"] == TEST_EMAIL
        assert user_info["full_name"] == TEST_FULL_NAME
        assert user_info["role"] == "farmer"
        assert user_info["organization"] == TEST_ORGANIZATION
        assert "id" in user_info and len(user_info["id"]) > 0

    def test_02_user_login_success(self, http_client):
        """Test POST /api/v1/auth/login with valid credentials."""
        payload = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        }
        r = http_client.post(f"{BACKEND_URL}/api/v1/auth/login", json=payload)
        assert r.status_code == 200, f"Login failed with status {r.status_code}: {r.text}"
        data = r.json()

        assert "access_token" in data, "Missing 'access_token' in login response"
        assert len(data["access_token"]) > 10
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == TEST_EMAIL

    def test_03_user_login_invalid_password(self, http_client):
        """Test POST /api/v1/auth/login with incorrect password returns 401."""
        payload = {
            "email": TEST_EMAIL,
            "password": "WrongPassword999!",
        }
        r = http_client.post(f"{BACKEND_URL}/api/v1/auth/login", json=payload)
        assert r.status_code == 401, f"Expected 401 for wrong password, got {r.status_code}"

    def test_04_get_current_user_profile(self, http_client):
        """Test GET /api/v1/auth/me using Bearer JWT token."""
        # 1. Login to get fresh access token
        login_res = http_client.post(
            f"{BACKEND_URL}/api/v1/auth/login",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
        )
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]

        # 2. Access protected profile endpoint
        headers = {"Authorization": f"Bearer {token}"}
        r = http_client.get(f"{BACKEND_URL}/api/v1/auth/me", headers=headers)
        assert r.status_code == 200, f"Get profile failed with status {r.status_code}: {r.text}"
        profile = r.json()

        assert profile["email"] == TEST_EMAIL
        assert profile["full_name"] == TEST_FULL_NAME
        assert profile["organization"] == TEST_ORGANIZATION

    def test_05_protected_route_without_token(self, http_client):
        """Test GET /api/v1/auth/me without Authorization header returns 401."""
        r = http_client.get(f"{BACKEND_URL}/api/v1/auth/me")
        assert r.status_code == 401

    def test_06_logout(self, http_client):
        """Test POST /api/v1/auth/logout with Bearer token."""
        login_res = http_client.post(
            f"{BACKEND_URL}/api/v1/auth/login",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
        )
        token = login_res.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        r = http_client.post(f"{BACKEND_URL}/api/v1/auth/logout", headers=headers)
        assert r.status_code == 200
        data = r.json()
        assert data["success"] is True
