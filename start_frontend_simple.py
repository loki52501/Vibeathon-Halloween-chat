#!/usr/bin/env python3
"""
Simple frontend startup script that works without npm
Uses a basic HTTP server to serve the frontend files
"""
import http.server
import socketserver
import os
import sys
import webbrowser
import threading
import time

def create_simple_frontend():
    """Create a simple HTML frontend that works without React"""
    print("Creating simple frontend...")
    
    # Create a simple HTML file
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Halloween Poe Chat - Simple Version</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(45deg, #0a0a0a, #1a0a0a, #0a0a1a);
            color: #fff;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }
        h1 {
            color: #ff0000;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        h2 {
            color: #ffd700;
            font-size: 1.5rem;
            margin-bottom: 2rem;
        }
        .message {
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #333;
            border-radius: 12px;
            padding: 2rem;
            margin: 2rem 0;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .success {
            border-color: #00ff00;
            color: #00ff00;
        }
        .warning {
            border-color: #ffd700;
            color: #ffd700;
        }
        .error {
            border-color: #ff0000;
            color: #ff0000;
        }
        .button {
            background: linear-gradient(45deg, #8B0000, #FF0000);
            border: 2px solid #FFD700;
            color: #fff;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 10px;
            transition: all 0.3s ease;
        }
        .button:hover {
            background: linear-gradient(45deg, #FF0000, #8B0000);
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
            transform: translateY(-2px);
        }
        .api-info {
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid #666;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            text-align: left;
        }
        .api-info h3 {
            color: #ffd700;
            margin-top: 0;
        }
        .api-info code {
            background: rgba(255, 255, 255, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎃 Halloween Poe Chat</h1>
        <h2>Simple Frontend Version</h2>
        
        <div class="message success">
            <h3>✅ Backend is Running!</h3>
            <p>The Halloween Poe Chat backend is successfully running on port 8000.</p>
            <p>This simple frontend allows you to test the API endpoints.</p>
        </div>
        
        <div class="message warning">
            <h3>⚠️ React Frontend Not Available</h3>
            <p>The full React frontend requires npm to be properly installed.</p>
            <p>Use this simple version to test the backend API.</p>
        </div>
        
        <div class="api-info">
            <h3>🔗 API Endpoints Available:</h3>
            <p><strong>API Documentation:</strong> <a href="http://localhost:8000/docs" target="_blank" style="color: #ffd700;">http://localhost:8000/docs</a></p>
            <p><strong>User Registration:</strong> <code>POST http://localhost:8000/register</code></p>
            <p><strong>Get Users:</strong> <code>GET http://localhost:8000/users</code></p>
            <p><strong>Attempt Connection:</strong> <code>POST http://localhost:8000/attempt-connection</code></p>
        </div>
        
        <div class="message">
            <h3>🧪 Test the API</h3>
            <p>You can test the API using:</p>
            <p>• <strong>Postman</strong> - Import the API from http://localhost:8000/docs</p>
            <p>• <strong>curl</strong> - Use command line tools</p>
            <p>• <strong>Python requests</strong> - Use the demo script</p>
        </div>
        
        <a href="http://localhost:8000/docs" target="_blank" class="button">
            📚 Open API Documentation
        </a>
        
        <a href="http://localhost:8000/users" target="_blank" class="button">
            👥 View Users
        </a>
        
        <div class="message">
            <h3>🔧 To Fix npm Issues:</h3>
            <p>1. Run: <code>python fix_npm_windows.py</code></p>
            <p>2. Or reinstall Node.js from <a href="https://nodejs.org/" target="_blank" style="color: #ffd700;">nodejs.org</a></p>
            <p>3. Make sure to check "Add to PATH" during installation</p>
        </div>
        
        <div class="message">
            <h3>🎮 Demo Script</h3>
            <p>Test the backend with: <code>python demo.py</code></p>
        </div>
    </div>
    
    <script>
        // Simple JavaScript to test API connectivity
        async function testAPI() {
            try {
                const response = await fetch('http://localhost:8000/users');
                if (response.ok) {
                    console.log('✅ API is working!');
                } else {
                    console.log('❌ API error:', response.status);
                }
            } catch (error) {
                console.log('❌ Cannot connect to API:', error);
            }
        }
        
        // Test API on page load
        testAPI();
    </script>
</body>
</html>
"""
    
    # Create the HTML file
    with open("frontend_simple.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("SUCCESS: Simple frontend created!")

def start_simple_server():
    """Start a simple HTTP server"""
    PORT = 3000
    
    # Change to the directory containing the HTML file
    os.chdir(".")
    
    # Create simple frontend
    create_simple_frontend()
    
    # Start HTTP server
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Simple Frontend Server starting on port {PORT}")
        print(f"📍 Open: http://localhost:{PORT}/frontend_simple.html")
        print("Press Ctrl+C to stop the server")
        
        # Open browser automatically
        def open_browser():
            time.sleep(1)
            webbrowser.open(f"http://localhost:{PORT}/frontend_simple.html")
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👻 Server stopped. Goodbye!")
            httpd.shutdown()

def main():
    print("Halloween Poe Chat - Simple Frontend")
    print("=" * 40)
    print("This creates a simple HTML frontend without npm/React")
    print("Perfect for testing the backend API")
    print()
    
    start_simple_server()

if __name__ == "__main__":
    main()
