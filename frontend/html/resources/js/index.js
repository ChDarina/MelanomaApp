const isDoctor = sessionStorage.getItem("isDoctor");
let button = document.getElementById("action");

if (isDoctor === "false") {
    button.href = "http://0.0.0.0:3001/image-download";
    button.innerHTML = "Провериться";
}
else {
    button.href = "http://0.0.0.0:3001/appointments";
    button.innerHTML = "Просмотреть мои приёмы";
}

button.hidden = false;