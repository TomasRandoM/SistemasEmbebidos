const socket = io("http://192.168.1.34:3000");

socket.on("connect", () => {
    fetch("http://192.168.1.34:3000/start");
});

document.addEventListener("DOMContentLoaded", () => {

socket.on("alarm", (data) => {
    if (data.state) {
        document.getElementById("alarma").className = "alarm on";
        document.getElementById("alarma").innerText = "Alarma activada. Persona en la puerta.";
    }
    else {
        document.getElementById("alarma").className = "alarm off";
        document.getElementById("alarma").innerText = "Alarma desactivada";
    }
});

socket.on("people", (data) => {
    document.getElementById("people").innerText = data.quantity;
});

socket.on("person", (data) => {
    if (data.state) {
        document.getElementById("circle").style.backgroundColor = "red";
    } else {
        document.getElementById("circle").style.backgroundColor = "green";
    }
})

})

function borrarContador() {
    fetch("http://192.168.1.34:3000/erase");
    document.getElementById("people").innerText = 0;
}
