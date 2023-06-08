const accessToken = sessionStorage.getItem("token");
let params = new URLSearchParams(document.location.search);
const articleId = params.get("articleId");

const fetchOptions = {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + accessToken
    }
};

fetch(`http://0.0.0.0:8001/article/${articleId}`, fetchOptions)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        addArticle(data);
    })
    .catch(error => {
        // Handle the error
        console.error(error);
        responseElement.innerText = "Произошла ошибка при загрузке страницы. Попробуйте позднее";
    });

function addArticle(item) {
    let body = document.getElementById("ibody");
    let el = document.createElement("article");
    console.log(item);

    el.innerHTML = `<div class="bd-heading sticky-xl-top align-self-start mt-5 mb-3 mt-xl-0 mb-xl-2">
        <h3>`+ item.title + `</h3>
        <a class="d-flex align-items-center" href="`+ "#" + `">` + item.doctor_name + `</a>
        <p> Стаж: `+ item.work_years + `</p>
    </div>
    <div>
        <p>`+ item.content + `</p>
    </div>`;
    body.appendChild(el);
}