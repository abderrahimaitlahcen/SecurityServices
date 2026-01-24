#!/usr/bin/env python
import os
import sys
os.chdir(r"c:\Users\soufi\OneDrive\Documents\PYTHON\project_crypto")

print("Starting Flask app...")
print(f"Working dir: {os.getcwd()}")

try:
    from app import app
    print("[OK] App imported")
    
    print("\nAttempting to run Flask server...")
    print("Server should be running on http://127.0.0.1:5000")
    
    # Run for 120 seconds then exit
    app.run(debug=False, port=5000, use_reloader=False, threaded=True, host='127.0.0.1')
    
except KeyboardInterrupt:
    print("\nServer stopped by user")
except Exception as e:
    print(f"\n[ERROR]: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
