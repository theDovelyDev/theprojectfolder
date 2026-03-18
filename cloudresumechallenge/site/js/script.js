// Hamburger Menu
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');

function toggleMenu() {
    const isOpen = hamburger.classList.toggle('open');
    navMenu.classList.toggle('open', isOpen);

    // ARIA for accessibility
    hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    navMenu.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
}

// Toggle on hamburger click
hamburger.addEventListener('click', toggleMenu);

// Close when a link is clicked (mobile)
navMenu.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
        hamburger.classList.remove('open');
        navMenu.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        navMenu.setAttribute('aria-hidden', 'true');
    });
});

// Visitor Counter
const functionUrl = "https://ligzkttonselfrpj5d3266qb7a0imnhp.lambda-url.us-east-1.on.aws/";

// Log helper
const logError = (msg, err) => {
    console.error(msg, err);
    document.getElementById("visitor_counter").innerText = "Visitor Count Unavailable";
};

// 1. Increment visitor count (POST)
fetch(functionUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    mode: "cors"
}).catch(err => logError("POST failed", err));

// 2. Fetch current visitor count (GET)
fetch(functionUrl, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    mode: "cors"
})
    .then(response => {
        if (!response.ok) throw new Error("Response not OK");
        return response.json();
    })
    .then(data => {
        if (data.visitorCount !== undefined) {
            document.getElementById("visitor_counter").innerText = data.visitorCount;
        } else {
            throw new Error("Missing visitorCount in response");
        }
    })
    .catch(err => logError("GET failed", err));

// Animate icons and cards when visible
document.addEventListener("DOMContentLoaded", function () {
    const observerOptions = { threshold: 0.1 };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                // Add visible class to icon immediately
                entry.target.classList.add('visible');

                // If the target is a cert-wrapper, fade in the name slightly after
                const certName = entry.target.querySelector('.cert-name');
                if (certName) {
                    setTimeout(() => {
                        certName.classList.add('visible');
                    }, 150); // delay in ms for name
                }

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // About Me section cards, icons, and cert wrappers
    const aboutElements = document.querySelectorAll(
        '.about-details-container, .icon-circle, .cert-wrapper'
    );
    aboutElements.forEach(el => observer.observe(el));

    // Experience section cards and icons
    const experienceElements = document.querySelectorAll(
        '.details-container, .details-container .icon-circle'
    );
    experienceElements.forEach(el => observer.observe(el));
});
