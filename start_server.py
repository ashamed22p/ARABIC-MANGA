#!/usr/bin/env python3
import subprocess
import sys
import os

def main():
    """Start the FastAPI server using uvicorn"""
    # Change to the workspace directory
    os.chdir('/home/runner/workspace')
    
    # Start uvicorn with FastAPI app
    cmd = [
        sys.executable, '-m', 'uvicorn',
        'main:app',
        '--host', '0.0.0.0',
        '--port', '5000',
        '--reload'
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()