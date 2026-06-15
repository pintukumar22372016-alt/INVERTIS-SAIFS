// Main JavaScript File

document.addEventListener("DOMContentLoaded", () => {

    console.log("Invertis SAIFS System Loaded Successfully");

    const cards = document.querySelectorAll(".card");

    cards.forEach(card => {

        card.addEventListener("mouseenter", () => {

            card.style.transform = "scale(1.02)";

        });

        card.addEventListener("mouseleave", () => {

            card.style.transform = "scale(1)";

        });

    });

});