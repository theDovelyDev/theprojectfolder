function toggleMenu() {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");
    menu.classList.toggle("open");
    icon.classList.toggle("open");
}


// Visitor Counter
function fetch('https://aqj1luijr1.execute-api.us-east-1.amazonaws.com/dev')
    .then(response => response.json())
    .then(data => {
        document.getElementById("visitCounter").textContent = data.body.visitcount;
    })