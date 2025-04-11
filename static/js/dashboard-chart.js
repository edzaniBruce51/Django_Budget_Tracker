/**
 * Dashboard Charts Configuration
 * This file contains the configuration for all charts displayed on the dashboard
 */

// Initialize charts when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize expense category chart if the element exists
    if (document.getElementById('expenseCategoryChart')) {
        initializeExpenseCategoryChart();
    }

     // Initialize budget progress chart if the element exists
     if (document.getElementById('budgetProgressChart')) {
        initializeBudgetProgressChart();
    }

    // Initialize expense trend chart if the element exists
    if (document.getElementById('expenseTrendChart')) {
        initializeExpenseTrendChart();
    }
});

/**
 * Initialize the expense category pie chart
 */
function initializeExpenseCategoryChart() {
    const ctx = document.getElementById('expenseCategoryChart').getContext('2d');
    
    // Get data from the data attributes
    const chartElement = document.getElementById('expenseCategoryChart');
    const categories = JSON.parse(chartElement.dataset.categories || '[]');
    const amounts = JSON.parse(chartElement.dataset.amounts || '[]');
    
    // Generate colors for each category
    const colors = generateColors(categories.length);
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: categories,
            datasets: [{
                data: amounts,
                backgroundColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                },
                title: {
                    display: true,
                    text: 'Expenses by Category'
                }
            }
        }
    });
}

/**
 * Initialize the budget progress bar chart
 */
function initializeBudgetProgressChart() {
    const ctx = document.getElementById('budgetProgressChart').getContext('2d');
    
    // Get data from the data attributes
    const chartElement = document.getElementById('budgetProgressChart');
    const budgetNames = JSON.parse(chartElement.dataset.budgetNames || '[]');
    const budgetAmounts = JSON.parse(chartElement.dataset.budgetAmounts || '[]');
    const spentAmounts = JSON.parse(chartElement.dataset.spentAmounts || '[]');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: budgetNames,
            datasets: [
                {
                    label: 'Budget Amount',
                    data: budgetAmounts,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Spent Amount',
                    data: spentAmounts,
                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Amount (R)'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Budget vs. Spent'
                }
            }
        }
    });
}

/**
 * Initialize the expense trend line chart
 */
function initializeExpenseTrendChart() {
    const ctx = document.getElementById('expenseTrendChart').getContext('2d');
    
    // Get data from the data attributes
    const chartElement = document.getElementById('expenseTrendChart');
    const dates = JSON.parse(chartElement.dataset.dates || '[]');
    const amounts = JSON.parse(chartElement.dataset.amounts || '[]');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Daily Expenses',
                data: amounts,
                fill: false,
                borderColor: 'rgba(75, 192, 192, 1)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Amount (R)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Expense Trend'
                }
            }
        }
    });
}

/**
 * Generate an array of colors for chart elements
 * @param {number} count - Number of colors to generate
 * @returns {string[]} Array of color strings
 */
function generateColors(count) {
    const colors = [
        'rgba(255, 99, 132, 0.7)',   // Red
        'rgba(54, 162, 235, 0.7)',   // Blue
        'rgba(255, 206, 86, 0.7)',   // Yellow
        'rgba(75, 192, 192, 0.7)',   // Green
        'rgba(153, 102, 255, 0.7)',  // Purple
        'rgba(255, 159, 64, 0.7)',   // Orange
        'rgba(199, 199, 199, 0.7)',  // Gray
        'rgba(83, 102, 255, 0.7)',   // Indigo
        'rgba(255, 99, 255, 0.7)',   // Pink
        'rgba(99, 255, 132, 0.7)'    // Light Green
    ];
    
    // If we need more colors than in our predefined array, generate them
    if (count > colors.length) {
        for (let i = colors.length; i < count; i++) {
            const r = Math.floor(Math.random() * 255);
            const g = Math.floor(Math.random() * 255);
            const b = Math.floor(Math.random() * 255);
            colors.push(`rgba(${r}, ${g}, ${b}, 0.7)`);
        }
    }
    
    return colors.slice(0, count);
}