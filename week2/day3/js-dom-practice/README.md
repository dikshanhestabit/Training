# Day 3: JavaScript ES6 & DOM Summary

##  Key Concepts Implemented

### 1. Modern Variables (`let` vs `const`)
- **`const`**: Used for DOM element references and fixed data arrays (e.g., FAQ data).
- **`let`**: Used for the counter state (`count`) because its value changes.

### 2. Arrow Functions
- Used shorter syntax for event listeners and utility functions.
- Benefit: They inherit `this` from the parent scope, preventing context issues in complex UI logic.

### 3. Array Methods
- **`.map()`**: Dynamically built the FAQ HTML items from a JavaScript object array.
- **`.filter()`**: (Used in background) Extracts specific data based on criteria.
- **`.reduce()`**: (Used in background) Aggregates array values into a single result (e.g., total sum).

### 4. DOM Manipulation
- **`document.getElementById`**: Selected specific elements for interaction.
- **`classList.toggle()`**: Handled the visibility of the Navbar, Dropdown, and FAQ items.
- **`addEventListener`**: Attached logic to user actions (click, keydown).

## Components Built
1. **Hamburger Navbar**: Toggles menu on mobile.
2. **Dropdown Menu**: Resources list with click-outside closure.
3. **Interactive Counter**: Multi-modal control (Buttons + Arrow Keys).
4. **FAQ Accordion**: Single-open expansion logic with smooth CSS transitions.
5. **Modal Popup**: Centered overlay with backdrop focus.


