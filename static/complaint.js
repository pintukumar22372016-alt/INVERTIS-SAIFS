// Complaint Validation

function validateComplaint() {

    const title =
        document.getElementById("title").value;

    const description =
        document.getElementById("description").value;

    if (title.trim() === "") {

        alert("Please Enter Complaint Title");

        return false;
    }

    if (description.trim() === "") {

        alert("Please Enter Complaint Description");

        return false;
    }

    if (description.length < 10) {

        alert(
            "Complaint description must contain at least 10 characters."
        );

        return false;
    }

    return true;
}

function clearComplaintForm() {

    document.getElementById("title").value = "";
    document.getElementById("description").value = "";

}