# UI Component Docs

## Overview
This folder contains a small reusable component library built with **TailwindCSS** and **Next.js**. All components are functional React components that accept props for customization.

---

## `Button.jsx`
- **Props**
  - `children` – button label
  - `onClick` – click handler
  - `variant` – `"primary"`, `"secondary"`, `"success"`, `"info"`, `"warning"`, `"danger"`
  - `className` – additional Tailwind classes
  - any other native button props via `...rest`

---

## `Input.jsx`
- **Props**
  - `id` – required for label association
  - `label` – optional label text
  - `type` – input type (default `"text"`)
  - `placeholder` – placeholder text
  - `className` – extra classes
  - any other native input props via `...rest`

---

## `Card.jsx`
- **Props**
  - `title` – optional heading
  - `children` – card content
  - `variant` – `"default"`, `"primary"`, `"success"`, `"info"`, `"warning"`, `"danger"`
  - `className` – extra Tailwind classes

---

## `Badge.jsx`
- **Props**
  - `children` – badge label
  - `variant` – `"default"`, `"success"`, `"warning"`, `"danger"`, `"info"`
  - `className` – extra classes

---

## `Modal.jsx`
- **Props**
  - `isOpen` – boolean to control visibility
  - `onClose` – callback when modal should close
  - `title` – header text
  - `children` – modal content
