function toggleMenu() {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");
    menu.classList.toggle("open");
    icon.classList.toggle("open");
}


// Visitor Counter
function updateCounter() {
    let data = fetch("https://bibrxksugh6draq2bukj2ai4ai0qqtfo.lambda-url.us-east-1.on.aws/").json();
    const counter = document.getElementsByClassName(".visit-count");
    counter.innerHTML = `${data}`;
}

updateCounter();