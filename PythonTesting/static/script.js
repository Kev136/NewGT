
const socket = io(); // Establish a connection to the server

let myChart; // Declare the chart variable outside the function

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
// Listen for "cost_update" events from the server
socket.on("cost_update", function (data) {
    console.log("Cost update received:", data);
    if (myChart) {
        addData(data.climate_type, data.cost, data.time);
    }
});


// Initial fetch of data to populate the chart
fetch('/cost_data')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        initializeChart(data);
    });



// For slider code
const slider = document.getElementById('slider');
const sliderBar = document.getElementById('slider-bar');
const sliderIndicator = document.getElementById('slider-indicator');

sliderBar.style.width = slider.value + '%';
sliderIndicator.innerText = slider.value + '%';

slider.addEventListener('input', () => {
    sliderBar.style.width = slider.value + '%';
    sliderIndicator.innerText = slider.value + '%';
});

sliderBar.addEventListener('mousedown', (event) => {
    const shiftX = event.clientX - sliderBar.getBoundingClientRect().left;

    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);

    function onMouseMove(event) {
        let newWidth = event.clientX - shiftX - slider.getBoundingClientRect().left;

        if (newWidth < 0) {
            newWidth = 0;
        } else if (newWidth > slider.clientWidth) {
            newWidth = slider.clientWidth;
        }

        sliderBar.style.width = newWidth + 'px';
        slider.value = Math.round((newWidth / slider.clientWidth) * 100);
        sliderIndicator.innerText = slider.value + '%';
    }

    function onMouseUp() {
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    }
});


// For slider code
document.getElementById('slider').addEventListener('change', function (event) {
    const sliderValue = parseInt(event.target.value); // Convert value to integer
    fetch('/update_cost_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            percentage: sliderValue
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Log the response from the server
            // Handle the response as needed
        })
        .catch(error => {
            console.error('Error:', error);
        });
});