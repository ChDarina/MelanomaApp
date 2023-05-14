const isDoctor = sessionStorage.getItem("isDoctor");

let navigation = `
<header class="p-3 mb-3 border-bottom">
<div class="container">
    <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
        <h3>
            <a href="http://0.0.0.0:3001/index"
                class="d-flex align-items-center mb-2 mb-lg-0 text-dark text-decoration-none"><b>SkinCancerApp</b></a>
        </h3>

        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
            <li><a href="http://0.0.0.0:3001/articles" class="nav-link px-2 link-dark">Статьи</a></li>
            <li><a href="http://0.0.0.0:3001/questions" class="nav-link px-2 link-dark">Вопросы</a></li>
            `

if (isDoctor === 'false') navigation += `<li><a href="http://0.0.0.0:3001/image-download" class="nav-link px-2 link-dark">Провериться</a></li>`

navigation += `
            <li><a href="http://0.0.0.0:3001/doctors" class="nav-link px-2 link-dark">Врачи</a></li>
        </ul>
        `

if (window.location.pathname == "/articles" || window.location.pathname == "/questions"
|| window.location.pathname == "/doctors" || window.location.pathname == "/appointments")
    navigation += `
        <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3">
            <input type="search" class="form-control" placeholder="Поиск..." aria-label="Search">
        </form>
        `

navigation += `
        <div class="dropdown text-end">
            <a href="#" class="d-block link-dark text-decoration-none dropdown-toggle" id="dropdownUser1"
                data-bs-toggle="dropdown" aria-expanded="false">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                    <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
                    <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"/>
                  </svg>
            </a>
            <ul class="dropdown-menu text-small" aria-labelledby="dropdownUser1">
                <li><a class="dropdown-item" href="http://0.0.0.0:3001/profile">Профиль</a></li>
                <li><a class="dropdown-item" href="#">Настройки</a></li>
                <li><a class="dropdown-item" href="http://0.0.0.0:3001/appointments">Мои приёмы</a></li>
                <li>
                    <hr class="dropdown-divider">
                </li>
                <li><button class="dropdown-item" onclick="logout()">Выйти</button></li>
            </ul>
        </div>
    </div>
</div>
</header>
`
document.body.insertAdjacentHTML("afterbegin", navigation)

function logout() {
    sessionStorage.clear();
    alert("Вы вышли из аккаунта");
    window.location.replace("http://0.0.0.0:3001/login");
}