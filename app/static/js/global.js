console.log(
    "CLEANZO Global UI Loaded"
);


/* ===================================
FLASH AUTO HIDE
=================================== */

const flashMessages =
    document.querySelectorAll(
        ".flash-message"
    );

if (flashMessages.length > 0) {

    flashMessages.forEach((message) => {

        setTimeout(() => {

            message.style.opacity = "0";

            message.style.transform =
                "translateY(-10px)";

            setTimeout(() => {

                message.remove();

            }, 400);

        }, 3000);

    });

}


/* ===================================
MOBILE MENU
=================================== */

const mobileMenuButton =
    document.getElementById(
        "mobileMenuBtn"
    );

const navigationLinks =
    document.getElementById(
        "navLinks"
    );

if (
    mobileMenuButton &&
    navigationLinks
) {

    mobileMenuButton.addEventListener(
        "click",
        () => {

            navigationLinks.classList.toggle(
                "show-mobile-menu"
            );

        }
    );

}


/* ===================================
ACTIVE PAGE LOG
=================================== */

const activeNavigation =
    document.querySelector(
        ".active-nav"
    );

if (activeNavigation) {

    console.log(
        "Current Page:",
        activeNavigation.innerText
    );

}


/* ===================================
NAVBAR SHADOW ON SCROLL
=================================== */

const navbar =
    document.querySelector(
        ".navbar"
    );

window.addEventListener(
    "scroll",
    () => {

        if (!navbar) return;

        if (window.scrollY > 40) {

            navbar.style.boxShadow =
                "0px 8px 30px rgba(0,0,0,0.35)";

        }

        else {

            navbar.style.boxShadow =
                "none";

        }

    }
);


/* ===================================
PROFILE IMAGE FALLBACK
=================================== */

const profileImages =
    document.querySelectorAll(
        ".nav-profile-image"
    );

profileImages.forEach((image) => {

    image.addEventListener(
        "error",
        () => {

            image.src =
                "/static/images/default-profile.png";

        }
    );

});


console.log(
    "Navbar Ready"
);


/* ===================================
USER MENU DROPDOWN TOGGLE
=================================== */

const userMenuBtn = document.getElementById("userMenuBtn");
const userDropdown = document.getElementById("userDropdown");

if (userMenuBtn && userDropdown) {
    // Toggle dropdown on button click
    userMenuBtn.addEventListener("click", () => {
        userDropdown.classList.toggle("show");
        userMenuBtn.classList.toggle("active");
    });

    // Close dropdown when clicking outside
    document.addEventListener("click", (e) => {
        if (!userMenuBtn.contains(e.target) && !userDropdown.contains(e.target)) {
            userDropdown.classList.remove("show");
            userMenuBtn.classList.remove("active");
        }
    });

    // Close dropdown when clicking a link
    const dropdownItems = userDropdown.querySelectorAll(".dropdown-item");
    dropdownItems.forEach(item => {
        item.addEventListener("click", () => {
            userDropdown.classList.remove("show");
            userMenuBtn.classList.remove("active");
        });
    });
}