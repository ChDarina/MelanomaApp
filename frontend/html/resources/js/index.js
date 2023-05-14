let temp = sessionStorage.getItem("isDoctor")

if (temp === false) {
    let button = document.getElementById("analyse");
    button.hidden = false;
}