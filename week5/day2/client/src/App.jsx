import { useState, useEffect } from 'react'

function App() {
    const [items, setItems] = useState([])
    const [name, setName] = useState('')

    useEffect(() => {
        fetch('http://localhost:5000/api/items')
            .then(res => res.json())
            .then(data => setItems(data))
            .catch(err => console.error('Error fetching:', err))
    }, [])

    const handleSubmit = (e) => {
        e.preventDefault()
        fetch('http://localhost:5000/api/items', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        })
            .then(res => res.json())
            .then(newItem => {
                setItems([...items, newItem])
                setName('')
            })
    }

    return (
        <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
            <h1>Multi-Container App</h1>
            <form onSubmit={handleSubmit}>
                <input value={name} onChange={e => setName(e.target.value)} placeholder="Item name" />
                <button type="submit">Add</button>
            </form>
            <ul>
                {items.map(item => <li key={item._id}>{item.name}</li>)}
            </ul>
        </div>
    )
}

export default App
