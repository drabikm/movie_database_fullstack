import ActorListItem from "./ActorListItem";

export default function MoviesList(props) {
    return <div>
        <h2>Actors</h2>
        <ul className="actors-list">
            {props.actors.map(actor => <li key={actor.surname}>
                <ActorListItem actor={actor} onDelete={() => props.onDeleteActor(actor)}
                onAssign={() => props.onAssignActor(actor)}/>
            </li>)}
        </ul>
    </div>;
}