// Feedback Form Validation

function validateFeedback() {

    const teacher =
        document.getElementById("teacher_name").value;

    const subject =
        document.getElementById("subject").value;

    const rating =
        document.getElementById("rating").value;

    if (teacher.trim() === "") {

        alert("Enter Teacher Name");

        return false;
    }

    if (subject.trim() === "") {

        alert("Enter Subject");

        return false;
    }

    if (rating === "") {

        alert("Select Rating");

        return false;
    }

    return true;
}

function previewRating() {

    let rating =
        document.getElementById("rating").value;

    document.getElementById(
        "ratingValue"
    ).innerText = rating;
}