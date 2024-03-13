function toggleMenu() {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");
    menu.classList.toggle("open");
    icon.classList.toggle("open");
}


// Visitor Counter

const counter = document.querySelector("#visits");
async function updateCounter() {
    let visits = await (await fetch("https://q5miqidsndmldlh5jbdlfchhlq0gnkvk.lambda-url.us-east-1.on.aws")).json();
    document.querySelector("#visits").innerHTML = ` Visits: ${visits}`;
}

updateCounter();
