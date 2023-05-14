const userId = sessionStorage.getItem("userId");

// If user_id is undefined, redirect to the login page
if (!userId && window.location.pathname !== "/login" && window.location.pathname !== "/sign-up") {
    window.location.replace("http://0.0.0.0:3000/login");
    alert("Вы не вошли в аккаунт");
}
else if (userId && (window.location.pathname === "/login" || window.location.pathname === "/sign-up")){
    window.location.replace("http://0.0.0.0:3000/index");
}