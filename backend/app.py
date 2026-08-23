from src import create_app

# Build the Flask app through the shared factory so blueprints and config load once.
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
