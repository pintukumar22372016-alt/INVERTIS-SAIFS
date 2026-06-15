// Dashboard Functions

document.addEventListener("DOMContentLoaded", () => {

    const counters = document.querySelectorAll(".counter");

    counters.forEach(counter => {

        const target = Number(counter.innerText);

        let count = 0;

        const updateCounter = () => {

            if (count < target) {

                count++;

                counter.innerText = count;

                setTimeout(updateCounter, 20);
            }
        };

        updateCounter();

    });

});

function showWelcome() {

    alert("Welcome to  Invertis SAIFS Dashboard");

}