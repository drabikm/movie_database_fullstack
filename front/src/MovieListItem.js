export default function MovieListItem(props) {

    return (
        <div>
            <div>
                <strong>{props.movie.title}</strong>
                {' '}
                <span>({props.movie.year})</span>
                {' '}
                directed by {props.movie.director}
                {' '}
                <a onClick={props.onDelete}>Delete</a>
                {' '}
                <a onClick={props.viewActors}>View Actors</a>
                {' '}
            </div>
            {props.movie.description}
        </div>
    );
}