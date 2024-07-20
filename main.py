import os
from dotenv import load_dotenv
import webbrowser
import threading
from src.app_factory import create_app

# Load environment variables from .env file
load_dotenv()

app = create_app()

def open_browser():
    try:
        webbrowser.open('http://127.0.0.1:5000/')
    except Exception as e:
        print(f"Failed to open browser: {e}")

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        threading.Timer(1, open_browser).start()
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, use_reloader=True, use_debugger=True)