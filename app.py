import graphene
from flask import Flask, request
from graphene import Schema

# Definir el tipo User con más campos
class User(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    age = graphene.Int()
    characteristics = graphene.List(graphene.String)
    email = graphene.String()
    address = graphene.String()

# Definir la clase Query para obtener los usuarios
class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.Int())

    def resolve_user(self, info, id):
        # Datos de ejemplo
        users = [
            {"id": 1, "name": "Alice", "age": 30, "characteristics": ["smart", "friendly"], "email": "alice@example.com", "address": "123 Main St"},
            {"id": 2, "name": "Bob", "age": 25, "characteristics": ["strong", "outgoing"], "email": "bob@example.com", "address": "456 Elm St"}
        ]
        
        # Buscar el usuario por ID
        user = next((u for u in users if u["id"] == id), None)
        if user:
            # Si el usuario existe, devolverlo como un objeto User
            return User(id=user["id"], name=user["name"], age=user["age"], characteristics=user["characteristics"], email=user["email"], address=user["address"])
        return None  # Si no se encuentra, devolver None

# Configuración de Flask y GraphQL
app = Flask(__name__)

# Crear el esquema de GraphQL
schema = graphene.Schema(query=Query)

@app.route("/graphql/<int:user_id>", methods=["GET"])
def graphql_server(user_id):
    # Buscar el usuario por el ID proporcionado en la URL
    query = f"{{user(id:{user_id}){{name age}}}}"
    
    # Ejecutar la consulta de GraphQL y devolver la respuesta
    response = schema.execute(query)
    return {"data": response.data}

if __name__ == '__main__':
    app.run(debug=True)
