#!/usr/bin/env python3
"""
Demo script for Halloween Poe Chat
This script demonstrates the key features of the application
"""
import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_registration():
    """Test user registration"""
    print("🎃 Testing User Registration...")
    
    # Test user data
    user_data = {
        "username": "shadow_soul",
        "password": "mysterious123",
        "questions": [
            "What is your favorite gothic novel?",
            "What color represents your soul?",
            "What is your spirit animal?"
        ],
        "answers": [
            "Dracula",
            "Deep purple",
            "Raven"
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=user_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Registration successful!")
            print(f"User ID: {result['user_id']}")
            print(f"Generated Poem:\n{result['poem']}")
            return result['user_id']
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        return None

def test_user_list():
    """Test getting user list"""
    print("\n👻 Testing User List...")
    
    try:
        response = requests.get(f"{BASE_URL}/users")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Found {len(users)} users:")
            for user in users:
                print(f"  - {user['username']}")
            return users
        else:
            print(f"❌ Failed to get users: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error getting users: {e}")
        return []

def test_connection_attempt():
    """Test connection attempt"""
    print("\n🔮 Testing Connection Attempt...")
    
    # This would normally be done by another user
    attempt_data = {
        "target_username": "shadow_soul",
        "answers": [
            "Dracula",
            "Deep purple", 
            "Raven"
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/attempt-connection", json=attempt_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Connection attempt successful!")
            print(f"Success: {result['success']}")
            print(f"Correct answers: {result['correct_answers']}/3")
            print(f"Cryptic message: {result['cryptic_message']}")
            return result
        else:
            print(f"❌ Connection attempt failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error during connection attempt: {e}")
        return None

def main():
    print("🎃 Halloween Poe Chat - Demo Script")
    print("=" * 50)
    print("This script demonstrates the key API endpoints")
    print("Make sure the backend server is running on http://localhost:8000")
    print()
    
    # Test registration
    user_id = test_registration()
    if not user_id:
        print("❌ Cannot continue without successful registration")
        return
    
    # Wait a moment
    time.sleep(1)
    
    # Test user list
    users = test_user_list()
    
    # Wait a moment
    time.sleep(1)
    
    # Test connection attempt
    connection_result = test_connection_attempt()
    
    print("\n🎉 Demo completed!")
    print("\nTo test the full application:")
    print("1. Start the backend: python start_backend.py")
    print("2. Start the frontend: python start_frontend.py")
    print("3. Open http://localhost:3000 in your browser")
    print("4. Register multiple users and try connecting!")

if __name__ == "__main__":
    main()
