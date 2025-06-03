// API endpoints
const API_BASE_URL = '/api';

// Product API
const ProductAPI = {
    async getAll() {
        const response = await fetch(`${API_BASE_URL}/products`);
        return response.json();
    },

    async getById(id) {
        const response = await fetch(`${API_BASE_URL}/products/${id}`);
        return response.json();
    },

    async create(productData) {
        const response = await fetch(`${API_BASE_URL}/products`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(productData),
        });
        return response.json();
    },

    async update(id, productData) {
        const response = await fetch(`${API_BASE_URL}/products/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(productData),
        });
        return response.json();
    },

    async delete(id) {
        await fetch(`${API_BASE_URL}/products/${id}`, {
            method: 'DELETE',
        });
    }
};

// Stock Movement API
const StockMovementAPI = {
    async getAll(productId = null) {
        const url = new URL(`${API_BASE_URL}/stock_movements`);
        if (productId) {
            url.searchParams.append('product_id', productId);
        }
        const response = await fetch(url);
        return response.json();
    },

    async create(movementData) {
        const response = await fetch(`${API_BASE_URL}/stock_movements`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(movementData),
        });
        return response.json();
    }
};