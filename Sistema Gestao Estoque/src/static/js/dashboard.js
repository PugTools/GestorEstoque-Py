// Dashboard management
class DashboardManager {
    constructor() {
        this.initializeCharts();
        this.loadDashboardData();
    }

    async loadDashboardData() {
        try {
            const products = await ProductAPI.getAll();
            const movements = await StockMovementAPI.getAll();
            this.updateDashboardCards(products, movements);
            this.updateLowStockTable(products);
            this.updateTopSellingTable(movements);
        } catch (error) {
            console.error('Error loading dashboard data:', error);
        }
    }

    updateDashboardCards(products, movements) {
        // Calculate total stock value
        const totalStock = products.reduce((sum, p) => sum + p.quantity, 0);
        const totalStockValue = products.reduce((sum, p) => sum + (p.quantity * (p.unit_price || 0)), 0);
        
        // Update cards
        document.querySelector('.card:nth-child(1) .value').textContent = totalStock;
        document.querySelector('.card:nth-child(2) .value').textContent = 
            `R$ ${totalStockValue.toFixed(2)}`;
    }

    updateLowStockTable(products) {
        const lowStockProducts = products
            .filter(p => p.quantity < 10) // Example threshold
            .sort((a, b) => a.quantity - b.quantity)
            .slice(0, 5);

        const tbody = document.querySelector('#low-stock-table tbody');
        if (tbody) {
            tbody.innerHTML = lowStockProducts.map(p => `
                <tr>
                    <td>${p.sku}</td>
                    <td>${p.name}</td>
                    <td>${p.description || '-'}</td>
                    <td>${p.quantity}</td>
                    <td><span class="status ${p.quantity < 5 ? 'pending' : 'active'}">
                        ${p.quantity < 5 ? 'Crítico' : 'Baixo'}
                    </span></td>
                    <td>
                        <button class="btn btn-sm" onclick="handleRestockProduct(${p.id})">
                            <i class="fas fa-shopping-cart"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        }
    }

    initializeCharts() {
        // Sales Chart
        const salesCtx = document.getElementById('salesChart')?.getContext('2d');
        if (salesCtx) {
            new Chart(salesCtx, {
                type: 'line',
                data: {
                    labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho'],
                    datasets: [
                        {
                            label: 'Vendas',
                            data: [12000, 15000, 13500, 14800, 16200, 15500],
                            borderColor: '#4285f4',
                            backgroundColor: 'rgba(66, 133, 244, 0.1)',
                            tension: 0.4,
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        }
                    }
                }
            });
        }

        // ABC Chart
        const abcCtx = document.getElementById('abcChart')?.getContext('2d');
        if (abcCtx) {
            new Chart(abcCtx, {
                type: 'doughnut',
                data: {
                    labels: ['A (80%)', 'B (15%)', 'C (5%)'],
                    datasets: [{
                        data: [80, 15, 5],
                        backgroundColor: ['#ea4335', '#fbbc05', '#34a853']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }
}