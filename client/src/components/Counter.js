import useCounterStore from "../stores/counterStore2";

function Counter() {

    const { count, increment, decrement, reset } = useCounterStore();

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>Counter: {count}</h1>
            <div className="btn-group">
                <button className="btn" onClick={increment}>➕ Increment</button>
                <button className="btn" onClick={decrement}>➖ Decrement</button>
                <button className="btn" onClick={reset}>🔄 Reset</button>
            </div>
        </div>
    )
}

export default Counter;
