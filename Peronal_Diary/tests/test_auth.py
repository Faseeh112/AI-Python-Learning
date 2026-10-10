"""
Auth Tests — registration, login, token refresh, password reset.
"""


class TestRegister:
    def test_register_success(self):
        # POST /api/auth/register with valid data → 201
        pass

    def test_register_duplicate_email(self):
        # POST /api/auth/register with existing email → 409
        pass

    def test_register_weak_password(self):
        # POST /api/auth/register with weak password → 400
        pass


class TestLogin:
    def test_login_success(self):
        # POST /api/auth/login with correct credentials → 200 + tokens
        pass

    def test_login_wrong_password(self):
        # POST /api/auth/login with wrong password → 401
        pass

    def test_login_nonexistent_user(self):
        # POST /api/auth/login with unknown email → 401
        pass


class TestTokenRefresh:
    def test_refresh_valid(self):
        # POST /api/auth/refresh with valid refresh token → 200 + new access token
        pass

    def test_refresh_expired(self):
        # POST /api/auth/refresh with expired token → 401
        pass
