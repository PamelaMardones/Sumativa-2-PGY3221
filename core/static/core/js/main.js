$(document).ready(function(){
    $('.navbar-nav>li>a').on('click', function(){
        $('.navbar-collapse').collapse('hide');
    });

    $('#login').submit(function(event) {
        event.preventDefault();
        var email = $('#email').val();
        var password = $('#password').val();
        
        if (!isValidEmail(email)) {
            alert('El email no esta en un formato válido.');
            return;
        }

        if (!isValidPassword(password)) {
            alert('La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula, un número y un carácter especial.');
            return;
        }

        let link = $('#userText');
        
        if (email == null) {
            link.innerHTML = "Bienvenido, Invitado";
            return;
        }
        
        // Actualizamos el texto utilizando innerHTML
        link.innerHTML = "Bienvenido, " + email;
        
        $('#modalLogin').modal('hide');
    });
  });


function isValidPassword(password) {
    var minLength = 8;
    var maxLength = 16;
    var hasUpperCase = /[A-Z]/.test(password);
    var hasLowerCase = /[a-z]/.test(password);
    var hasNumbers = /\d/.test(password);
    var hasSpecialChars = /[@#\$%\^&\*]/.test(password);

    if (password.length < minLength || password.length > maxLength) {
        return false;
    }

    if (!(hasUpperCase && hasLowerCase && hasNumbers && hasSpecialChars)) {
        return false;
    }

    return true;
}

function isValidEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}