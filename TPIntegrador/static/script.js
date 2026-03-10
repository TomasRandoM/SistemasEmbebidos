document.addEventListener("DOMContentLoaded", () => {
    var channel = 1;

    fetch("http://127.0.0.1:3000/start")
    .then(res => res.json())
    .then(data => {
        document.getElementById("channel").innerText = data.id;
        document.getElementById("videoYT").src = data.video;
        console.log(data.video)
    });

    const socket = io("http://127.0.0.1:3000")

    socket.on("changeChannel", (data) => {
        //
    });
});