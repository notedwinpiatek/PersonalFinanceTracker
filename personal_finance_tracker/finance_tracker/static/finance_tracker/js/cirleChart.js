import { formatCurrency } from "./utils.js";


export function cirleChart(labelNames, totals, context, currencySign){
    // Check if there is no data
    const allZeros = totals.length === 0 || totals.every(total => total === 0);
    
    // Define chart data based on the presence of data
    const chartData = allZeros
        ? {
            labels: ['No Data Available'], 
            datasets: [{
                label: `Expense Amount`,
                data: [1],
                backgroundColor: ['#cccccc'],
                borderWidth: 0,
            }]
        }
        : {
            labels: labelNames,
            datasets: [{
                label: 'Income Amount',
                data: totals,
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
    
    // Create the pie chart
    const categoryChart = new Chart(context, {
        type: 'pie',
        data: chartData, 
        options: {
            devicePixelRatio: 4,
            responsive: true,
            plugins: {
                legend: {
                    display: true, 
                    position: 'bottom',
                    labels: {
                        color: '#fff',
                        font: {
                            size: 14,
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
                                : `${label}: ${formatCurrency(value.toLocaleString(), currencySign)} (${percentage}%)`;
                        },
                    },
                },
            },
        },
    });
}