from flask import Flask
from flask_cors import CORS
from routes.sparql import sparql_endpoint
from routes.search import semantic_search
from routes.test import json_endpoint

app = Flask(__name__)

# Configurar CORS para permitir solicitudes desde cualquier origen (puedes especificar un dominio en origins)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Registrar los blueprints
app.register_blueprint(sparql_endpoint, url_prefix="/sparql")
app.register_blueprint(semantic_search, url_prefix="/search")
app.register_blueprint(json_endpoint, url_prefix="/test")

@app.route("/")
def home():
    return "API is running! Endpoints: /sparql and /search"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
