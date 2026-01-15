# DAY 4 : Todo App - JS Utilities & LocalStorage

I built this Todo App to demonstrate modular JavaScript, data persistence, and performance utilities.

## Features
- **Add, Edit, Delete & Toggle**: Full task management.
- **LocalStorage**: Data persists after page refresh.
- **Error Handling**: Uses `try/catch` to safely record errors in `logs/errors.md`.

## JS Utilities
- **Debounce**: Keeps the search bar smooth.
- **Throttle**: Limits execution rate of scroll events.
- **groupBy**: Categorizes tasks for the statistics display.

## Debugging Workflow
- **Breakpoints**: Paused execution to inspect the `addTodo` logic.
- **Watch Expressions**: Monitored the `todos` array in real-time.

## How to Test

### Local Testing
Because this project uses ES Modules (`type="module"`), it must be served over HTTP.
From the **parent directory of `todo-app/`**, run:

```bash
# Using Python
python3 -m http.server 3000 --directory todo-app
```
Then visit `http://localhost:3000`.
