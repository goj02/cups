export default function EventLog({ events }) {
  return (
    <div className="event-log">
      <h3>Events</h3>
      <ul>
        {events?.map((e, i) => (
          <li key={i}>{JSON.stringify(e)}</li>
        ))}
      </ul>
    </div>
  );
}
