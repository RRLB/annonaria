# run.py
# Entry point for the Annonaria backend Flask application.
# This script initializes the Flask app and starts the development server.

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)