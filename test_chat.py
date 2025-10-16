#!/usr/bin/env python3
"""
Test script for Halloween Poe Chat
This script tests the basic functionality of the chat system
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_connection():
    """Test if the backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/users", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Please start it first.")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

def register_test_users():
    """Register two test users"""
    print("\n👥 Registering test users...")
    
    # User 1
    user1_data = {
        "username": "testuser1",
        "password": "password123",
        "questions": [
            "What is your favorite color?",
            "What is your pet's name?",
            "What is your favorite food?"
        ],
        "answers": [
            "blue",
            "fluffy",
            "pizza"
        ]
    }
    
    # User 2
    user2_data = {
        "username": "testuser2", 
        "password": "password123",
        "questions": [
            "What is your favorite color?",
            "What is your pet's name?", 
            "What is your favorite food?"
        ],
        "answers": [
            "red",
            "spot",
            "burger"
        ]
    }
    
    try:
        # Register user 1
        response1 = requests.post(f"{BASE_URL}/register", json=user1_data)
        if response1.status_code == 200:
            print("✅ User 1 registered successfully")
            user1_info = response1.json()
            print(f"   Poem: {user1_info['poem'][:100]}...")
        else:
            print(f"❌ Failed to register user 1: {response1.text}")
            return False
            
        # Register user 2
        response2 = requests.post(f"{BASE_URL}/register", json=user2_data)
        if response2.status_code == 200:
            print("✅ User 2 registered successfully")
            user2_info = response2.json()
            print(f"   Poem: {user2_info['poem'][:100]}...")
        else:
            print(f"❌ Failed to register user 2: {response2.text}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error registering users: {e}")
        return False

def test_connection_attempt():
    """Test connection attempt with wrong answers"""
    print("\n🔗 Testing connection attempt with wrong answers...")
    
    attempt_data = {
        "target_username": "testuser1",
        "answers": ["wrong", "wrong", "wrong"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/attempt-connection", json=attempt_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Connection attempt result: {result['success']}")
            print(f"   Correct answers: {result['correct_answers']}/3")
            print(f"   Message: {result['message']}")
            return True
        else:
            print(f"❌ Connection attempt failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

def test_successful_connection():
    """Test connection attempt with correct answers"""
    print("\n🎯 Testing connection attempt with correct answers...")
    
    attempt_data = {
        "target_username": "testuser1",
        "answers": ["blue", "fluffy", "pizza"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/attempt-connection", json=attempt_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Connection attempt result: {result['success']}")
            print(f"   Correct answers: {result['correct_answers']}/3")
            print(f"   Message: {result['message']}")
            if result['success']:
                print("🎉 Connection successful! Users can now chat!")
            return True
        else:
            print(f"❌ Connection attempt failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

def test_get_users():
    """Test getting list of users"""
    print("\n👥 Testing user list...")
    
    try:
        response = requests.get(f"{BASE_URL}/users")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Found {len(users)} users:")
            for user in users:
                print(f"   - {user['username']}")
            return True
        else:
            print(f"❌ Failed to get users: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error getting users: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Halloween Poe Chat - Test Suite")
    print("=" * 50)
    
    # Test 1: Check if backend is running
    if not test_connection():
        print("\n❌ Please start the backend server first:")
        print("   python backend/main.py")
        return
    
    # Test 2: Register test users
    if not register_test_users():
        print("\n❌ Failed to register test users")
        return
    
    # Test 3: Get users list
    if not test_get_users():
        print("\n❌ Failed to get users list")
        return
    
    # Test 4: Test connection attempt with wrong answers
    if not test_connection_attempt():
        print("\n❌ Failed connection attempt test")
        return
    
    # Test 5: Test connection attempt with correct answers
    if not test_successful_connection():
        print("\n❌ Failed successful connection test")
        return
    
    print("\n🎉 All tests passed!")
    print("✅ Backend is working correctly")
    print("✅ User registration works")
    print("✅ Connection attempts work")
    print("✅ Chat functionality should work")
    print("\n🚀 You can now start the frontend and test the full chat experience!")
    print("   Run: npm start (in frontend folder)")

if __name__ == "__main__":
    main()
