// Elements
const productGrid = document.getElementById('productGrid');
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');
const sortSelect = document.getElementById('sortSelect');

let allProducts = [];
let filteredProducts = [];

// Fetch Products
async function fetchProducts() {
    try {
        const response = await fetch('https://dummyjson.com/products?limit=100');
        const data = await response.json();
        allProducts = data.products;
        filteredProducts = [...allProducts];

        populateCategories();
        renderProducts(filteredProducts);
    } catch (error) {
        console.error('Error fetching products:', error);
        productGrid.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: red;">Failed to load products. Please try again later.</p>`;
    }
}

// Populate Category Filter
function populateCategories() {
    const rawCategories = [...new Set(allProducts.map(p => p.category))];
    rawCategories.sort().forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        // Remove 'mens-' if it exists at the start of the category
        const label = category.replace(/^mens-/, '');
        option.textContent = label.charAt(0).toUpperCase() + label.slice(1);
        categoryFilter.appendChild(option);
    });
}

// Render Products
function renderProducts(products) {
    if (products.length === 0) {
        productGrid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 4rem;">
                <p style="font-size: 1.25rem; color: var(--text-muted);">No products found matching your criteria.</p>
            </div>
        `;
        return;
    }

    productGrid.innerHTML = products.map(product => {
        // Clean up category label for the badge as well
        const displayCategory = product.category.replace(/^mens-/, '');

        return `
            <article class="product-card">
                <div class="image-container">
                    <img src="${product.thumbnail}" alt="${product.title}" class="product-image" loading="lazy">
                </div>
                <div class="card-body">
                    <span class="category-badge">${displayCategory}</span>
                    <h3 class="product-title">${product.title}</h3>
                    <div class="rating">
                        ${'★'.repeat(Math.floor(product.rating))}${'☆'.repeat(5 - Math.floor(product.rating))}
                        <span>(${product.rating})</span>
                    </div>
                    <div class="product-price">$${product.price.toFixed(2)}</div>
                    <button class="btn-add" style="margin-top: 1rem;">Add to Cart</button>
                </div>
            </article>
        `;
    }).join('');
}

// Filter and Sort Logic
function applyFiltersAndSort(event) {
    // If searching, reset category filter to 'all' to avoid confusion
    if (event && event.target === searchInput) {
        categoryFilter.value = 'all';
    }

    const searchTerm = searchInput.value.toLowerCase().trim();
    const category = categoryFilter.value;
    const sortBy = sortSelect.value;

    // 1. Filter
    filteredProducts = allProducts.filter(product => {
        // Search in Title and Category only for better relevance
        const matchesSearch = product.title.toLowerCase().includes(searchTerm) ||
            product.category.toLowerCase().includes(searchTerm);

        const matchesCategory = category === 'all' || product.category === category;
        return matchesSearch && matchesCategory;
    });

    // 2. Sort
    if (sortBy === 'price-low') {
        filteredProducts.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price-high') {
        filteredProducts.sort((a, b) => b.price - a.price);
    }

    renderProducts(filteredProducts);
}

// Event Listeners
searchInput.addEventListener('input', applyFiltersAndSort);
categoryFilter.addEventListener('change', applyFiltersAndSort);
sortSelect.addEventListener('change', applyFiltersAndSort);

// Initialize
fetchProducts();
