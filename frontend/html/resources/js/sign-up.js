function isDoctor() {
    document.getElementById("description").hidden = false;
}
function isPatient() {
    document.getElementById("description").hidden = true;
}

async function signUp() {
    const fullName = document.getElementById("fullName").value;
    const email = document.getElementById("email").value;
    const telephone = document.getElementById("telephone").value;
    const residence = document.getElementById("residence").value;
    const description = document.getElementById("description").value;
    const birthdayDate = document.getElementById("birthdayDate").value;
    const password = document.getElementById("password").value;
    const passwordCheck = document.getElementById("passwordCheck").value;
    if (passwordCheck !== password) {
        alert("Пароли не совпадают!")
    } else {
        let body, loginUrl;
        if (document.getElementById("description").hidden === false) {
            loginUrl = "http://0.0.0.0:8001/doctor/";
            body = JSON.stringify({
                name: fullName,
                email: email,
                telephone: telephone,
                residence: residence,
                description: description,
                birthday_date: birthdayDate,
                password: password,
                confirm_password: passwordCheck,
                photo_id: 10,
                work_years: 0
            })
        }
        if (document.getElementById("description").hidden === true) {
            loginUrl = "http://0.0.0.0:8001/patient/";
            body = JSON.stringify({
                name: fullName,
                email: email,
                telephone: telephone,
                residence: residence,
                birthday_date: birthdayDate,
                password: password,
                confirm_password: passwordCheck,
                photo_id: 10,
                status_id: 1
            })
        }

        // Make the first POST request
        await fetch(loginUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: body
        })
            .then(async response => {
                if (response.status === 400) {
                    throw new Error('Регистрация не удалась. Проверьте введённые данные');
                } else if (response.status === 403) {
                    throw new Error('Регистрация не удалась. Пользователь с данной электронной почтой уже зарегистрирован -- попробуйте зайти');
                }
                else if (response.status !== 200) {
                    throw new Error(response.body)
                }
                return await response.json()
            })
            .then(async response => {
                sessionStorage.setItem('userId', response.id);
                sessionStorage.setItem('token', response.access_token);
                sessionStorage.setItem('isDoctor', response.is_doctor);
                setTimeout(() => {
                    window.location.replace("http://0.0.0.0:3001/index");
                }, 1000);
            })
            .catch(error => {
                alert(error.message)
            });
    }
}
