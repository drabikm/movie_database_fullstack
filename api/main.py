from typing import Any

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import api.database_structure as db

app = FastAPI()

app.mount("/static", StaticFiles(directory="../ui/build/static", check_dir=False), name="static")

@app.get("/")
def serve_react_app():
   return FileResponse("../ui/build/index.html")

@app.get('/movies')
def get_movies():
    return db.listMovies()

@app.get('/movies/{movie_id}')
def get_movie_by_id(movie_id:int):
    return db.getMovie(movie_id)

@app.post('/movies')
def add_movie(movie_info: dict[str, Any]):
    ids = db.addMovie(movie_info)
    return {"message": f"Movie with id = {ids} added successfully", "id": {ids}}

@app.put("/movies/{movie_id}")
def update_movie(params: dict[str, Any], movie_id:int):
    db.updateMovie(params, movie_id)
    return {f"Movie edited successfully"}

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id:int):
    db.deleteMovie(movie_id)
    return f'Movie with id {movie_id} deleted successfully'

@app.get('/actors')
def get_actors():
    return db.listActors()

@app.get('/actors/{actor_id}')
def get_actor_by_id(actor_id:int):
    return db.getActor(actor_id)

@app.post('/actors')
def add_actor(actor_info: dict[str, Any]):
    ids = db.addActor(actor_info)
    return f'Actor added successfully with id {ids}'

@app.put("/actors/{actor_id}")
def update_actor(params: dict[str, Any], actor_id:int):
    db.updateActor(params, actor_id)
    return {f"Actor edited successfully"}

@app.delete("/actors/{actor_id}")
def delete_actor(actor_id:int):
    db.deleteActor(actor_id)
    return f'Actor with id {actor_id} deleted successfully'

@app.get("/movies/{movie_id}/actors")
def get_actors_for_movie(movie_id:int):
    return db.getActorsForMovie(movie_id)

@app.get("/actors/{actor_id}/movies")
def get_movies_for_actor(actor_id:int):
    return db.getMoviesForActor(actor_id)

@app.post("/movies/{movie_id}/actors/{actor_id}")
def add_actors_to_movie(movie_id:int,actor_id:int):
    db.addActorToMovie(movie_id,actor_id)
    return 'Actor added to the movie'