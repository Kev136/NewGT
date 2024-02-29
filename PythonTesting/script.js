function initializeChart(data) {
    const ctx = document.getElementById('myChart').getContext('2d');
    const labels = Object.values(data)[0].map(item => new Date(item[0])); // Parse the dates

    const datasets = Object.entries(data).map(([climate_type, cost_data]) => ({
        label: climate_type,
        data: cost_data.map(item => ({ x: new Date(item[0]), y: item[1] })),
        fill: false,
    }));

    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets,
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'hour',
                        displayFormats: {
                            hour: 'HH:mm'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Cost'
                    }
                }
            }
        }
    });
}

function addData(climate_type, cost, time) {
    const datasetIndex = myChart.data.datasets.findIndex(ds => ds.label === climate_type);
    if (datasetIndex !== -1) {
        myChart.data.datasets[datasetIndex].data.push({ x: new Date(time), y: cost });
        myChart.update();
    }
}