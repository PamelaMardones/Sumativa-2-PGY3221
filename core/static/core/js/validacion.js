const form = document.getElementById("form")
const nombre = document.getElementById("inputName")
const email = document.getElementById("emailInput")
const contraseña = document.getElementById("inputPass")
const contraseña2 = document.getElementById("inputPass2")
const parrafo = document.getElementById("warnings")

form.addEventListener("submit", e=>{
    e.preventDefault()
    let warnings = ""
    let entrar = false
    let regexEmail = /^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,4})+$/
	let regexNombre = /^[A-ZÑa-zñáéíóúÁÉÍÓÚ'° ]+$/
	if(!regexNombre.test(nombre.value)){
		warnings += '* El nombre no es válido. <br>'
		entrar = true
	}
    let regexPass = /^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{6,18}$/
    parrafo.innerHTML = ""


    if(!regexEmail.test(email.value)){
        warnings += `* El email no es válido. <br>`
        entrar = true
    }

	if(!regexPass.test(contraseña.value)){
        warnings += `* La contraseña debe tener entre 6 y 18 caracteres, incluyendo mayúsculas, números  y caracteres especiales. <br>`
        entrar = true
    }
    if(!regexPass.test(contraseña2.value)){
        warnings += `* La contraseña debe tener entre 6 y 18 caracteres, incluyendo mayúsculas, números  y caracteres especiales. <br>`
        entrar = true
    }

    if(entrar){
        parrafo.innerHTML = warnings
    }else{
        parrafo.innerHTML = "Registro exitoso!"
        alert("Registro exitoso!");
        window.location.href = "index.html";        
    }

})