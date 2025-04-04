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

    //Bloque de codigo para mostrar el contenedor de agregar comentarios en una publicacion.

    const btnComentario = document.getElementById("btnComentario")
    const contenedorComentario = document.getElementById("contenedorComentario")
    const btnCerrarComentario = document.querySelector(".btnCerrarComentario")

    btnComentario.addEventListener("click",function(){
        contenedorComentario.style.display = "flex"
    })

    btnCerrarComentario.addEventListener("click",function(){
        contenedorComentario.style.display = "none"
    })


    const btnBusquedaUsuarios = document.querySelector(".btnBusquedaUsuarios")
    const btnCerrarFormBusqueda = document.querySelector(".btnCerrarFormBusqueda")
    const formBusqueda = document.getElementById("formBusqueda")
    const header = document.getElementById("header")

    //variable de control para saber si el formulario de busqueda esta activo o no.
    let busquedaActiva = false

    //El evento mouseover se activa cuando el mouse entra en el area del elemento, y el evento mouseout se activa cuando el mouse sale del area del elemento.
    //Esto permite que el header se expanda cuando el mouse entra en el area del elemento, y se contraiga cuando el mouse sale del area del elemento, pero solo si el formulario de busqueda no esta activo.
    if (header){
        header.addEventListener("mouseover",function(){
            if (!busquedaActiva){
                header.style.width = "300px"
            }
        })
        header.addEventListener("mouseout",function(){
            if (!busquedaActiva){
                header.style.width = "147px"
            }
        })
    }
    
    //El evento click se activa cuando el usuario hace click en el elemento.
    //Esto permite que el header se expanda cuando el usuario hace click en el elemento.
    if(btnBusquedaUsuarios){
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
    if(btnCerrarFormBusqueda){
        btnCerrarFormBusqueda.addEventListener("click",function(){
            formBusqueda.style.display = "none"
            header.style.width = "147px"
            busquedaActiva = false
        })
    }
    

})

