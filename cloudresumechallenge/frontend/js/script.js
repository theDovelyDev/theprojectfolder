function toggleMenu() {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");
    menu.classList.toggle("open");
    icon.classList.toggle("open");
}


// Visitor Counter
fetch('https://pyfq5y2b4j.execute-api.us-east-1.amazonaws.com/default/VisitorCounter')
    .then(response => response.json())
    .then(data => {
        document.getElementById("visitCounter").textContent = data["visitorcount"];
    })