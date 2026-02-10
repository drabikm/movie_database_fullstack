export default function ActorMovieListItem(props) {
    return (
        <div>
            <div>
                <strong>{props.actor.name}</strong>
                {' '}
                <strong>{props.actor.surname}</strong>
            </div>
        </div>
    );
}