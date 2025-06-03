// Products management
class ProductsManager {
    constructor() {
        this.productTable = document.getElementById('product-table');
        this.initializeEventListeners();
        this.loadProducts();
    }

    async loadProducts() {
        try {
            const products = await ProductAPI.getAll();
            this.renderProductsTable(products);
        } catch (error) {
            console.error('Error loading products:', error);
            this.showError('Erro ao carregar produtos');
        }
    }

    renderProductsTable(products) {
        const tbody = this.productTable.querySelector('tbody');
        tbody.innerHTML = products.map(product => `
            <tr data-product-id="${product.id}">
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.sku}</td>
                <td>${product.quantity}</td>
                <td>R$ ${product.unit_price?.toFixed(2) || '0.00'}</td>
                <td>
                    <button class="btn btn-sm btn-secondary edit-product" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-success add-stock" title="Entrada">
                        <i class="fas fa-plus"></i>
                    </button>
                    <button class="btn btn-sm btn-danger remove-stock" title="Saída">
                        <i class="fas fa-minus"></i>
                    </button>
                    <button class="btn btn-sm btn-danger delete-product" title="Excluir">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    async handleAddProduct(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const productData = {
            name: formData.get('name'),
            sku: formData.get('sku'),
            description: formData.get('description'),
            unit_price: parseFloat(formData.get('unit_price')),
            quantity: parseInt(formData.get('quantity')) || 0
        };

        try {
            await ProductAPI.create(productData);
            this.loadProducts();
            this.closeModal('addProductModal');
            this.showSuccess('Produto adicionado com sucesso');
        } catch (error) {
            console.error('Error creating product:', error);
            this.showError('Erro ao criar produto');
        }
    }

    async handleStockMovement(productId, type, quantity) {
        try {
            await StockMovementAPI.create({
                product_id: productId,
                movement_type: type,
                quantity: parseInt(quantity),
                reason: `Movimentação manual - ${type}`
            });
            this.loadProducts();
            this.showSuccess('Estoque atualizado com sucesso');
        } catch (error) {
            console.error('Error updating stock:', error);
            this.showError('Erro ao atualizar estoque');
        }
    }

    initializeEventListeners() {
        // Add product button
        document.querySelector('.btn-success[data-action="add-product"]')?.addEventListener('click', () => {
            this.showModal('addProductModal');
        });

        // Product form submission
        document.getElementById('addProductForm')?.addEventListener('submit', (e) => this.handleAddProduct(e));

        // Table action buttons
        this.productTable?.addEventListener('click', async (e) => {
            const target = e.target.closest('button');
            if (!target) return;

            const tr = target.closest('tr');
            const productId = tr?.dataset.productId;

            if (target.classList.contains('edit-product')) {
                // Implement edit functionality
            } else if (target.classList.contains('add-stock')) {
                const quantity = prompt('Quantidade para entrada:', '1');
                if (quantity) {
                    await this.handleStockMovement(productId, 'entrada', quantity);
                }
            } else if (target.classList.contains('remove-stock')) {
                const quantity = prompt('Quantidade para saída:', '1');
                if (quantity) {
                    await this.handleStockMovement(productId, 'saida', quantity);
                }
            } else if (target.classList.contains('delete-product')) {
                if (confirm('Tem certeza que deseja excluir este produto?')) {
                    try {
                        await ProductAPI.delete(productId);
                        this.loadProducts();
                        this.showSuccess('Produto excluído com sucesso');
                    } catch (error) {
                        console.error('Error deleting product:', error);
                        this.showError('Erro ao excluir produto');
                    }
                }
            }
        });
    }

    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'block';
        }
    }

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
        }
    }

    showSuccess(message) {
        // Implement success notification
        alert(message); // Temporary implementation
    }

    showError(message) {
        // Implement error notification
        alert(message); // Temporary implementation
    }
}