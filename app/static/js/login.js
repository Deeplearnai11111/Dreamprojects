console.log("Login Page Loaded");


const form = document.querySelector("form");

form.addEventListener("submit", () => {

    console.log("Login Attempt Started");

});


const featureBoxes = document.querySelectorAll(".feature-box");

featureBoxes.forEach((box) => {

    box.addEventListener("mouseenter", () => {

        console.log("Feature Hovered");

    });

});