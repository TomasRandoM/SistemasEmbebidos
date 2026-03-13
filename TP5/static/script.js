document.addEventListener("DOMContentLoaded", () => {
    
    function updatePlot() {
        fetch('/plot')
        .then(res => res.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            document.getElementById('ldrImg').src = url;
        });
    }
    updatePlot();
    setInterval(updatePlot, 6000);

})
