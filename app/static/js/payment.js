console.log(
    "CLEANZO Payment System Loaded"
);





/* ===================================
ELEMENTS
=================================== */

const paymentForm =
    document.querySelector("form");


const payButton =
    document.querySelector(".pay-btn");


const transactionInput =
    document.querySelector(
        ".transaction-input"
    );


const paymentCard =
    document.querySelector(
        ".payment-main-card"
    );





/* ===================================
BUTTON LOADING UI
=================================== */

function startPaymentLoading() {

    if (!payButton) return;

    payButton.innerHTML =
        "Processing Payment...";

    payButton.disabled = true;

    payButton.style.opacity = "0.8";

    payButton.style.cursor = "not-allowed";

}





/* ===================================
INPUT VALIDATION
=================================== */

function validateTransactionInput() {

    if (!transactionInput) {

        return false;

    }

    const value =
        transactionInput.value.trim();

    if (value === "") {

        transactionInput.style.border =
            "1px solid #ff5f7a";

        transactionInput.focus();

        alert(
            "Please enter Transaction / UTR ID"
        );

        return false;
    }

    transactionInput.style.border =
        "1px solid rgba(255,255,255,0.08)";

    return true;
}





/* ===================================
FORM SUBMIT
=================================== */

if (paymentForm) {

    paymentForm.addEventListener(

        "submit",

        (event) => {

            const isValid =
                validateTransactionInput();

            if (!isValid) {

                event.preventDefault();

                return;
            }

            startPaymentLoading();

        }

    );

}





/* ===================================
LIVE INPUT EFFECT
=================================== */

if (transactionInput) {

    transactionInput.addEventListener(

        "focus",

        () => {

            transactionInput.style.border =
                "1px solid rgba(57,207,255,0.5)";

            transactionInput.style.boxShadow =
                "0px 0px 20px rgba(57,207,255,0.12)";

        }

    );


    transactionInput.addEventListener(

        "blur",

        () => {

            transactionInput.style.boxShadow =
                "none";

            transactionInput.style.border =
                "1px solid rgba(255,255,255,0.08)";

        }

    );

}





/* ===================================
CARD FLOAT EFFECT
=================================== */

if (paymentCard) {

    paymentCard.addEventListener(

        "mousemove",

        (event) => {

            const rect =
                paymentCard.getBoundingClientRect();

            const x =
                event.clientX - rect.left;

            const y =
                event.clientY - rect.top;

            const rotateY =
                ((x / rect.width) - 0.5) * 4;

            const rotateX =
                ((y / rect.height) - 0.5) * -4;

            paymentCard.style.transform =
                `
                rotateX(${rotateX}deg)
                rotateY(${rotateY}deg)
                `;

        }

    );


    paymentCard.addEventListener(

        "mouseleave",

        () => {

            paymentCard.style.transform =
                "rotateX(0deg) rotateY(0deg)";

        }

    );

}





/* ===================================
PAY BUTTON PRESS EFFECT
=================================== */

if (payButton) {

    payButton.addEventListener(

        "mousedown",

        () => {

            payButton.style.transform =
                "scale(0.98)";

        }

    );


    payButton.addEventListener(

        "mouseup",

        () => {

            payButton.style.transform =
                "scale(1)";

        }

    );

}





/* ===================================
PAGE READY
=================================== */

window.addEventListener(

    "load",

    () => {

        console.log(
            "Payment Page Ready"
        );

    }

);