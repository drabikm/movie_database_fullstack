import ActorMovieListItem from "./ActorMovieListItem";

export default function ActorMovieList(props) {
    return <div>
        <h2>Actors for the movie {props.movieTitle}</h2>
        <ul className="actors-list">
            {props.actors.map(actor => <li key={actor.surname}>
                <ActorMovieListItem actor={actor}/>
            </li>)}
        </ul>
    </div>;
}