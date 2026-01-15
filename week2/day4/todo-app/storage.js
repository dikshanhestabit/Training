/**
 * Handles all LocalStorage operations with error handling.
 */
const STORAGE_KEY = 'todo_app_data';

export function getTodos() {
    try {
        const data = localStorage.getItem(STORAGE_KEY);
        return data ? JSON.parse(data) : [];
    } catch (error) {
        logError('Failed to load todos from LocalStorage', error);
        return [];
    }
}

export function saveTodos(todos) {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
    } catch (error) {
        logError('Failed to save todos to LocalStorage', error);
        alert('Could not save your changes. Storage might be full.');
    }
}

function logError(message, error) {
    const timestamp = new Date().toISOString();
    console.error(`[${timestamp}] ${message}:`, error);

    // In a real app, this might send to a server. 
    // For this project, we'll store it in a special "app_errors" key 
    // to demonstrate the concept of error boundaries.
    const errors = JSON.parse(localStorage.getItem('app_errors') || '[]');
    errors.push({ timestamp, message, stack: error.stack });
    localStorage.setItem('app_errors', JSON.stringify(errors.slice(-10))); // Keep last 10
}
