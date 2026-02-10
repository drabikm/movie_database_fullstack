import './App.css';
import {useEffect, useState} from "react";
import "milligram";
import MovieForm from "./MovieForm";
import MoviesList from "./MoviesList";
import ActorsList from "./ActorsList";
import ActorForm from "./ActorForm";
import ActorMovieList from "./ActorMovieList";

function App() {
    const [movies, setMovies] = useState([]);
    const [addingMovie, setAddingMovie] = useState(false);
    const [actors, setActors] = useState([]);
    const [addingActor, setAddingActor] = useState(false);
    const [actorsForMovie, setActorsForMovie] = useState([]);
    const [ifActorsForMovie, setFfActorsForMovie] = useState(false)
    const [movie, setMovie] = useState()
    const handleMovieCancel = () => {
        setAddingMovie(false);
    };
    const handleActorAddCancel = () => {
        setAddingMovie(false);
    };

    useEffect(() => {
        const fetchMovies = async () => {
            const response = await fetch(`/movies`);
            if (response.ok) {
                const movies = await response.json();
                setMovies(movies);
            }
        };
        const fetchActors = async () => {
            const response = await fetch(`/actors`);
            if (response.ok) {
                const actors = await response.json();
                setActors(actors);
            }
        };
        fetchMovies();
        fetchActors();
    }, []);

    async function handleAddMovie(movie) {
        const response = await fetch('/movies', {
        method: 'POST',
        body: JSON.stringify(movie),
        headers: { 'Content-Type': 'application/json' }
        });
        if (response.ok) {
            const addingResponse = await response.json();
            movie.id = addingResponse.id;
            setMovies([...movies, movie]);
            setAddingMovie(false);
        }
    }

    async function handleAddActor(actor) {
        const response = await fetch('/actors', {
        method: 'POST',
        body: JSON.stringify(actor),
        headers: { 'Content-Type': 'application/json' }
        });
        if (response.ok) {
            const addingResponse = await response.json();
            actor.id = addingResponse.id;
            setActors([...actors, actor]);
            setAddingActor(false);
        }
    }

    async function handleDeleteMovie(movie) {
        const response = await fetch(`/movies/${movie.id}`, {
            method: 'DELETE'
        });
        if (response.ok) {
          const nextMovies = movies.filter(m => m !== movie);
          setMovies(nextMovies);
        }
    }

    async function handleDeleteActor(actor) {
        const response = await fetch(`/actors/${actor.id}`, {
            method: 'DELETE'
        });
        if (response.ok) {
          const nextActors = actors.filter(a => a !== actor);
          setActors(nextActors);
        }
    }

    async function handleViewActors(movie) {
        const response = await fetch(`/movies/${movie.id}/actors`);
        if (response.ok) {
            const actors = await response.json();
            setActorsForMovie(actors);
            setFfActorsForMovie(true);
            setMovie(movie)
        }
    }

    async function handleAssignActors(movie, actor) {
        if(ifActorsForMovie===false) {
            alert("First check actors for movie you want to assign actor to")
            return;
        }
        const response = await fetch(`/movies/${movie.id}/actors/${actor.id}`, {
            method: 'POST'
        });
        if (response.ok) {
            setActorsForMovie([...actorsForMovie, actor]);
        }
    }

    return (
        <div className="container">
            <h1>My favourite movies to watch</h1>
            <div className="row">
                <div className="column">
                    {movies.length === 0
                        ? <p>No movies yet. Maybe add something?</p>
                        : <MoviesList movies={movies}
                              onDeleteMovie={(movie) => handleDeleteMovie(movie)}
                            viewActors={(movie) => handleViewActors(movie)}/>}
                    {addingMovie
                        ? <MovieForm onMovieSubmit={handleAddMovie} onMovieCancel={handleMovieCancel}
                             buttonLabel="Add new movie"/>
                        : <div>
                            <button onClick={() => setAddingMovie(true)}>Add a movie</button>
                        </div>
                        }
                </div>
                <div className="column">
                    {actors.length === 0
                        ? <p>There is no actors. Try to add one</p>
                        : <ActorsList actors={actors}
                              onDeleteActor={(actor) => handleDeleteActor(actor)}
                            onAssignActor={(actor) => handleAssignActors(movie,actor)}/>}
                    {addingActor
                        ? <ActorForm onActorSubmit={handleAddActor} onActorCancel={handleActorAddCancel}
                             buttonLabel="Add new actor"/>
                        : <div>
                            <button onClick={() => setAddingActor(true)}>Add an actor</button>
                        </div>
                        }
                </div>
                {ifActorsForMovie
                        ? <div className="column">
                        {actorsForMovie.length === 0
                            ? <p>There is no actors assigned to movie ... Do you want to add one?</p>
                            :
                            <ActorMovieList actors={actorsForMovie} movieTitle={movie.title}/>}
                        </div>:<div/>
                        }
            </div>
        </div>
    );
}

export default App;