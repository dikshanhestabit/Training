/**
 * Day 3: JS & DOM Practice
 * Concepts: ES6, DOM Selection, Event Listeners, ClassList
 */

console.log("🚀 JS Practice Script Loaded!");

document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Navbar Toggle (Mobile) ---
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('show');
            console.log("Navbar toggled");
        });
    }

    // --- 2. Dropdown Functionality ---
    const dropBtn = document.getElementById('dropBtn');
    const dropContent = document.getElementById('dropContent');

    if (dropBtn && dropContent) {
        dropBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            dropContent.classList.toggle('show');
            console.log("Dropdown toggled");
        });
    }

    // Close dropdown when clicking outside
    document.addEventListener('click', () => {
        if (dropContent) {
            dropContent.classList.remove('show');
        }
    });

    // --- 3. Counter & Key Events ---
    const counterValue = document.getElementById('counterValue');
    const incrementBtn = document.getElementById('increment');
    const decrementBtn = document.getElementById('decrement');

    let count = 0;

    const updateCounter = (val) => {
        count += val;
        if (counterValue) {
            counterValue.textContent = count;
            counterValue.style.transform = 'scale(1.2)';
            setTimeout(() => counterValue.style.transform = 'scale(1)', 100);
        }
    };

    if (incrementBtn) {
        incrementBtn.addEventListener('click', () => updateCounter(1));
    }
    if (decrementBtn) {
        decrementBtn.addEventListener('click', () => updateCounter(-1));
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowUp') updateCounter(1);
        if (e.key === 'ArrowDown') updateCounter(-1);
    });

    // --- 4. FAQ Accordion Logic (Dynamic with .map) ---
    const faqData = [
        { id: 1, q: "What is ES6?", a: "ES6 (ECMAScript 2015) is an update to the JavaScript that introduced significant new features to make JavaScript more powerful, readable, and easier to use, including arrow functions, classes, modules, let/const keywords." },
        { id: 2, q: "Why use 'let' and 'const'?", a: "They provide block-scoping, which prevents bugs caused by 'var' and its function-scoping/hoisting behavior." },
        { id: 3, q: "How does the DOM work?", a: "The DOM is a tree-like representation of your HTML that JavaScript can interact with to change content and styles dynamically." }
    ];

    const accordionContainer = document.getElementById('accordionContainer');

    const renderFAQs = (data) => {
        if (!accordionContainer) return;

        accordionContainer.innerHTML = data.map(item => `
            <div class="accordion-item" data-id="${item.id}">
                <button class="accordion-header">
                    ${item.q}
                    <span class="icon">+</span>
                </button>
                <div class="accordion-content">
                    <p>${item.a}</p>
                </div>
            </div>
        `).join('');

        attachAccordionListeners();
    };

    const attachAccordionListeners = () => {
        const headers = document.querySelectorAll('.accordion-header');
        headers.forEach(header => {
            header.addEventListener('click', () => {
                const currentItem = header.parentElement;
                const isOpen = currentItem.classList.contains('active');

                document.querySelectorAll('.accordion-item').forEach(item => {
                    item.classList.remove('active');
                });

                if (!isOpen) {
                    currentItem.classList.add('active');
                }
                console.log("FAQ item toggled");
            });
        });
    };

    renderFAQs(faqData);

    // --- 5. Modal Logic ---
    const openModalBtn = document.getElementById('openModal');
    const closeModalBtn = document.getElementById('closeModal');
    const modalOverlay = document.getElementById('modalOverlay');
    const modalConfirm = document.getElementById('modalConfirm');

    const toggleModal = (show) => {
        if (modalOverlay) {
            modalOverlay.style.display = show ? 'flex' : 'none';
            document.body.style.overflow = show ? 'hidden' : 'auto';
        }
    };

    if (openModalBtn) openModalBtn.addEventListener('click', () => toggleModal(true));
    if (closeModalBtn) closeModalBtn.addEventListener('click', () => toggleModal(false));
    if (modalConfirm) modalConfirm.addEventListener('click', () => toggleModal(false));

    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) toggleModal(false);
        });
    }

    // --- 6. Mini-Challenges ---
    const numbers = [10, 20, 30, 40, 50];
    const doubled = numbers.map(n => n * 2);
    const filtered = numbers.filter(n => n > 25);
    const sum = numbers.reduce((acc, curr) => acc + curr, 0);

    console.log("Mini-Challenges (map, filter, reduce):", { doubled, filtered, sum });

});
