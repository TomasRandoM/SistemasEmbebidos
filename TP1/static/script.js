document.addEventListener("DOMContentLoaded", () => {

    fetch("http://192.168.1.34:3000/getLedsValue")
    .then(res => res.json())
    .then(data => {
        Object.keys(data).forEach(key => {
            if(key === "led13") {
                document.getElementById(key).checked = data[key] === "1";
            }
            else {
                document.getElementById(key).innerText = data[key];
            }
        }
        )
    });
    
    const sliders = document.querySelectorAll(".slider");

    sliders.forEach(slider => {
        slider.addEventListener("change", function() {
            const id = this.id;
            const pin = id.replace("led", "");
            const value = this.value;
            if (pin != 13) {
                document.getElementById("brilloLed" + pin).innerText = parseInt(value * 255 / 100);
            }
            fetch("http://192.168.1.34:3000/changeLedValue", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: "pin=" + pin + "&valor=" + value
            });
        });
    });

    const checkbox = document.getElementById("led13");

    checkbox.addEventListener("change", () => {
        value = checkbox.checked ? 1 : 0;
        fetch("http://192.168.1.34:3000/changeLedValue", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: "pin=13" + "&valor=" + value
        });
    });
});

