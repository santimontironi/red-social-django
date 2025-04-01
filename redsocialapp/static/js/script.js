document.addEventListener("DOMContentLoaded",function(){
    const contenedorSinInternet = document.querySelector(".contenedorSinInternet");
    const contenedorRegistro = document.getElementById("contenedorRegistro")
    const contenedorLogin = document.getElementById("contenedorLogin");

if(!navigator.onLine){
    if (contenedorLogin) contenedorLogin.style.display = "none"
    if (contenedorRegistro) contenedorRegistro.style.display = "none"
    if (contenedorSinInternet){
        contenedorSinInternet.classList.remove("d-none")
        contenedorSinInternet.classList.add("d-flex")
    }
}
})

