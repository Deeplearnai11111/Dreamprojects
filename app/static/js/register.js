console.log("CLEANZO Register Loaded");


/* ===================================
MULTI STEP FORM
=================================== */

const steps =
document.querySelectorAll(
    ".form-step"
);

const nextBtns =
document.querySelectorAll(
    ".next-btn"
);

const prevBtns =
document.querySelectorAll(
    ".prev-btn"
);

let currentStep = 0;



/* ===================================
SHOW STEP
=================================== */

function showStep(stepIndex){

    steps.forEach(

        (step) => {

            step.classList.remove(
                "active-step"
            );

        }

    );

    steps[stepIndex].classList.add(
        "active-step"
    );

}



/* ===================================
NEXT BUTTON
=================================== */

nextBtns.forEach(

    (button) => {

        button.addEventListener(

            "click",

            () => {

                /*
                STEP VALIDATION
                */

                const currentInputs =
                steps[currentStep]
                .querySelectorAll(
                    "input[required], select[required]"
                );

                let valid = true;

                currentInputs.forEach(

                    (input) => {

                        if(
                            !input.value.trim()
                        ){

                            valid = false;

                            input.style.borderColor =
                            "#ff4d6d";


                            input.addEventListener(

                                "input",

                                () => {

                                    input.style.borderColor =
                                    "rgba(255,255,255,0.08)";

                                }

                            );

                        }

                    }

                );

                if(!valid){

                    return;

                }


                /*
                NEXT STEP
                */

                if(
                    currentStep <
                    steps.length - 1
                ){

                    currentStep++;

                    showStep(
                        currentStep
                    );

                    window.scrollTo({

                        top:0,

                        behavior:"smooth"

                    });

                }

            }

        );

    }

);



/* ===================================
PREVIOUS BUTTON
=================================== */

prevBtns.forEach(

    (button) => {

        button.addEventListener(

            "click",

            () => {

                if(currentStep > 0){

                    currentStep--;

                    showStep(
                        currentStep
                    );

                    window.scrollTo({

                        top:0,

                        behavior:"smooth"

                    });

                }

            }

        );

    }

);



/* ===================================
FORM SUBMIT
=================================== */

const form =
document.querySelector(
    "#multiStepForm"
);


if(form){

    form.addEventListener(

        "submit",

        (e) => {

            console.log(
                "Registration Started"
            );


            /*
            BUTTON LOADING
            */

            const submitBtn =
            document.querySelector(
                ".continue-btn[type='submit']"
            );

            if(submitBtn){

                submitBtn.innerHTML =
                "Creating Account...";

                submitBtn.style.opacity =
                "0.8";

                submitBtn.disabled =
                true;

            }

        }

    );

}



/* ===================================
GLASS CARD HOVER EFFECT
=================================== */

const glassCards =
document.querySelectorAll(
    ".glass-card"
);


glassCards.forEach(

    (card) => {

        card.addEventListener(

            "mousemove",

            (e) => {

                const rect =
                card.getBoundingClientRect();

                const x =
                e.clientX - rect.left;

                const y =
                e.clientY - rect.top;

                card.style.background = `

                radial-gradient(
                    circle at ${x}px ${y}px,
                    rgba(57,207,255,0.18),
                    rgba(255,255,255,0.03)
                )

                `;

            }

        );


        card.addEventListener(

            "mouseleave",

            () => {

                card.style.background = `

                linear-gradient(
                    135deg,
                    rgba(57,207,255,0.12),
                    rgba(255,255,255,0.03)
                )

                `;

            }

        );

    }

);



/* ===================================
INPUT FOCUS EFFECT
=================================== */

const inputs =
document.querySelectorAll(

    "input, select"

);


inputs.forEach(

    (input) => {

        input.addEventListener(

            "focus",

            () => {

                const parent =
                input.closest(
                    ".input-group"
                );

                if(parent){

                    parent.style.transform =
                    "translateY(-3px)";

                }

            }

        );


        input.addEventListener(

            "blur",

            () => {

                const parent =
                input.closest(
                    ".input-group"
                );

                if(parent){

                    parent.style.transform =
                    "translateY(0px)";

                }

            }

        );

    }

);



/* ===================================
BUTTON HOVER EFFECT
=================================== */

const buttons =
document.querySelectorAll(

    ".continue-btn, .back-btn"

);


buttons.forEach(

    (button) => {

        button.addEventListener(

            "mouseenter",

            () => {

                button.style.transform =
                "translateY(-4px)";

            }

        );


        button.addEventListener(

            "mouseleave",

            () => {

                button.style.transform =
                "translateY(0px)";

            }

        );

    }

);



/* ===================================
SELECT LOG
=================================== */

const selects =
document.querySelectorAll(
    "select"
);


selects.forEach(

    (select) => {

        select.addEventListener(

            "change",

            () => {

                console.log(

                    "Selected:",

                    select.value

                );

            }

        );

    }

);



/* ===================================
STEP ANIMATION
=================================== */

window.addEventListener(

    "load",

    () => {

        setTimeout(

            () => {

                document.body.classList.add(
                    "loaded"
                );

            },

            300

        );

    }

);



/* ===================================
MOBILE DETECTION
=================================== */

if(window.innerWidth < 768){

    console.log(
        "Mobile Register View"
    );

}else{

    console.log(
        "Desktop Register View"
    );

}