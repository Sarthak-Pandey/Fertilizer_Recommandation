"""
Supabase Authentication Service.

Handles user signup, signin, token management, and profile retrieval.
"""

import logging
from typing import Any, Dict, Optional
from supabase import Client, create_client
from backend.config import settings

logger = logging.getLogger("backend.services.auth")


class AuthService:
    """Service wrapping Supabase Auth and database operations."""

    def __init__(self):
        self._client: Optional[Client] = None

    @property
    def client(self) -> Client:
        if self._client is None:
            if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be configured.")
            self._client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return self._client

    def register_user(
        self,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        role: str = "farmer",
        organization: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Register a new user in Supabase Auth."""
        user_metadata = {
            "full_name": full_name or "",
            "role": role or "farmer",
            "organization": organization or "",
        }

        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": user_metadata
                }
            })

            user = response.user
            session = response.session

            if user is None:
                raise ValueError("Failed to create user. Please check credentials or email verification settings.")

            created_user_id = str(user.id)
            logger.info("user_registered email=%s user_id=%s", email, created_user_id)

            profile = {
                "id": created_user_id,
                "email": user.email or email,
                "full_name": user_metadata["full_name"],
                "role": user_metadata["role"],
                "organization": user_metadata["organization"],
                "created_at": str(user.created_at) if user.created_at else None,
            }

            return {
                "access_token": session.access_token if session else "",
                "refresh_token": session.refresh_token if session else "",
                "token_type": "bearer",
                "user": profile,
            }
        except Exception as e:
            err_msg = str(e)
            logger.error("user_registration_failed email=%s error=%s", email, err_msg)
            raise ValueError(f"Registration failed: {err_msg}")

    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate existing user against Supabase Auth."""
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })

            user = response.user
            session = response.session

            if not user or not session:
                raise ValueError("Invalid email or password.")

            meta = user.user_metadata or {}
            profile = {
                "id": str(user.id),
                "email": user.email or email,
                "full_name": meta.get("full_name", ""),
                "role": meta.get("role", "farmer"),
                "organization": meta.get("organization", ""),
                "created_at": str(user.created_at) if user.created_at else None,
            }

            logger.info("user_logged_in email=%s user_id=%s", email, user.id)

            return {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "token_type": "bearer",
                "user": profile,
            }
        except Exception as e:
            err_msg = str(e)
            logger.warning("login_failed email=%s error=%s", email, err_msg)
            raise ValueError(f"Login failed: {err_msg}")

    def get_user_from_token(self, token: str) -> Dict[str, Any]:
        """Verify token with Supabase Auth and return user details."""
        try:
            response = self.client.auth.get_user(token)
            user = response.user
            if not user:
                raise ValueError("Invalid or expired token.")

            meta = user.user_metadata or {}
            return {
                "id": str(user.id),
                "email": user.email or "",
                "full_name": meta.get("full_name", ""),
                "role": meta.get("role", "farmer"),
                "organization": meta.get("organization", ""),
                "created_at": str(user.created_at) if user.created_at else None,
            }
        except Exception as e:
            logger.warning("token_verification_failed error=%s", e)
            raise ValueError("Invalid, expired, or unverified session token.")


auth_service = AuthService()
