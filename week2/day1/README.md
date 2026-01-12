# HTML5 + Semantic Layout Learning Journey

## Overview
This project demonstrates the construction of a blog page using strictly **Semantic HTML5**. The goal was to understand page structure and accessibility without relying on generic containers or CSS for visual styling (visual structure implies the document outline).

## Key Concepts

### 1. Semantic Structure vs Generic Containers
- **Banned Tag**: `<div>` (Generic container with no meaning).
- **Used Tags**:
    - `<header>`: Introductory content or navigational links.
    - `<nav>`: Section of the page intended for navigation.
    - `<main>`: Dominant content of the <body>.
    - `<article>`: Self-contained composition (like a blog post).
    - `<section>`: Thematic grouping of content.
    - `<aside>`: Content tangentially related to the content around it (sidebar).
    - `<footer>`: Footer for its nearest sectioning content.

### 2. Forms & Validation
The contact form uses built-in HTML5 validation:
- `type="email"`: Ensures the input is formatted as an email address.
- `required`: Prevents submission if the field is empty.
- `<fieldset>` & `<legend>`: Groups related elements in a form, improving accessibility and structure.
- **Custom Validation**: Used `pattern` attribute for strict email regex and `oninvalid` to display a custom error message ("Enter valid email address").

### 3. Accessibility
- **ARIA Labels**: Used `aria-label` on the navigation to define it specifically as "Main Navigation".
- **Alt Text**: All images utilize the `alt` attribute to describe the visual content for screen readers.
- **Landmarks**: By using `<main>`, `<nav>`, and `<aside>`, we automatically create navigation landmarks for assistive technology.
- **Tab Index**: `tabindex="0"` was added to the `<blockquote>` element to ensure the "Chef's Tip" is reachable via keyboard navigation, properly demonstrating focus management.

### 4. Interactive & Embedded Content
- **Details & Summary**: Used `<details>` and `<summary>` tags to create native, JavaScript-free interactive accordions for long recipe content.
- **Embedded Map**: Integrated a Google Map using an `<iframe>` in the footer to satisfy media embedding requirements comfortably without external scripts.


