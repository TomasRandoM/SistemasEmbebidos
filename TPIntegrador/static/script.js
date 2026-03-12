var channel = 1;
document.addEventListener("DOMContentLoaded", () => {
    
    fetch("http://192.168.1.6:3000/start")
    .then(res => res.json())
    .then(data => {
        channel = parseInt(data.id);
        document.getElementById("channel").innerText = data.id;
        document.getElementById("videoYT").src = data.video + "?autoplay=1&mute=0";
    });

    const socket = io("http://192.168.1.6:3000")

    socket.on("changeChannel", (data) => {
        channel = parseInt(data.id);
        document.getElementById("channel").innerText = data.id;
        document.getElementById("videoYT").src = data.video + "?autoplay=1&mute=0";
    });

    const buttonRight = document.getElementById("btnRight");

    buttonRight.addEventListener("click", function() {
        fetchChangeChannel(channel + 1)
    });

    const buttonLeft = document.getElementById("btnLeft");

    buttonLeft.addEventListener("click", function() {
        fetchChangeChannel(channel - 1)
    });
});

function fetchChangeChannel(newChannel) {
    fetch("http://192.168.1.6:3000/changeChannel/" + newChannel)
        .then(res => res.json())
        .then(data => {
            channel = parseInt(data.id);
            document.getElementById("channel").innerText = data.id;
            document.getElementById("videoYT").src = data.video + "?autoplay=1&mute=0";
        });
}
