const doctor_id = sessionStorage.getItem("userId");
const accessToken = sessionStorage.getItem("token");
let params = new URLSearchParams(document.location.search);
const question_id = params.get("questionId");

async function postAnswer() {
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;
    const url = `http://0.0.0.0:8001/doctor/${doctor_id}/answer`;
    let body = JSON.stringify({
            question_id: question_id,
            title: title,
            content: content
        })

    // Make the first POST request
    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        },
        body: body
    })
        .then(async response => {
            if (response.status === 200) window.location.replace(`http://0.0.0.0:3001/single-question?questionId=${question_id}`);
            else throw new Error('Произошла ошибка. Попробуйте перезагрузить страницу.');
        })
        .catch(error => {
            alert(error.message)
        });
}