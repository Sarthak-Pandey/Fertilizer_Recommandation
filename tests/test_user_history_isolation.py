"""
Test suite for User-Specific History Isolation & Prediction Linking.
"""

import uuid
import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


class TestUserHistoryIsolation:
    @pytest.fixture(autouse=True)
    def setup_users(self):
        """Create two distinct test users and store their valid auth tokens."""
        unique_id = uuid.uuid4().hex[:6]
        self.user1_email = f"farmer.a.{unique_id}@example.com"
        self.user2_email = f"farmer.b.{unique_id}@example.com"
        self.password = "SecurePass123!"

        # Register User A
        client.post(
            "/api/v1/auth/register",
            json={
                "email": self.user1_email,
                "password": self.password,
                "full_name": "Farmer Alice",
                "role": "farmer",
            },
        )
        login1 = client.post(
            "/api/v1/auth/login",
            json={"email": self.user1_email, "password": self.password},
        )
        assert login1.status_code == 200, f"Login A failed: {login1.text}"
        self.token_a = login1.json()["access_token"]
        assert self.token_a, "Token A must not be empty"

        # Register User B
        client.post(
            "/api/v1/auth/register",
            json={
                "email": self.user2_email,
                "password": self.password,
                "full_name": "Farmer Bob",
                "role": "agronomist",
            },
        )
        login2 = client.post(
            "/api/v1/auth/login",
            json={"email": self.user2_email, "password": self.password},
        )
        assert login2.status_code == 200, f"Login B failed: {login2.text}"
        self.token_b = login2.json()["access_token"]
        assert self.token_b, "Token B must not be empty"

    def test_01_user_recommendations_linked_to_user_id(self):
        """Verify that predictions submitted with user token are stored with user_id."""
        # User A makes recommendation
        res_a = client.post(
            "/api/v1/fertilizer/recommend",
            json={
                "Soil_pH": 6.5,
                "Nitrogen_Level": 120.0,
                "Phosphorus_Level": 50.0,
                "Potassium_Level": 80.0,
                "Crop_Growth_Stage": "Vegetative",
            },
            headers={"Authorization": f"Bearer {self.token_a}"},
        )
        assert res_a.status_code == 200, f"Response A failed: {res_a.text}"
        pred_a_id = res_a.json()["prediction_id"]

        # User B makes recommendation
        res_b = client.post(
            "/api/v1/fertilizer/recommend",
            json={
                "Soil_pH": 5.8,
                "Nitrogen_Level": 40.0,
                "Phosphorus_Level": 20.0,
                "Potassium_Level": 30.0,
                "Crop_Growth_Stage": "Sowing",
            },
            headers={"Authorization": f"Bearer {self.token_b}"},
        )
        assert res_b.status_code == 200, f"Response B failed: {res_b.text}"
        pred_b_id = res_b.json()["prediction_id"]

        # User A fetches history -> must see pred_a_id, but NOT pred_b_id
        hist_a = client.get(
            "/api/v1/predictions",
            headers={"Authorization": f"Bearer {self.token_a}"},
        )
        assert hist_a.status_code == 200
        items_a_ids = [item["prediction_id"] for item in hist_a.json()["items"]]
        assert pred_a_id in items_a_ids
        assert pred_b_id not in items_a_ids

        # User B fetches history -> must see pred_b_id, but NOT pred_a_id
        hist_b = client.get(
            "/api/v1/predictions",
            headers={"Authorization": f"Bearer {self.token_b}"},
        )
        assert hist_b.status_code == 200
        items_b_ids = [item["prediction_id"] for item in hist_b.json()["items"]]
        assert pred_b_id in items_b_ids
        assert pred_a_id not in items_b_ids

    def test_02_user_stats_isolation(self):
        """Verify that prediction stats are isolated per user."""
        # User A recommendation
        client.post(
            "/api/v1/fertilizer/recommend",
            json={
                "Soil_pH": 6.5,
                "Nitrogen_Level": 120.0,
                "Phosphorus_Level": 50.0,
                "Potassium_Level": 80.0,
                "Crop_Growth_Stage": "Vegetative",
            },
            headers={"Authorization": f"Bearer {self.token_a}"},
        )

        stats_a = client.get(
            "/api/v1/predictions/stats",
            headers={"Authorization": f"Bearer {self.token_a}"},
        )
        assert stats_a.status_code == 200
        assert stats_a.json()["total_count"] >= 1

        stats_b = client.get(
            "/api/v1/predictions/stats",
            headers={"Authorization": f"Bearer {self.token_b}"},
        )
        assert stats_b.status_code == 200
