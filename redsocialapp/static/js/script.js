document.addEventListener("DOMContentLoaded",function(){
    const contenedorSinInternet = document.querySelector(".contenedorSinInternet")
    const contenedorRegistro = document.getElementById("contenedorRegistro")
    const contenedorLogin = document.getElementById("contenedorLogin");
    const contenedorCrearPerfil = document.querySelector(".contenedorCrearPerfil")
    const contenedorInicio = document.querySelector(".contenedorInicio")
    const contenedorAgregarPublicacion = document.querySelector(".contenedorAgregarPublicacion")
    const contenedorMiPerfil = document.querySelector(".contenedorMiPerfil")
    const contenedorBusquedaUsuarios = document.querySelector(".contenedorBusquedaUsuarios")
    const contenedorMisAmigos = document.querySelector(".contenedorMisAmigos")

    if(!navigator.onLine){
        if (contenedorLogin) contenedorLogin.style.display = "none"
        if (contenedorRegistro) contenedorRegistro.style.display = "none"
        if (contenedorCrearPerfil) contenedorCrearPerfil.style.display = "none"
        if (contenedorInicio) contenedorInicio.style.display = "none"
        if (contenedorMiPerfil) contenedorMiPerfil.style.display = "none"
        if (contenedorMisAmigos) contenedorMisAmigos.style.display = "none"
        if (contenedorAgregarPublicacion) contenedorAgregarPublicacion.style.display = "none"
        if (contenedorBusquedaUsuarios) contenedorBusquedaUsuarios.style.display = "none"
        if (contenedorSinInternet){
            contenedorSinInternet.classList.remove("d-none")
            contenedorSinInternet.classList.add("d-flex")
        }
    }
    //Los if para cada contenedor sirven para asegurarse de que los elementos existen en el DOM antes de intentar modificar sus estilos.

    const header = document.getElementById("header")
    const btnAbrirMenu = document.querySelector(".btnAbrirMenu")
    const btnCerrarMenu = document.querySelector(".btnCerrarMenu")

    header.addEventListener("mouseover",function(){
        header.classList.add("abierto")
    })

    header.addEventListener("mouseleave",function(){
        header.classList.remove("abierto")
    })

    if(btnAbrirMenu && header){
        btnAbrirMenu.addEventListener("click",function(){
            header.style.display = "flex"
            header.style.width = "150px"
            header.classList.remove("abierto")
        })
    }

    if (btnCerrarMenu && header) {
        btnCerrarMenu.addEventListener("click", function () {
            header.style.animation = "cerrarMenu 0.3s ease-in-out forwards";
            
            // Esperar a que termine la animación para ocultar el menú
            header.addEventListener("animationend",function(){
                header.style.display = "none";
                // Resetear la animación para la próxima apertura
                header.style.animation = "";
            },{once:true}) //asegura que el evento animationend solo se ejecute una vez al cerrar el menú, y luego el listener se elimina automáticamente.
        });
    }
    
    const btnOlvidarClave = document.querySelector(".btnOlvidarClave")
    const contenedorCambiarClave = document.getElementById("contenedorCambiarClave")
    const btnCerrarContenedorCambiarClave = document.querySelector(".btnCerrarContenedorCambiarClave")

    if(btnOlvidarClave && contenedorCambiarClave){
        btnOlvidarClave.addEventListener("click",function(){
            contenedorCambiarClave.style.display = "flex"
        })
    }

    if(btnCerrarContenedorCambiarClave && contenedorCambiarClave){
        btnCerrarContenedorCambiarClave.addEventListener("click",function(){
            contenedorCambiarClave.style.display = "none"
        })
    }
})

