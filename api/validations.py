import jsonschema
from fastapi import HTTPException
from jsonschema import validate

movie_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "director": {"type": "string"},
        "year": {"type": "string"},
        "description": {"type": "string"}
    },
    "required": ["title", "director", "year", "description"]
}

actor_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "surname": {"type": "string"}
    },
    "required": ["name", "surname"]
}

def validate_movie_json(data):
    try:
        validate(instance=data, schema=movie_schema)
    except jsonschema.exceptions.ValidationError as e:
        raise HTTPException(status_code=400, detail=f'{e.message}')

def validate_actor_json(actor_info):
    try:
        validate(instance=actor_info, schema=actor_schema)
    except jsonschema.exceptions.ValidationError as e:
        raise HTTPException(status_code=400, detail=f'{e.message}')