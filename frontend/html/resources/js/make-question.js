const patient_id = sessionStorage.getItem("userId");
const accessToken = sessionStorage.getItem("token");

async function postQuestion() {
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;
    const url = `http://0.0.0.0:8001/patient/${patient_id}/question`;
    let body = JSON.stringify({
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
            if (response.status === 200) window.location.replace("http://0.0.0.0:3001/questions");
            else throw new Error('Произошла ошибка. Попробуйте перезагрузить страницу.');
        })
        .catch(error => {
            alert(error.message)
        });
}