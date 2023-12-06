document.addEventListener('DOMContentLoaded', function() {
    checkIsLogged();
});

async function checkIsLogged(){
    const access_token = localStorage.getItem("access_token");
    if(!access_token){
        window.location.href = '/login'
    }
}