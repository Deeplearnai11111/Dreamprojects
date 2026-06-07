console.log("CLEANZO Plans Loaded");


function togglePlanDetails(button) {

    const currentCard =
        button.closest(".plan-card");

    const details =
        currentCard.querySelector(
            ".plan-details"
        );

    const allDetails =
        document.querySelectorAll(
            ".plan-details"
        );

    const allButtons =
        document.querySelectorAll(
            ".select-btn"
        );

    // CLOSE ALL OTHER CARDS

    allDetails.forEach((item) => {

        if (item !== details) {

            item.style.display = "none";

        }

    });

    allButtons.forEach((btn) => {

        if (btn !== button) {

            btn.innerText =
                "Select Plan →";

        }

    });

    // TOGGLE CURRENT CARD

    if (
        details.style.display === "block"
    ) {

        details.style.display = "none";

        button.innerText =
            "Select Plan →";

    } else {

        details.style.display = "block";

        button.innerText =
            "Hide Details ↑";

    }

}