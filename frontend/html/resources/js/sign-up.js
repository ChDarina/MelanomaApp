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
        if (document.getElementById("doctor") === checked) {
            loginUrl = "http://0.0.0.0:8000/user/";
            body = JSON.stringify({
                name: fullName,
                email: email,
                telephone: telephone,
                residence: residence,
                description: description,
                birthday_date: birthdayDate,
                password: password,
                confirm_password: passwordCheck
            })
        }
        if (document.getElementById("patient") === checked) {
            loginUrl = "http://0.0.0.0:8000/user/";
            body = JSON.stringify({
                name: fullName,
                email: email,
                telephone: telephone,
                residence: residence,
                birthday_date: birthdayDate,
                password: password,
                confirm_password: passwordCheck
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
                return (await response.json())["access_token"]
            })
            .then(async result => {
                token.set(result);
                // Make the second POST request
                return await fetch(`http://0.0.0.0:8000/user/me`, {
                    method: 'POST',
                    headers: {
                        'Authorization': 'Bearer ' + result
                    }
                })
            })
            .then(async response => {
                if (response.status !== 200) {
                    token.clearNow()
                    throw new Error('Регистрация не удалась. Попробуйте перезагрузить страницу');
                }
                return await response.json()
            })
            .then(async response => {
                sessionStorage.setItem('userId', response.id);
                setTimeout(() => {
                    window.location.replace("http://0.0.0.0:3000/index");
                }, 1000);
            })
            .catch(error => {
                alert(error.message)
            });
    }
}
