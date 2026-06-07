console.log(
    "CLEANZO Tracking System Loaded"
);


/* ===================================
TIMELINE ITEMS
=================================== */

const timelineItems =
    document.querySelectorAll(
        ".timeline-item"
    );


/* ===================================
ACTIVE STEPS
=================================== */

const activeSteps =
    document.querySelectorAll(
        ".active-step"
    );


/* ===================================
CURRENT STATUS
=================================== */

const currentStatus =
    document.querySelector(
        ".live-status"
    );


/* ===================================
PROGRESS BAR
=================================== */

const progressFill =
    document.querySelector(
        ".tracking-progress-fill"
    );


/* ===================================
ADMIN MESSAGE
=================================== */

const adminMessage =
    document.querySelector(
        ".admin-live-message"
    );


/* ===================================
GARAGE NOTE
=================================== */

const garageNote =
    document.querySelector(
        ".garage-note-box"
    );


/* ===================================
COMPLETION CARD
=================================== */

const completionCard =
    document.querySelector(
        ".completion-card"
    );


/* ===================================
STATUS BADGE
=================================== */

const statusBadge =
    document.querySelector(
        ".live-status-badge"
    );


/* ===================================
PAYMENT STATUS
=================================== */

const paymentBadge =
    document.querySelector(
        ".payment-status-badge"
    );


/* ===================================
SCROLL TOP ON LOAD
=================================== */

window.scrollTo({

    top:0,

    behavior:"smooth"

});


/* ===================================
PAGE LOAD
=================================== */

window.addEventListener(
    "load",
    () => {

        console.log(
            "Tracking Timeline Ready"
        );


        /* ==========================
        TIMELINE ANIMATION
        ========================== */

        timelineItems.forEach(
            (item, index) => {

                item.style.opacity = "0";

                item.style.transform =
                    "translateY(25px)";

                setTimeout(() => {

                    item.style.transition =
                        "0.45s ease";

                    item.style.opacity = "1";

                    item.style.transform =
                        "translateY(0px)";

                }, index * 180);

            }
        );


        /* ==========================
        CURRENT STATUS
        ========================== */

        if(currentStatus){

            console.log(

                "Current Status : " +

                currentStatus.innerText

            );

        }


        /* ==========================
        ACTIVE STEP EFFECT
        ========================== */

        activeSteps.forEach((step) => {

            step.style.boxShadow =
                "0px 0px 24px rgba(57,207,255,0.08)";

            step.style.borderRadius =
                "22px";

        });


        /* ==========================
        PROGRESS BAR
        ========================== */

        if(progressFill){

            const finalWidth =
                progressFill.style.width;

            progressFill.style.width =
                "0%";

            setTimeout(() => {

                progressFill.style.transition =
                    "1.2s ease";

                progressFill.style.width =
                    finalWidth;

            }, 400);

        }


        /* ==========================
        ADMIN UPDATE ANIMATION
        ========================== */

        if(adminMessage){

            adminMessage.style.opacity =
                "0";

            adminMessage.style.transform =
                "translateY(15px)";

            setTimeout(() => {

                adminMessage.style.transition =
                    "0.6s ease";

                adminMessage.style.opacity =
                    "1";

                adminMessage.style.transform =
                    "translateY(0px)";

            }, 700);

        }


        /* ==========================
        GARAGE NOTE ANIMATION
        ========================== */

        if(garageNote){

            garageNote.style.opacity =
                "0";

            garageNote.style.transform =
                "translateY(15px)";

            setTimeout(() => {

                garageNote.style.transition =
                    "0.6s ease";

                garageNote.style.opacity =
                    "1";

                garageNote.style.transform =
                    "translateY(0px)";

            }, 900);

        }


        /* ==========================
        COMPLETION CARD
        ========================== */

        if(completionCard){

            completionCard.style.opacity =
                "0";

            completionCard.style.transform =
                "scale(0.95)";

            setTimeout(() => {

                completionCard.style.transition =
                    "0.7s ease";

                completionCard.style.opacity =
                    "1";

                completionCard.style.transform =
                    "scale(1)";

            }, 700);

        }


        /* ==========================
        STATUS BADGE EFFECT
        ========================== */

        if(statusBadge){

            statusBadge.style.opacity =
                "0";

            setTimeout(() => {

                statusBadge.style.transition =
                    "0.5s ease";

                statusBadge.style.opacity =
                    "1";

            }, 300);

        }


        /* ==========================
        PAYMENT BADGE EFFECT
        ========================== */

        if(paymentBadge){

            paymentBadge.style.transform =
                "scale(0.95)";

            setTimeout(() => {

                paymentBadge.style.transition =
                    "0.4s ease";

                paymentBadge.style.transform =
                    "scale(1)";

            }, 500);

        }

    }
);


/* ===================================
LIVE STATUS PULSE
=================================== */

if(currentStatus){

    setInterval(() => {

        currentStatus.style.transition =
            "0.4s ease";

        currentStatus.style.transform =
            "scale(1.03)";

        setTimeout(() => {

            currentStatus.style.transform =
                "scale(1)";

        }, 450);

    }, 2500);

}


/* ===================================
COMPLETION DETECTION
=================================== */

if(currentStatus){

    const statusText =
        currentStatus.innerText
        .trim()
        .toLowerCase();

    if(
        statusText.includes(
            "completed"
        )
    ){

        console.log(
            "Service Completed Successfully"
        );

        document.title =
            "✅ CLEANZO Service Completed";

    }

    else{

        document.title =
            "🚗 CLEANZO Live Tracking";

    }

}


/* ===================================
GARAGE MODE DETECTION
=================================== */

if(garageNote){

    console.log(
        "Garage Service Tracking Enabled"
    );

}


/* ===================================
LIVE REFRESH CHECK
=================================== */

setInterval(() => {

    console.log(
        "Checking latest service status..."
    );

}, 30000);


/* ===================================
LIVE STATUS COLOR CONTROL
=================================== */

if(statusBadge){

    const badgeText =
        statusBadge.innerText
        .trim()
        .toLowerCase();

    if(
        badgeText.includes(
            "completed"
        )
    ){

        statusBadge.style.boxShadow =
            "0px 0px 20px rgba(0,255,128,0.2)";

    }

    else if(
        badgeText.includes(
            "progress"
        )
    ){

        statusBadge.style.boxShadow =
            "0px 0px 20px rgba(57,207,255,0.2)";

    }

    else{

        statusBadge.style.boxShadow =
            "0px 0px 20px rgba(255,179,71,0.15)";

    }

}


/* ===================================
AUTO UPDATE NOTIFICATION
=================================== */

function showUpdateNotification(message){

    const notification =
        document.createElement("div");

    notification.innerText =
        message;

    notification.style.position =
        "fixed";

    notification.style.top =
        "25px";

    notification.style.right =
        "25px";

    notification.style.padding =
        "16px 22px";

    notification.style.background =
        "rgba(57,207,255,0.12)";

    notification.style.border =
        "1px solid rgba(57,207,255,0.2)";

    notification.style.color =
        "#ffffff";

    notification.style.borderRadius =
        "18px";

    notification.style.backdropFilter =
        "blur(12px)";

    notification.style.zIndex =
        "9999";

    notification.style.opacity =
        "0";

    notification.style.transform =
        "translateY(-20px)";

    document.body.appendChild(
        notification
    );

    setTimeout(() => {

        notification.style.transition =
            "0.5s ease";

        notification.style.opacity =
            "1";

        notification.style.transform =
            "translateY(0px)";

    }, 100);

    setTimeout(() => {

        notification.style.opacity =
            "0";

        notification.style.transform =
            "translateY(-20px)";

        setTimeout(() => {

            notification.remove();

        }, 500);

    }, 3500);

}


/* ===================================
ADMIN UPDATE ALERT
=================================== */

if(adminMessage){

    setTimeout(() => {

        showUpdateNotification(
            "New Admin Update Available"
        );

    }, 1200);

}


/* ===================================
TRACKING READY
=================================== */

console.log(
    "CLEANZO Smart Tracking Active"
);