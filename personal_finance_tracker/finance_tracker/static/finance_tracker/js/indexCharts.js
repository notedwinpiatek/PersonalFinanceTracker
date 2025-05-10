const montlyChartEl = document.getElementById('monthlyChart');
const ctx = montlyChartEl.getContext('2d');
const incomeData = JSON.parse(montlyChartEl.getAttribute("data-income"));
const expenseData = JSON.parse(montlyChartEl.getAttribute("data-expense"));
const months = JSON.parse(montlyChartEl.getAttribute("data-months"));
const currencySign = montlyChartEl.getAttribute("data-currency-sign");
import { formatCurrency } from "./utils.js";

const chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: months,
        datasets: [
            {
                label: 'Max Income',
                data: incomeData,
                backgroundColor: '#06ff4c', 
                borderColor: 'rgba(0, 128, 0, 1)',
                borderWidth: 1,
                borderRadius: 7
            },
            {
                label: 'Max Expenses',
                data: expenseData, 
                backgroundColor: '#dc3f4d',
                borderColor: 'rgba(128, 0, 0, 1)',
                borderWidth: 1,
                borderRadius: 7
            },
        ],
    },
    options: {
        devicePixelRatio: 4,
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom',
                align: 'center',
                labels: {
                    usePointStyle: true,
                    color: '#ffffff',
                },
            },
            title: {
                display: false,
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return formatCurrency(context.raw, currencySign);
                    }
                }
            }
        },
        layout: {
            padding: {
                left: 5,
                right: 5,
                bottom: 70
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#ffffff',
                    font: {
                        size: 14
                    } 
                },
                grid: {
                    display: false 
                }
            },
            y: {
                beginAtZero: true,
                suggestedMin: 0, 
                suggestedMax: 500,
                ticks: {
                    font: {
                        size: 14
                    },
                    color: '#ffffff',
                    callback: (value) => formatCurrency(value, currencySign)
                },
                grid: {
                    display: false 
                }
            },
        },
    },
    plugins: [],
    devicePixelRatio: window.devicePixelRatio
});

const sourceEl = document.getElementById('sourceChart');
const sourceCtx = sourceEl.getContext('2d');
const sourceLabels = JSON.parse(sourceEl.getAttribute("data-source-labels") || '[]');
const sourceTotals = JSON.parse(sourceEl.getAttribute("data-source-totals") || '[]');

// Combine labels and totals into a single array of objects
const categories = sourceLabels.map((label, index) => ({
    label,
    value: sourceTotals[index],
}));

// Sort categories by value (highest to lowest)
categories.sort((a, b) => b.value - a.value);

// Limit to the top 8 categories
const maxCategories = 7;
const limitedCategories = categories.slice(0, maxCategories);

// Split sorted and limited categories back into labels and totals
const sortedAndLimitedLabels = limitedCategories.map(category => category.label);
const sortedAndLimitedTotals = limitedCategories.map(category => category.value);

// Dynamically adjust canvas width
const canvas = document.getElementById('sourceChart');
const minWidth = 100; // Minimum width for the canvas
const barWidth = 70; // Width per bar 
let maxWidth;
if (sourceLabels.length){
    maxWidth = Math.max(minWidth, sourceLabels.length * (barWidth + 10));
} else {
    maxWidth = Math.max(minWidth, 4 * (barWidth + 10));
}
canvas.style.maxWidth = `${maxWidth}px`;

const sourceData = sortedAndLimitedTotals.length
    ? {
        labels:  sortedAndLimitedLabels,
        datasets: [{
            label: 'Income Amount',
            data: sortedAndLimitedTotals,
            backgroundColor: [
                '#06ff4c',
                '#dc3f4d',
                '#fbbc16',
                '#45aaf2',
                '#8E1BE0',
                '#E0D12D',
                '#E12ECB',
                '#45DBE0'
            ],
            borderWidth: 0,
            borderRadius: 7,
            maxBarThickness: 60,
        }]
    } 
    : {
        labels:  ["No data 1", "No Data 2", "No Data 3", "No Data 4"],
        datasets: [{
            label: 'Income Amount',
            data: [6, 4, 3, 2],
            backgroundColor: ['#cccccc', '#aaaaaa', '#999999', '#666666'],
            borderWidth: 0,
            borderRadius: 7,
            maxBarThickness: 60,
        }]
    }

const sourceChart = new Chart(sourceCtx, {
    type: 'bar',
    data: sourceData,
    options: {
        devicePixelRatio: 4,
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return formatCurrency(context.raw, currencySign)
                    }
                }
            },
        },
        layout: {
            padding: {
                bottom: 70
            },
        },
        scales: {
            x: {
                ticks: {
                    color: '#ffffff',
                    font: {
                        size: 14
                    } 
                },
                grid: {
                    display: false
                },
            },
            y: {
                border: {
                    display: false,
                },
                beginAtZero: true,
                ticks: {
                    display: false
                },
                grid: {
                    display: false
                },
            },
        },
    }
});

const categoryEl = document.getElementById('categoryChart');
const categoryCtx = categoryEl.getContext('2d');
const categoryLabels = JSON.parse(categoryEl.getAttribute("data-category-labels"));
const categoryTotals = JSON.parse(categoryEl.getAttribute("data-category-totals"));

// Check if there is no data
const allZeros = categoryTotals.length === 0 || categoryTotals.every(total => total === 0);

// Define chart data based on the presence of data
const chartData = allZeros
? {
    labels: ['No Data'], 
    datasets: [{
        label: 'Expense Amount',
        data: [1],
        backgroundColor: ['#cccccc'],
        borderWidth: 0,
    }]
}
: {
    labels: categoryLabels,
    datasets: [{
        label: 'Income Amount',
        data: categoryTotals,
        backgroundColor: [
            '#06ff4c',
            '#dc3f4d',
            '#fbbc16',
            '#45aaf2',
            '#8E1BE0',
            '#E0D12D',
            '#E12ECB',
            '#45DBE0'
        ],
        borderWidth: 0,
    }]
};

const mobileScreen = window.innerWidth < 800;

// Create the pie chart
const categoryChart = new Chart(categoryCtx, {
    type: 'doughnut',
    data: chartData, 
    options: {
        devicePixelRatio: 4,
        maintainAspectRatio: false,
        responsive: true,
        layout: {
            padding: {
                bottom: 70, 
                left: mobileScreen? 70: 100, 
                right: mobileScreen? 70: 100
            },
        },
        plugins: {
            legend: {
                display: true, 
                position: mobileScreen? 'bottom': 'left',
                labels: {
                    color: '#fff',
                    font: {
                        size: 16,
                    },
                },
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        const label = context.label || '';
                        const value = context.raw || 0;
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = ((value / total) * 100).toFixed(2);
                        return allZeros
                            ? label 
                            : `${label}: ${formatCurrency(value, currencySign)} (${percentage}%)`;
                    },
                },
            },
        },
        cutout: '50%',
    },
});