console.log("CLEANZO Dashboard Loaded");



/* ===================================
SERVICE CARD HOVER
=================================== */

const serviceCards =
document.querySelectorAll(
    ".service-card"
);


serviceCards.forEach(

    (card) => {

        card.addEventListener(

            "mouseenter",

            () => {

                card.style.transform =
                "translateY(-6px) scale(1.02)";

            }

        );


        card.addEventListener(

            "mouseleave",

            () => {

                card.style.transform =
                "translateY(0px) scale(1)";

            }

        );

    }

);




/* ===================================
BOTTOM NAV CLICK EFFECT
=================================== */

const navItems =
document.querySelectorAll(
    ".bottom-nav-item"
);


navItems.forEach(

    (item) => {

        item.addEventListener(

            "click",

            () => {

                navItems.forEach(

                    (nav) => {

                        nav.classList.remove(
                            "active-nav"
                        );

                    }

                );

                item.classList.add(
                    "active-nav"
                );

            }

        );

    }

);




/* ===================================
CARD FLOAT EFFECT
=================================== */

const dashboardCards =
document.querySelectorAll(
    ".dashboard-card"
);


dashboardCards.forEach(

    (card) => {

        card.addEventListener(

            "mouseenter",

            () => {

                card.style.transform =
                "translateY(-6px)";

            }

        );


        card.addEventListener(

            "mouseleave",

            () => {

                card.style.transform =
                "translateY(0px)";

            }

        );

    }

);




/* ===================================
BUTTON EFFECT
=================================== */

const scheduleBtn =
document.querySelector(
    ".schedule-btn"
);


if(scheduleBtn){

    scheduleBtn.addEventListener(

        "mouseenter",

        () => {

            scheduleBtn.style.transform =
            "translateY(-4px) scale(1.03)";

        }

    );


    scheduleBtn.addEventListener(

        "mouseleave",

        () => {

            scheduleBtn.style.transform =
            "translateY(0px) scale(1)";

        }

    );

}




/* ===================================
WELCOME ANIMATION
=================================== */

window.addEventListener(

    "load",

    () => {

        const container =
        document.querySelector(
            ".dashboard-container"
        );

        if(container){

            container.style.opacity =
            "0";

            container.style.transform =
            "translateY(20px)";

            setTimeout(() => {

                container.style.transition =
                "0.8s ease";

                container.style.opacity =
                "1";

                container.style.transform =
                "translateY(0px)";

            }, 100);

        }

    }

);




/* ===================================
MOBILE DETECTION
=================================== */

if(window.innerWidth < 768){

    console.log(
        "Mobile Dashboard Active"
    );

}else{

    console.log(
        "Desktop Dashboard Active"
    );

}