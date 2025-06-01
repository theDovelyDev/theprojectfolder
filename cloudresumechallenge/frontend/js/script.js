function toggleMenu() {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");
    menu.classList.toggle("open");
    icon.classList.toggle("open");
}


// Visitor Counter
fetch('https://o7vctu4eiznpqfiu4kzc6iaxw40jaczm.lambda-url.us-east-1.on.aws/')
    .then(response => response.json())
    .then(data => {
        document.getElementById("visitCounter").textContent = data["visitorcount"];
    })