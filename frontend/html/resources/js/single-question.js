const accessToken = sessionStorage.getItem("token");
let params = new URLSearchParams(document.location.search);
const questionId = params.get("questionId");
const url = `http://0.0.0.0:3001/make-answer?questionId=${questionId}`;

if (isDoctor === "true") {
    let button = document.getElementById("makeAnswer");
    button.href = url;
    button.hidden = false;
}

const fetchOptions = {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + accessToken
    }
};

fetch(`http://0.0.0.0:8001/question/${questionId}`, fetchOptions)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        addQuestion(data);
    })
    .catch(error => {
        // Handle the error
        console.error(error);
        responseElement.innerText = "Произошла ошибка при загрузке страницы. Попробуйте позднее";
    });

fetch(`http://0.0.0.0:8001/question/${questionId}/answers`, fetchOptions)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        for (let i = 0; i < data.length; i++) {
            let item = data[i];
            addAnswer(item);
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

function addQuestion(item) {
    let body = document.getElementById("question");
    let el = document.createElement("article");
    console.log(item);

    el.innerHTML = `<div class="bd-heading sticky-xl-top align-self-start mt-5 mb-3 mt-xl-0 mb-xl-2">
            <h3>` + item.title + `</h3>
            <a class="d-flex align-items-center" href="` + "#" + `">` + item.patient_name + `</a>
            <p>Создано: ` + formatDatetime(item.datetime_created) + `</p>
        </div>
        <div>
            <p>` + item.content + `</p>
        </div>`;
    body.appendChild(el);
}

function addAnswer(item) {
    let body = document.getElementById("answers");
    let el = document.createElement("article");
    console.log(item);

    el.innerHTML = `<div class="bd-heading sticky-xl-top align-self-start mt-5 mb-3 mt-xl-0 mb-xl-2">
        <h3>` + item.title + `</h3>
        <a class="d-flex align-items-center" href="` + "#" + `">` + item.doctor_name + `</a>
        <p>Стаж: ` + item.work_years + ` лет</p>
        <p>Создано: ` + formatDatetime(item.datetime_created) + `</p>
    </div>
    <div>
        <p>` + item.content + `</p>
    </div>`;
    body.appendChild(el);
}
