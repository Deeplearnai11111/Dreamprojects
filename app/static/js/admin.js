console.log(
    "CLEANZO Enterprise Dashboard Loaded"
);


/* ===================================
GLOBAL SELECTORS
=================================== */

const menuButtons =
    document.querySelectorAll(
        ".sidebar-btn"
    );

const sections =
    document.querySelectorAll(
        ".admin-section"
    );

const adminSidebar =
    document.getElementById(
        "adminSidebar"
    );

const dynamicTitle =
    document.getElementById(
        "dynamicTitle"
    );

const mobileSidebarBtn =
    document.getElementById(
        "mobileSidebarBtn"
    );


/* ===================================
SECTION SWITCHING
=================================== */

menuButtons.forEach((button) => {

    button.addEventListener(
        "click",
        () => {

            /* REMOVE ACTIVE */

            menuButtons.forEach((btn) => {

                btn.classList.remove(
                    "active-menu"
                );

            });

            sections.forEach((section) => {

                section.classList.remove(
                    "active-section"
                );

            });


            /* ACTIVE */

            button.classList.add(
                "active-menu"
            );

            const target =
                button.dataset.section;

            const activeSection =
                document.getElementById(
                    target
                );

            if(activeSection){

                activeSection.classList.add(
                    "active-section"
                );

            }


            /* TITLE */

            if(dynamicTitle){

                dynamicTitle.innerText =
                    button.innerText.trim();

            }


            /* SAVE ACTIVE TAB */

            localStorage.setItem(
                "adminActiveSection",
                target
            );


            /* MOBILE CLOSE */

            if(adminSidebar){

                adminSidebar.classList.remove(
                    "show-sidebar"
                );

            }


            window.scrollTo({

                top:0,
                behavior:"smooth"

            });

        }
    );

});


/* ===================================
RESTORE ACTIVE SECTION
=================================== */

window.addEventListener(
    "load",
    () => {

        const savedSection =
            localStorage.getItem(
                "adminActiveSection"
            );

        if(savedSection){

            const targetButton =
                document.querySelector(
                    `[data-section="${savedSection}"]`
                );

            if(targetButton){

                targetButton.click();

            }

        }

        else if(menuButtons.length){

            menuButtons[0].click();

        }

    }
);


/* ===================================
MOBILE SIDEBAR
=================================== */

if(
    mobileSidebarBtn &&
    adminSidebar
){

    mobileSidebarBtn.addEventListener(
        "click",
        () => {

            adminSidebar.classList.toggle(
                "show-sidebar"
            );

        }
    );

}


/* ===================================
OUTSIDE CLICK CLOSE
=================================== */

document.addEventListener(
    "click",
    (event) => {

        if(
            window.innerWidth <= 992 &&
            adminSidebar &&
            mobileSidebarBtn
        ){

            const insideSidebar =
                adminSidebar.contains(
                    event.target
                );

            const menuClicked =
                mobileSidebarBtn.contains(
                    event.target
                );

            if(
                !insideSidebar &&
                !menuClicked
            ){

                adminSidebar.classList.remove(
                    "show-sidebar"
                );

            }

        }

    }
);


/* ===================================
FORM SUBMIT LOADER
=================================== */

document.querySelectorAll("form")
.forEach((form) => {

    form.addEventListener(
        "submit",
        () => {

            const button =
                form.querySelector(
                    "button[type='submit']"
                );

            if(button){

                button.disabled = true;

                button.innerText =
                    "Processing...";

                button.style.opacity =
                    "0.7";

            }

        }
    );

});


/* ===================================
CARD HOVER EFFECT
=================================== */

document.querySelectorAll(
    `
    .stat-card,
    .slot-admin-card,
    .frequency-card-admin,
    .tier-card-admin,
    .admin-box
    `
)
.forEach((card) => {

    card.addEventListener(
        "mouseenter",
        () => {

            card.style.transform =
                "translateY(-5px)";

        }
    );

    card.addEventListener(
        "mouseleave",
        () => {

            card.style.transform =
                "translateY(0px)";

        }
    );

});


/* ===================================
PROGRESS BAR ANIMATION
=================================== */

document.querySelectorAll(
    `
    .seat-progress-fill-admin,
    .booking-progress-fill
    `
)
.forEach((bar) => {

    const width =
        bar.style.width;

    bar.style.width = "0%";

    setTimeout(() => {

        bar.style.transition =
            "1s ease";

        bar.style.width = width;

    }, 300);

});


/* ===================================
STATUS COLOR SYSTEM
=================================== */

document.querySelectorAll(
    `
    .booking-status-badge,
    .slot-open-badge,
    .tier-status-badge
    `
)
.forEach((badge) => {

    const text =
        badge.innerText
        .toLowerCase();

    if(
        text.includes("completed") ||
        text.includes("active") ||
        text.includes("open")
    ){

        badge.style.background =
            "rgba(0,255,128,0.12)";

        badge.style.color =
            "#7dffb0";

    }

    else if(
        text.includes("pending")
    ){

        badge.style.background =
            "rgba(255,180,0,0.12)";

        badge.style.color =
            "#ffcb45";

    }

    else if(
        text.includes("disabled") ||
        text.includes("closed") ||
        text.includes("full")
    ){

        badge.style.background =
            "rgba(255,0,0,0.12)";

        badge.style.color =
            "#ff8d8d";

    }

});


/* ===================================
LIVE CLOCK
=================================== */

const realtimeClock =
    document.getElementById(
        "realtimeClock"
    );

function updateClock(){

    if(realtimeClock){

        realtimeClock.innerText =
            new Date()
            .toLocaleTimeString(
                "en-IN",
                {
                    hour:"2-digit",
                    minute:"2-digit",
                    second:"2-digit"
                }
            );

    }

}

setInterval(
    updateClock,
    1000
);

updateClock();


/* ===================================
SEARCH FILTER
=================================== */

const searchInput =
    document.getElementById(
        "adminSearchInput"
    );

if(searchInput){

    searchInput.addEventListener(
        "keyup",
        () => {

            const value =
                searchInput.value
                .toLowerCase();

            document.querySelectorAll(
                `
                .slot-admin-card,
                .user-card,
                .booking-card,
                .frequency-card-admin,
                .tier-card-admin
                `
            )
            .forEach((card) => {

                const text =
                    card.innerText
                    .toLowerCase();

                card.style.display =

                    text.includes(value)

                    ? "block"

                    : "none";

            });

        }
    );

}


/* ===================================
DELETE CONFIRMATION
=================================== */

document.querySelectorAll(
    `
    .delete-btn,
    .delete-slot-btn
    `
)
.forEach((button) => {

    button.addEventListener(
        "click",
        (e) => {

            const confirmed =
                confirm(
                    "Delete this item permanently?"
                );

            if(!confirmed){

                e.preventDefault();

            }

        }
    );

});


/* ===================================
LIVE ACTIVITY FEED
=================================== */

const activityFeed =
    document.querySelector(
        ".live-activity-feed"
    );

const liveMessages = [

    "New Premium booking received",

    "6AM slot almost full",

    "Payment verified",

    "Worker assigned",

    "Complaint resolved",

    "New customer onboarded",

    "Morning slot opened",

    "Frequency updated by admin",

    "New weekly plan created",

    "Evening slot disabled"

];

function addLiveActivity(message){

    if(!activityFeed){

        return;

    }

    const item =
        document.createElement("div");

    item.className =
        "live-update-item";

    item.innerHTML = `

        <div class="live-update-top">

            <strong>
                ${message}
            </strong>

            <span>
                Just Now
            </span>

        </div>

    `;

    activityFeed.prepend(item);

}


setInterval(() => {

    const randomMessage =

        liveMessages[
            Math.floor(
                Math.random() *
                liveMessages.length
            )
        ];

    addLiveActivity(
        randomMessage
    );

}, 20000);


/* ===================================
SLOT WARNING SYSTEM
=================================== */

document.querySelectorAll(
    ".seat-top-admin strong"
)
.forEach((seat) => {

    const parts =
        seat.innerText.split("/");

    if(parts.length !== 2){

        return;

    }

    const current =
        parseInt(parts[0]);

    const max =
        parseInt(parts[1]);

    const percentage =
        (current / max) * 100;

    const card =
        seat.closest(
            ".slot-admin-card"
        );

    if(!card){

        return;

    }

    if(percentage >= 90){

        card.style.borderColor =
            "#ff6b6b";

        card.style.boxShadow =
            "0px 0px 18px rgba(255,0,0,0.18)";

    }

    else if(percentage >= 70){

        card.style.borderColor =
            "#ffcb45";

    }

});


/* ===================================
FREQUENCY SELECTION SYSTEM
=================================== */

const frequencyCards =
    document.querySelectorAll(
        ".frequency-card-admin"
    );

frequencyCards.forEach((card) => {

    card.addEventListener(
        "click",
        () => {

            frequencyCards.forEach((c) => {

                c.classList.remove(
                    "active-frequency-admin"
                );

            });

            card.classList.add(
                "active-frequency-admin"
            );

            const frequencyId =
                card.dataset.frequency;

            if(!frequencyId){

                return;

            }

            document.querySelectorAll(
                ".tier-card-admin"
            )
            .forEach((tier) => {

                if(
                    tier.dataset.frequency ===
                    frequencyId
                ){

                    tier.style.display =
                        "block";

                }

                else{

                    tier.style.display =
                        "none";

                }

            });

        }
    );

});


/* ===================================
PLAN SELECTION SYSTEM
=================================== */

const tierCards =
    document.querySelectorAll(
        ".tier-card-admin"
    );

tierCards.forEach((card) => {

    card.addEventListener(
        "click",
        () => {

            tierCards.forEach((tier) => {

                tier.classList.remove(
                    "selected-tier-card"
                );

            });

            card.classList.add(
                "selected-tier-card"
            );

            const planId =
                card.dataset.plan;

            if(!planId){

                return;

            }

            document.querySelectorAll(
                ".slot-admin-card"
            )
            .forEach((slot) => {

                if(
                    slot.dataset.plan ===
                    planId
                ){

                    slot.style.display =
                        "block";

                }

                else{

                    slot.style.display =
                        "none";

                }

            });

        }
    );

});


/* ===================================
AUTO SCROLL TO NEXT SECTION
=================================== */

frequencyCards.forEach((card) => {

    card.addEventListener(
        "click",
        () => {

            const tierSection =
                document.querySelector(
                    ".tier-grid-admin"
                );

            if(tierSection){

                tierSection.scrollIntoView({

                    behavior:"smooth",
                    block:"start"

                });

            }

        }
    );

});


tierCards.forEach((card) => {

    card.addEventListener(
        "click",
        () => {

            const slotSection =
                document.querySelector(
                    ".slot-grid-admin"
                );

            if(slotSection){

                slotSection.scrollIntoView({

                    behavior:"smooth",
                    block:"start"

                });

            }

        }
    );

});


/* ===================================
LIVE DASHBOARD STATS ANIMATION
=================================== */

document.querySelectorAll(
    ".stat-card h2"
)
.forEach((counter) => {

    const text =
        counter.innerText
        .replace(/[^\d]/g,'');

    const target =
        parseInt(text);

    if(isNaN(target)){

        return;

    }

    let count = 0;

    const increment =
        Math.ceil(target / 40);

    const updateCounter = () => {

        count += increment;

        if(count >= target){

            counter.innerText =
                counter.innerText
                .includes("₹")

                ? `₹${target}`

                : target;

            return;

        }

        counter.innerText =
            counter.innerText
            .includes("₹")

            ? `₹${count}`

            : count;

        requestAnimationFrame(
            updateCounter
        );

    };

    updateCounter();

});


console.log(
    "Enterprise Operations UI Ready"
);