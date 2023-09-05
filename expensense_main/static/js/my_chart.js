// Function to create the expense chart
// Template taken from chart.js documentation
function createExpenseChart(expenses) {
    // unpack the expenses into labels and data
    var labels = Object.keys(expenses);
    var data = Object.values(expenses);

    // reverse both the lists
    labels.reverse();
    data.reverse()

    var ctx = document.getElementById('expenseChart').getContext('2d');
    var expenseChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Expense Amount',
                data: data,
                borderColor: 'rgba(35, 78, 112, 1)',
                tension: 0.2,
                backgroundColor: 'rgba(35, 78, 112, 0.4)',
                borderWidth: 2,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'category',
                    title: {
                        display: true,
                        text: 'Months'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Amount'
                    }
                }
            }
        }
    });
}
