function toggleMenu() {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");
    menu.classList.toggle("open");
    icon.classList.toggle("open");
}

const pageviewsCount = document.getElementsByClassName('pageviews-count');
const visitsCount = document.getElementsByClassName('visits - count');

if (sessionStorage.getItem('visit') === null) {
    //New visit and pageview
    updateCounter('type=visit-page-view');
} else {
    //Pageview
    updateCounter('type=pageview');
}

function updateCounter() {
    fetch('https://www.theprojectfolder.com/?' + type)
        .then(res => res.json())
        .then(data => {
            pageviewsCount.textContent = data.pageviews;
            visitsCount.textContent = data.visits;
        })
}

sessionStorage.setItem('visit', 'x');
