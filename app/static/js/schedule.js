console.log(
    "CLEANZO Smart Schedule UI Loaded"
);


/* ===================================
GLOBAL SELECTORS
=================================== */

const frequencyCards =
    document.querySelectorAll(
        ".frequency-card"
    );

const tierCards =
    document.querySelectorAll(
        ".tier-card"
    );

const slotCards =
    document.querySelectorAll(
        ".slot-card"
    );

const summaryFrequency =
    document.getElementById(
        "summaryFrequency"
    );

const summaryPlan =
    document.getElementById(
        "summaryPlan"
    );

const summarySlot =
    document.getElementById(
        "summarySlot"
    );

const summaryPrice =
    document.getElementById(
        "summaryPrice"
    );

const confirmButton =
    document.getElementById(
        "confirmBookingBtn"
    );


/* ===================================
HELPERS
=================================== */

function resetTierSelection(){

    tierCards.forEach((tier) => {

        tier.classList.remove(
            "active-tier"
        );

        const tierInput =
            tier.querySelector(
                "input"
            );

        if(tierInput){

            tierInput.checked = false;

        }

    });

}


function resetSlotSelection(){

    slotCards.forEach((slot) => {

        slot.classList.remove(
            "active-slot"
        );

        const slotInput =
            slot.querySelector(
                "input"
            );

        if(slotInput){

            slotInput.checked = false;

        }

    });

}


function updateSummary(){

    const activeFrequency =
        document.querySelector(
            ".frequency-card.active-frequency"
        );

    const activeTier =
        document.querySelector(
            ".tier-card.active-tier"
        );

    const activeSlot =
        document.querySelector(
            ".slot-card.active-slot"
        );


    /* FREQUENCY */

    if(
        activeFrequency &&
        summaryFrequency
    ){

        summaryFrequency.innerText =

            activeFrequency.dataset.frequency ||

            "Not Selected";

    }


    /* PLAN */

    if(
        activeTier &&
        summaryPlan &&
        summaryPrice
    ){

        summaryPlan.innerText =

            activeTier.dataset.plan ||

            "Not Selected";

        summaryPrice.innerText =

            `₹${
                activeTier.dataset.price || 0
            }`;

    }


    /* SLOT */

    if(
        activeSlot &&
        summarySlot
    ){

        const slotTime =
            activeSlot.dataset.slot;

        const slotShift =
            activeSlot.dataset.shift;

        summarySlot.innerText =

            `${slotTime}
            (${slotShift})`;

    }

}


/* ===================================
FREQUENCY SELECT
=================================== */

frequencyCards.forEach((card) => {

    const input =
        card.querySelector(
            "input"
        );

    card.addEventListener(
        "click",
        () => {

            frequencyCards.forEach((item) => {

                item.classList.remove(
                    "active-frequency"
                );

            });

            card.classList.add(
                "active-frequency"
            );

            if(input){

                input.checked = true;

            }


            /* FILTER TIERS */

            const selectedFrequencyId =

                card.dataset.frequencyId;

            tierCards.forEach((tier) => {

                const tierFrequencyId =

                    tier.dataset.frequencyId;

                if(
                    tierFrequencyId ===
                    selectedFrequencyId
                ){

                    tier.style.display =
                        "block";

                }

                else{

                    tier.style.display =
                        "none";

                }

            });


            /* RESET */

            resetTierSelection();

            resetSlotSelection();


            if(summaryPlan){

                summaryPlan.innerText =
                    "Select Plan";

            }

            if(summaryPrice){

                summaryPrice.innerText =
                    "₹0";

            }

            if(summarySlot){

                summarySlot.innerText =
                    "Select Slot";

            }


            updateSummary();

        }
    );

});


/* ===================================
PLAN SELECT
=================================== */

tierCards.forEach((card) => {

    const input =
        card.querySelector(
            "input"
        );

    card.addEventListener(
        "click",
        () => {

            tierCards.forEach((item) => {

                item.classList.remove(
                    "active-tier"
                );

            });

            card.classList.add(
                "active-tier"
            );

            if(input){

                input.checked = true;

            }


            /* FILTER SLOT */

            const selectedPlanId =

                card.dataset.planId;

            slotCards.forEach((slot) => {

                const slotPlanId =

                    slot.dataset.planId;

                if(
                    slotPlanId ===
                    selectedPlanId
                ){

                    slot.style.display =
                        "block";

                }

                else{

                    slot.style.display =
                        "none";

                }

            });


            /* RESET SLOT */

            resetSlotSelection();

            if(summarySlot){

                summarySlot.innerText =
                    "Select Slot";

            }

            updateSummary();

        }
    );

});


/* ===================================
SLOT SELECT
=================================== */

slotCards.forEach((card) => {

    const input =
        card.querySelector(
            "input"
        );

    card.addEventListener(
        "click",
        () => {

            slotCards.forEach((item) => {

                item.classList.remove(
                    "active-slot"
                );

            });

            card.classList.add(
                "active-slot"
            );

            if(input){

                input.checked = true;

            }

            updateSummary();

        }
    );

});


/* ===================================
AUTO LOAD
=================================== */

window.addEventListener(
    "load",
    () => {

        if(
            frequencyCards.length
        ){

            frequencyCards[0].click();

        }

    }
);


/* ===================================
CONFIRM BUTTON
=================================== */

if(confirmButton){


confirmButton.addEventListener(
    "click",
    (e) => {

        const selectedFrequency =
            document.querySelector(
                ".frequency-card.active-frequency"
            );

        const selectedTier =
            document.querySelector(
                ".tier-card.active-tier"
            );

        const selectedSlot =
            document.querySelector(
                ".slot-card.active-slot"
            );

        if(
            !selectedFrequency
        ){

            e.preventDefault();

            alert(
                "Please Select Frequency"
            );

            return;

        }

        if(
            !selectedTier
        ){

            e.preventDefault();

            alert(
                "Please Select Service Tier"
            );

            return;

        }

        if(
            !selectedSlot
        ){

            e.preventDefault();

            alert(
                "Please Select Time Slot"
            );

            return;

        }

      //  confirmButton.innerText =
        //    "Processing...";

       // confirmButton.disabled =
           // true;

        /*
        IMPORTANT

        No e.preventDefault()
        No fetch()
        No AJAX

        Browser will submit form normally.
        Flask will redirect to payment page.
        */

    }
);


}

// Robust submit: use fetch to POST and follow server redirect reliably
const scheduleForm = document.querySelector('form.schedule-layout');
if(scheduleForm){
    scheduleForm.addEventListener('submit', (ev) => {
        ev.preventDefault();

        // gather and basic-validate selections
        const selectedFrequency = document.querySelector('.frequency-card.active-frequency');
        const selectedTier = document.querySelector('.tier-card.active-tier');
        const selectedSlot = document.querySelector('.slot-card.active-slot');

        if(!selectedFrequency || !selectedTier || !selectedSlot){
            alert('Please complete the selection before confirming.');
            return;
        }

        const fd = new FormData(scheduleForm);

        // Send form via fetch and navigate to final URL returned by server
        fetch(scheduleForm.action, {
            method: 'POST',
            body: fd,
            credentials: 'same-origin'
        }).then(response => {
            // If server redirected to payment, response.url will reflect final location
            if(response && response.url){
                window.location.href = response.url;
            } else {
                // fallback: reload to reflect any flashes
                window.location.reload();
            }
        }).catch(err => {
            console.error('Schedule submit failed', err);
            window.location.reload();
        });

    });
}



/* ===================================
SLOT WARNING
=================================== */

slotCards.forEach((card) => {

    const seats =
        parseInt(
            card.dataset.available || 0
        );

    if(seats <= 2){

        const span =
            card.querySelector(
                "span"
            );

        if(span){

            span.style.borderColor =
                "#ff8d8d";

            span.style.boxShadow =
                `
                0px 0px 18px
                rgba(
                    255,
                    120,
                    120,
                    0.18
                )
                `;

        }

    }

});


/* ===================================
SMOOTH ANIMATION
=================================== */

document.querySelectorAll(
    `
    .frequency-content,
    .tier-card,
    .slot-card span,
    .summary-card
    `
)
.forEach((card) => {

    card.addEventListener(
        "mouseenter",
        () => {

            card.style.transition =
                "0.35s ease";

        }
    );

});


/* ===================================
LIVE SYSTEM CHECK
=================================== */

function updateSummaryStatus(){

    const frequency =
        document.querySelector(
            ".frequency-card.active-frequency"
        );

    const tier =
        document.querySelector(
            ".tier-card.active-tier"
        );

    const slot =
        document.querySelector(
            ".slot-card.active-slot"
        );

    if(
        frequency &&
        tier &&
        slot
    ){

        console.log(
            "Schedule Ready For Booking"
        );

    }

}

setInterval(
    updateSummaryStatus,
    1000
);


console.log(
    "CLEANZO Schedule System Ready"
);