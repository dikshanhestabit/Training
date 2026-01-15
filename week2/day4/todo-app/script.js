import { debounce, throttle, groupBy } from './utils.js';
import { getTodos, saveTodos } from './storage.js';

// State Management
let todos = getTodos();
let editingId = null;

// DOM Elements
const todoInput = document.getElementById('todo-input');
const addBtn = document.getElementById('add-btn');
const todoList = document.getElementById('todo-list');
const searchInput = document.getElementById('search-input');
const taskCount = document.getElementById('task-count');
const groupsInfo = document.getElementById('groups-info');
const clearCompletedBtn = document.getElementById('clear-completed');

// Edit Modal Elements
const editModal = document.getElementById('edit-modal');
const editInput = document.getElementById('edit-input');
const saveEditBtn = document.getElementById('save-edit');
const cancelEditBtn = document.getElementById('cancel-edit');

/**
 * Renders the todo list based on the current state.
 * Includes grouping logic to show stats.
 */
function render(filteredTodos = todos) {
    todoList.innerHTML = '';

    filteredTodos.forEach(todo => {
        const li = document.createElement('li');
        li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
        li.innerHTML = `
            <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''}>
            <span class="todo-text">${todo.text}</span>
            <div class="todo-actions">
                <button class="btn-icon edit-btn" title="Edit">✏️</button>
                <button class="btn-icon delete-btn" title="Delete">🗑️</button>
            </div>
        `;

        // Event Listeners
        li.querySelector('.todo-checkbox').onclick = () => toggleTodo(todo.id);
        li.querySelector('.delete-btn').onclick = () => deleteTodo(todo.id);
        li.querySelector('.edit-btn').onclick = () => openEditModal(todo);

        todoList.appendChild(li);
    });

    updateStats();
}

/**
 * Updates stats using the groupBy utility.
 */
function updateStats() {
    const activeTasks = todos.filter(t => !t.completed).length;
    taskCount.textContent = `${activeTasks} tasks left`;

    // Demonstrate groupBy: Group todos by status
    const grouped = groupBy(todos, 'completed');
    const completedCount = (grouped['true'] || []).length;
    const pendingCount = (grouped['false'] || []).length;

    groupsInfo.innerHTML = `
        <span>Pending: ${pendingCount}</span>
        <span>Completed: ${completedCount}</span>
    `;
}

// Actions
function addTodo() {
    // This is a great place for a BREAKPOINT!
    const text = todoInput.value.trim();
    if (!text) return;

    const newTodo = {
        id: Date.now(),
        text: text,
        completed: false
    };

    todos.push(newTodo);
    todoInput.value = '';
    saveAndRender();
}

function toggleTodo(id) {
    todos = todos.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
    );
    saveAndRender();
}

function deleteTodo(id) {
    todos = todos.filter(todo => todo.id !== id);
    saveAndRender();
}

function openEditModal(todo) {
    editingId = todo.id;
    editInput.value = todo.text;
    editModal.classList.add('active');
    editInput.focus();
}

function closeEditModal() {
    editingId = null;
    editModal.classList.remove('active');
}

function saveEdit() {
    const newText = editInput.value.trim();
    if (newText) {
        todos = todos.map(todo =>
            todo.id === editingId ? { ...todo, text: newText } : todo
        );
        saveAndRender();
        closeEditModal();
    }
}

function saveAndRender() {
    saveTodos(todos);
    render();
}

// Utility Usage - Debounced Search
const handleSearch = debounce(() => {
    const query = searchInput.value.toLowerCase();
    const filtered = todos.filter(todo =>
        todo.text.toLowerCase().includes(query)
    );
    render(filtered);
}, 300);

// Utility Usage - Throttled Log (Example of Throttle)
const throttledScrollLog = throttle(() => {
    console.log('Throttled Scroll: Checking scroll position...');
}, 2000);

// Event Listeners
addBtn.addEventListener('click', addTodo);
todoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addTodo();
});

searchInput.addEventListener('input', handleSearch);

clearCompletedBtn.addEventListener('click', () => {
    todos = todos.filter(t => !t.completed);
    saveAndRender();
});

saveEditBtn.addEventListener('click', saveEdit);
cancelEditBtn.addEventListener('click', closeEditModal);
window.addEventListener('scroll', throttledScrollLog);

// Initial Render
render();
