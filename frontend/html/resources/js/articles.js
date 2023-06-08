const accessToken = sessionStorage.getItem("token");
const url = `http://0.0.0.0:8000/make-article`;

if (isDoctor === "true") {
    let button = document.getElementById("makeArticle");
    button.href = url;
    button.hidden = false;
}

const fetchOptions = {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + accessToken
    }
};

fetch(`http://0.0.0.0:8001/article/`, fetchOptions)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        for (let i = 0; i < data.length; i++) {
            let item = data[i];
            addArticle(item);
        }
    })
    .catch(error => {
        // Handle the error
        console.error(error);
        responseElement.innerText = "Произошла ошибка при загрузке страницы. Попробуйте позднее";
    });

function addArticle(item) {
    let body = document.getElementById("ibody");
    let el = document.createElement();
    console.log(item)

    let articleUrl = `http://0.0.0.0:3001/single-article?articleId=${item.id}`;
    let articlePart = item.content.split('\n\n');
    el.innerHTML = `<article class="my-3" id="typography">
    <div class="bd-heading sticky-xl-top align-self-start mt-5 mb-3 mt-xl-0 mb-xl-2">
        <h3>`+ item.title + `</h3>
        <a class="d-flex align-items-center" href="`+ "#" + `">` + item.doctor_name + `</a>
        <p> Стаж: `+ item.work_years + `</p>
    </div>
    <div>
        <p>`+ articlePart[0] + `</p>
        <a class="d-flex align-items-center" href="`+ articleUrl + `">Читать далее...</a>
    </div>
    </article>`;
    body.appendChild(el);
}