function toggleMenu() {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");
    menu.classList.toggle("open");
    icon.classList.toggle("open");
}

const counter = document.querySelector(".visit-counter");
async function updateCounter() {
    let response = await fetch("https://q5miqidsndmldlh5jbdlfchhlq0gnkvk.lambda-url.us-east-1.on.aws/");
    let data = await response.json();
    counter.innerHTML = '${data} Visits';
}

updateCounter();
