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

    const btnBusquedaUsuarios = document.querySelector(".btnBusquedaUsuarios")
    const btnCerrarFormBusqueda = document.querySelector(".btnCerrarFormBusqueda")
    const formBusqueda = document.getElementById("formBusqueda")
    const header = document.getElementById("header")

    let busquedaActiva = false

    if (header){
        header.addEventListener("mouseenter",function(){
            if (!busquedaActiva){
                header.style.width = "320px"
            }
        })
        header.addEventListener("mouseleave",function(){
            if (!busquedaActiva){
                header.style.width = "147px"
            }
        })
    }
    
    if(btnBusquedaUsuarios && header){
        btnBusquedaUsuarios.addEventListener("click",function(){
            formBusqueda.style.display = "flex"
            formBusqueda.style.flexDirection = "column"
            formBusqueda.style.alignItems = "center"
            formBusqueda.style.textAlign = "center"
            formBusqueda.style.justifyContent = "center"
            formBusqueda.style.gap = "10px"
            header.style.width = "410px"
            busquedaActiva = true
        })
    }

    if(btnCerrarFormBusqueda && header){
        btnCerrarFormBusqueda.addEventListener("click",function(){
            formBusqueda.style.display = "none"
            header.style.width = "147px"
            busquedaActiva = false
        })
    }
    
    const btnAbrirMenu = document.querySelector(".btnAbrirMenu")
    const btnCerrarMenu = document.querySelector(".btnCerrarMenu")

    if(btnAbrirMenu && header){
        btnAbrirMenu.addEventListener("click",function(){
            header.style.display = "flex"
            header.style.width = "200px"
        })
    }

    if(btnCerrarMenu && header){
        btnCerrarMenu.addEventListener("click",function(){
            header.style.display = "none"
        })
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

