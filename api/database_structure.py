from typing import Any

from fastapi import HTTPException
from peewee import *

from api import validations

db = SqliteDatabase('api/movies-extended.db')

class BaseModel(Model):
    class Meta:
        database = db

class Actor(BaseModel):
    id = IntegerField()
    name = CharField()
    surname = CharField()

class Movie(BaseModel):
    id = IntegerField()
    title = CharField()
    director = CharField()
    year = IntegerField()
    description = TextField()
    actors = ManyToManyField(Actor, backref='movies')

ActorMovie = Movie.actors.get_through_model()
db.connect()
db.create_tables([Actor, Movie, ActorMovie])

def verify_movie_exist(movie_id:int):
    try:
        movie = Movie.get(Movie.id == movie_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f'Movie with id {movie_id} does not exist in database')
    return movie

def verify_actor_exist(actor_id:int):
    try:
        actor = Actor.get(Actor.id == actor_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f'Actor with id {actor_id} does not exist in database')
    return actor

def listMovies():
    movies = []
    for movie in Movie.select():
        movie = {'id': movie.id, 'title': movie.title, 'year': movie.year, 'director': movie.director, 'description': movie.description}
        movies.append(movie)
    return movies

def listActors():
    actors = []
    for actor in Actor.select():
        actor = {'id': actor.id, 'name': actor.name, 'surname': actor.surname}
        actors.append(actor)
    return actors

def getMovie(movie_id:int):
    movie = verify_movie_exist(movie_id)
    return '{0}, {1}, {2}, {3}'.format(movie.title, movie.director, movie.year, movie.description)

def getActor(actor_id:int):
    actor = verify_actor_exist(actor_id)
    return '{0} {1}'.format(actor.name, actor.surname)

def addMovie(movie_info: dict[str, Any]):
    validations.validate_movie_json(movie_info)
    new_movie = Movie(title=movie_info.get('title'), year=movie_info.get('year'), director=movie_info.get('director'), description=movie_info.get('description'))
    new_movie.save()
    return new_movie.id

def addActor(actor_info: dict[str, Any]):
    validations.validate_actor_json(actor_info)
    new_actor = Actor(name=actor_info.get('name'), surname=actor_info.get('surname'))
    new_actor.save()
    return new_actor.id

def updateMovie(movie_info: dict[str, Any], movie_id:int):
    movie = verify_movie_exist(movie_id)
    validations.validate_movie_json(movie_info)
    movie.title = movie_info.get('title')
    movie.director = movie_info.get('director')
    movie.year = movie_info.get('year')
    movie.description = movie_info.get('description')
    movie.save()

def updateActor(actor_info: dict[str, Any], actor_id:int):
    actor = verify_actor_exist(actor_id)
    validations.validate_actor_json(actor_info)
    actor.name = actor_info.get('name')
    actor.surname = actor_info.get('surname')
    actor.save()

def deleteMovie(movie_id:int):
    movie = verify_movie_exist(movie_id)
    ActorMovie.delete().where(ActorMovie.movie.id == movie_id)
    movie.delete_instance()

def deleteActor(actor_id:int):
    actor = verify_actor_exist(actor_id)
    ActorMovie.delete().where(ActorMovie.actor.id == actor_id)
    actor.delete_instance()

def getActorsForMovie(movie_id:int):
    movie = verify_movie_exist(movie_id)
    actors = []
    for actor in movie.actors:
        actors.append({'id': actor.id, 'name': actor.name, 'surname': actor.surname})
    return actors

def getMoviesForActor(actor_ids:int):
    actor = verify_actor_exist(actor_ids)
    movies = []
    for movie in actor.movies:
        movies.append('{0} {1}'.format(movie.title, movie.director))
    return movies

def addActorToMovie(movie_id:int, actor_id:int):
    actor = verify_actor_exist(actor_id)
    movie = verify_movie_exist(movie_id)
    try:
        movie.actors.add(actor)
    except IntegrityError:
        raise HTTPException(status_code=418,detail="It is already linked and I am a teapot :D")