console.log(
    "CLEANZO Smart Schedule UI Loaded"
);


/* ===================================
SELECTORS
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


/* ===================================
EMPTY SLOT MESSAGE
=================================== */

function updateEmptySlotMessage(){

    let visibleCount = 0;

    slotCards.forEach((slot) => {

        if(
            slot.style.display !==
            "none"
        ){

            visibleCount++;

        }

    });

    let emptyBox =
        document.getElementById(
            "emptySlotMessage"
        );

    if(!emptyBox){

        emptyBox =
            document.createElement(
                "div"
            );

        emptyBox.id =
            "emptySlotMessage";

        emptyBox.className =
            "no-slot-box";

        emptyBox.innerText =
            "No Slots Available";

        const section =
            document.querySelector(
                ".schedule-section:last-child"
            );

        if(section){

            section.appendChild(
                emptyBox
            );

        }

    }

    if(visibleCount === 0){

        emptyBox.style.display =
            "flex";

    }

    else{

        emptyBox.style.display =
            "none";

    }

}


/* ===================================
RESET SLOT STATE
=================================== */

function resetSlots(){

    slotCards.forEach((slot) => {

        slot.style.display =
            "none";

        slot.classList.remove(
            "active-slot"
        );

        const input =
            slot.querySelector(
                "input"
            );

        if(input){

            input.checked =
                false;

        }

    });

    if(summarySlot){

        summarySlot.innerText =
            "Select Slot";

    }

    updateEmptySlotMessage();

}


/* ===================================
FREQUENCY SELECT
=================================== */

frequencyCards.forEach((card) => {

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

            const input =
                card.querySelector(
                    "input"
                );

            if(input){

                input.checked = true;

            }

            const frequencyName =
                card.dataset.frequency;

            const frequencyId =
                card.dataset.frequencyId;

            if(summaryFrequency){

                summaryFrequency.innerText =
                    frequencyName;

            }


            /* ===================================
            FILTER PLANS
            =================================== */

            let firstVisiblePlan =
                null;

            tierCards.forEach((tier) => {

                const tierFrequencyId =
                    tier.dataset.frequencyId;

                if(
                    tierFrequencyId ===
                    frequencyId
                ){

                    tier.style.display =
                        "block";

                    if(
                        !firstVisiblePlan
                    ){

                        firstVisiblePlan =
                            tier;

                    }

                }

                else{

                    tier.style.display =
                        "none";

                    tier.classList.remove(
                        "active-tier"
                    );

                    const tierInput =
                        tier.querySelector(
                            "input"
                        );

                    if(tierInput){

                        tierInput.checked =
                            false;

                    }

                }

            });


            /* ===================================
            RESET SLOT
            =================================== */

            resetSlots();


            /* ===================================
            AUTO SELECT FIRST PLAN
            =================================== */

            if(firstVisiblePlan){

                firstVisiblePlan.click();

            }

            else{

                if(summaryPlan){

                    summaryPlan.innerText =
                        "Select Plan";

                }

                if(summaryPrice){

                    summaryPrice.innerText =
                        "₹0";

                }

            }

        }
    );

});


/* ===================================
PLAN SELECT
=================================== */

tierCards.forEach((card) => {

    card.addEventListener(
        "click",
        () => {

            if(
                card.style.display ===
                "none"
            ){

                return;

            }

            tierCards.forEach((item) => {

                item.classList.remove(
                    "active-tier"
                );

            });

            card.classList.add(
                "active-tier"
            );

            const input =
                card.querySelector(
                    "input"
                );

            if(input){

                input.checked = true;

            }

            const planName =
                card.dataset.plan;

            const planPrice =
                card.dataset.price;

            const planId =
                card.dataset.planId;

            const frequencyCard =
                document.querySelector(
                    ".frequency-card.active-frequency"
                );

            const activeFrequencyId =
                frequencyCard
                ?
                frequencyCard.dataset.frequencyId
                :
                null;

            if(summaryPlan){

                summaryPlan.innerText =
                    planName;

            }

            if(summaryPrice){

                summaryPrice.innerText =
                    `₹${planPrice}`;

            }


            /* ===================================
            FILTER SLOTS
            =================================== */

            let visibleSlots = 0;

            slotCards.forEach((slot) => {

                const slotPlanId =
                    slot.dataset.planId;

                const slotFrequencyId =
                    slot.dataset.frequencyId;

                if(

                    slotPlanId ===
                    planId &&

                    slotFrequencyId ===
                    activeFrequencyId

                ){

                    slot.style.display =
                        "flex";

                    visibleSlots++;

                }

                else{

                    slot.style.display =
                        "none";

                    slot.classList.remove(
                        "active-slot"
                    );

                    const slotInput =
                        slot.querySelector(
                            "input"
                        );

                    if(slotInput){

                        slotInput.checked =
                            false;

                    }

                }

            });

            if(summarySlot){

                summarySlot.innerText =
                    "Select Slot";

            }

            updateEmptySlotMessage();

        }
    );

});


/* ===================================
SLOT SELECT
=================================== */

slotCards.forEach((card) => {

    card.addEventListener(
        "click",
        () => {

            if(
                card.style.display ===
                "none"
            ){

                return;

            }

            slotCards.forEach((item) => {

                item.classList.remove(
                    "active-slot"
                );

            });

            card.classList.add(
                "active-slot"
            );

            const input =
                card.querySelector(
                    "input"
                );

            if(input){

                input.checked = true;

            }

            const slot =
                card.dataset.slot;

            const shift =
                card.dataset.shift;

            if(summarySlot){

                summarySlot.innerText =
                    `${slot} (${shift})`;

            }

        }
    );

});


/* ===================================
AUTO START
=================================== */

window.addEventListener(
    "load",
    () => {

        if(
            frequencyCards.length
        ){

            frequencyCards[0].click();

        }

        updateEmptySlotMessage();

    }
);


console.log(
    "CLEANZO Schedule System Ready"
);