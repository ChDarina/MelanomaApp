async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const loginUrl = "http://0.0.0.0:8000/token";

    // Make the first POST request
    await fetch(loginUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            username: email,
            password: password
        })
    })
        .then(async response => {
            if (response.status !== 200) {
                throw new Error('Неверный email или пароль!');
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
}Ы