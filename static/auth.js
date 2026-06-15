// Login Validation

function validateLogin() {

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    if (email.trim() === "") {

        alert("Enter Email");

        return false;
    }

    if (password.trim() === "") {

        alert("Enter Password");

        return false;
    }

    return true;
}

// Signup Validation

function validateSignup() {

    const name =
        document.getElementById("name").value;

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    const role =
        document.getElementById("role").value;

    if (name.trim() === "") {

        alert("Enter Name");

        return false;
    }

    if (email.trim() === "") {

        alert("Enter Email");

        return false;
    }

    if (password.length < 6) {

        alert(
            "Password must contain at least 6 characters"
        );

        return false;
    }

    if (role === "") {

        alert("Select Role");

        return false;
    }

    return true;
}