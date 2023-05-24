const predictSessionId = sessionStorage.getItem("predict_session_id")
const accessToken = sessionStorage.getItem("token")
const fetchOptions = {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + accessToken
    }
};
fetch(`http://0.0.0.0:8001/predict_session/${predictSessionId}/predict`, fetchOptions)
    .then(async response => {
        if (response.status !== 200)
            throw new Error('Произошла ошибка при анализе изображения! Попробуйте выполнить анализ еще раз')
        return await response.json()
    })
    .then(data => {
        console.log(data)
        let resultStatus = document.getElementById("resultStatus");
        let resultAction = document.getElementById("resultAction");
        let displayed_score = (parseFloat(data.predict_score) * 100).toFixed(2) + '%'

        if (data.status_name === "здоров" || data.status_name === "неизвестен")
            resultStatus.innerHTML += `С вероятностью ` + displayed_score + ` вы здоровы`;
        else
            resultStatus.innerHTML += `С вероятностью ` +  displayed_score + ` у вас ` + data.status_name;
        resultAction.innerHTML = `<p class="font-weight-bold">Важно!</p>
    <p>Этот инструмент предназначен для пред-диагностики и не может служить основанием для постановки диагноза.</p>
    <p>В случае опасения насчёт того или иного заболевания рекомендуем вам обратиться к специалисту</p>
    <a class="btn btn-outline-dark btn-rounded" href="http://0.0.0.0:3001/doctors">Просмотреть врачей</a>`;
    })
    .catch(error => {
        // Handle the error
        console.error(error);
        responseElement.innerText = "Произошла ошибка при загрузке результата. Попробуйте позднее";
    });