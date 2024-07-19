# src/main.py
from backend.app import create_app
import webbrowser
import threading
from threading import Timer
import os

app = create_app()

# Global variable to track if the browser has been opened
browser_opened = False

def open_browser():
    try:
        # Get the first available web browser
        browser = webbrowser.get()

        # Open the URL in the browser
        browser.open('http://127.0.0.1:5000/')
    except Exception as e:
        print(f"Failed to open browser: {e}")

if __name__ == '__main__':
    # Check if the script is running in the main process
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        threading.Timer(1, open_browser).start()  
    app.run(debug=True)