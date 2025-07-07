"""
Test that all fixtures work correctly
"""
import pytest

@pytest.mark.mysql
def test_all_fixtures_working(app, client, clean_db, sample_user, admin_user, user_token, admin_token, auth_headers):
    """Test that all fixtures are available and working"""
    
    # Test app fixture
    assert app is not None
    assert app.config['TESTING'] is True
    print("✅ App fixture works")
    
    # Test client fixture
    assert client is not None
    print("✅ Client fixture works")
    
    # Test database fixture
    assert clean_db is not None
    print("✅ Database fixture works")
    
    # Test user fixtures
    assert sample_user is not None
    assert sample_user.email == "pytest.user@mysql.test"
    print(f"✅ Sample user fixture works: {sample_user.email}")
    
    assert admin_user is not None
    assert admin_user.is_admin is True
    print(f"✅ Admin user fixture works: {admin_user.email}")
    
    # Test token fixtures
    assert user_token is not None
    assert len(user_token) > 10  # JWT tokens are long
    print("✅ User token fixture works")
    
    assert admin_token is not None
    assert len(admin_token) > 10
    print("✅ Admin token fixture works")
    
    # Test helper fixture
    headers = auth_headers(user_token)
    assert 'Authorization' in headers
    assert 'Bearer' in headers['Authorization']
    print("✅ Auth headers fixture works")
    
    print("🎉 All fixtures working correctly!")