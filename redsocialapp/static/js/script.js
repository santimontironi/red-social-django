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
})

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

//Bloque de codigo para mostrar el formulario de busqueda de usuarios.

const btnBusquedaUsuarios = document.querySelector(".btnBusquedaUsuarios")
const formBusqueda = document.getElementById("formBusqueda")
const header = document.getElementById("header")

btnBusquedaUsuarios.addEventListener("click",function(){
    formBusqueda.classList.toggle("formBusquedaAbierto")

    if (formBusqueda.classList.contains("formBusquedaAbierto")){
        formBusqueda.style.display = "none"
        header.style.width = "147px"
    }else{
        formBusqueda.style.display = "flex"
        formBusqueda.style.flexDirection = "column"
        formBusqueda.style.alignItems = "center"
        formBusqueda.style.justifyContent = "center"
        formBusqueda.style.gap = "6px"
        header.style.width = "380px"
    }
})
