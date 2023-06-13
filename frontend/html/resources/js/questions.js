const accessToken = sessionStorage.getItem("token");
const url = `http://0.0.0.0:3001/make-question`;

if (isDoctor === "false") {
    let button = document.getElementById("makeQuestion");
    button.href = url;
    button.hidden = false;
}

const fetchOptions = {
    method: 'GET'
};

fetch(`http://0.0.0.0:8001/question/`, fetchOptions)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        for (let i = 0; i < data.length; i++) {
            let item = data[i];
            addRow(item);
        }
    })
    .catch(error => {
        // Handle the error
        console.error(error);
        responseElement.innerText = "Произошла ошибка при загрузке страницы. Попробуйте позднее";
    });

function formatDatetime(datetimeStr) {
    const datetime = new Date(datetimeStr);
    const hours = String(datetime.getHours()).padStart(2, '0');
    const minutes = String(datetime.getMinutes()).padStart(2, '0');
    const day = String(datetime.getDate()).padStart(2, '0');
    const month = String(datetime.getMonth() + 1).padStart(2, '0');
    const year = datetime.getFullYear();

    return `${hours}:${minutes} ${day}.${month}.${year}`;
}

function addRow(item) {
    var table = document.getElementById("table");
    var row = table.insertRow();
    console.log(item)

    let questionUrl = `http://0.0.0.0:3001/single-question?questionId=${item.id}`;
    var cell = row.insertCell();
    cell.innerHTML = `<a href="` + "#" + ` " class="font-weight-bold blue-text">` + item.patient_name + `</a>`;
    cell = row.insertCell();
    cell.innerHTML = `<p class="font-weight-bold">` + item.title + `</p>`;
    cell = row.insertCell();
    cell.innerHTML = `<p class="font-weight-bold"> ` + item.answers_count + `</p >`;
    cell = row.insertCell();
    cell.innerHTML = `<p class="font-weight-bold"> ` + formatDatetime(item.datetime_created) + `</p >`;
    cell = row.insertCell();
    cell.innerHTML = `<a href="` + questionUrl + `">Читать далее...</a>`;
}