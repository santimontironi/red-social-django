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

    //variable de control para saber si el formulario de busqueda esta activo o no.
    let busquedaActiva = false

    //El evento mouseover se activa cuando el mouse entra en el area del elemento, y el evento mouseout se activa cuando el mouse sale del area del elemento.
    //Esto permite que el header se expanda cuando el mouse entra en el area del elemento, y se contraiga cuando el mouse sale del area del elemento, pero solo si el formulario de busqueda no esta activo.
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
    
    //El evento click se activa cuando el usuario hace click en el elemento.
    //Esto permite que el header se expanda cuando el usuario hace click en el elemento.
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

    //El evento click se activa cuando el usuario hace click en el elemento.
    //Esto permite que el header se contraiga cuando el usuario hace click en el elemento.
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
})

