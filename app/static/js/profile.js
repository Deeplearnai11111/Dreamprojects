console.log(
    "CLEANZO Dashboard Loaded"
);


/* ===================================
TAB SWITCHING
=================================== */

const tabButtons =
    document.querySelectorAll(
        ".sidebar-btn"
    );

const tabContents =
    document.querySelectorAll(
        ".tab-content"
    );


tabButtons.forEach((button) => {

    button.addEventListener(
        "click",
        () => {

            /* REMOVE ACTIVE */

            tabButtons.forEach((btn) => {

                btn.classList.remove(
                    "active-tab"
                );

            });

            tabContents.forEach((content) => {

                content.classList.remove(
                    "active-content"
                );

            });


            /* ADD ACTIVE */

            button.classList.add(
                "active-tab"
            );

            const target =
                button.dataset.tab;

            const activeContent =
                document.getElementById(
                    target
                );

            if(activeContent){

                activeContent.classList.add(
                    "active-content"
                );

            }


            /* SAVE ACTIVE TAB */

            localStorage.setItem(
                "profileActiveTab",
                target
            );


            /* SCROLL TOP */

            window.scrollTo({

                top:0,

                behavior:"smooth"

            });

        }
    );

});


/* ===================================
RESTORE LAST TAB
=================================== */

window.addEventListener(
    "load",
    () => {

        const savedTab =
            localStorage.getItem(
                "profileActiveTab"
            );

        if(savedTab){

            const targetButton =
                document.querySelector(
                    `[data-tab="${savedTab}"]`
                );

            if(targetButton){

                targetButton.click();

            }

        }

        else{

            const firstTab =
                document.querySelector(
                    ".sidebar-btn"
                );

            if(firstTab){

                firstTab.click();

            }

        }


        /* PAGE FADE */

        document.body.style.opacity = "0";

        setTimeout(() => {

            document.body.style.opacity = "1";

            document.body.style.transition =
                "0.5s ease";

        }, 100);

    }
);


/* ===================================
CARD HOVER EFFECT
=================================== */

const cards =
    document.querySelectorAll(
        `
        .stat-card,
        .content-card,
        .car-card,
        .service-history-card,
        .tracking-preview-box,
        .live-status-box,
        .notification-card
        `
    );

cards.forEach((card) => {

    card.addEventListener(
        "mouseenter",
        () => {

            card.style.transform =
                "translateY(-5px)";

            card.style.transition =
                "0.3s ease";

            card.style.boxShadow =
                "0px 10px 30px rgba(0,0,0,0.18)";

        }
    );

    card.addEventListener(
        "mouseleave",
        () => {

            card.style.transform =
                "translateY(0px)";

            card.style.boxShadow =
                "none";

        }
    );

});


/* ===================================
STATS FADE ANIMATION
=================================== */

const statNumbers =
    document.querySelectorAll(
        ".stat-card h2"
    );

statNumbers.forEach((stat,index) => {

    stat.style.opacity = "0";

    stat.style.transform =
        "translateY(15px)";

    setTimeout(() => {

        stat.style.opacity = "1";

        stat.style.transform =
            "translateY(0px)";

        stat.style.transition =
            "0.5s ease";

    }, index * 150);

});


/* ===================================
TRACKING PROGRESS ANIMATION
=================================== */

const trackingBars =
    document.querySelectorAll(
        ".tracking-progress-fill"
    );

trackingBars.forEach((bar) => {

    const finalWidth =
        bar.style.width;

    bar.style.width = "0%";

    setTimeout(() => {

        bar.style.width =
            finalWidth;

        bar.style.transition =
            "1s ease";

    }, 400);

});


/* ===================================
LIVE STATUS GLOW
=================================== */

const liveStatus =
    document.querySelector(
        ".live-status-box"
    );

if(liveStatus){

    setInterval(() => {

        liveStatus.style.boxShadow =
            "0px 0px 24px rgba(57,207,255,0.12)";

        setTimeout(() => {

            liveStatus.style.boxShadow =
                "none";

        }, 900);

    }, 2200);

}


/* ===================================
TRACKING PULSE
=================================== */

const trackingPulse =
    document.querySelector(
        ".tracking-pulse"
    );

if(trackingPulse){

    setInterval(() => {

        trackingPulse.style.transform =
            "scale(1.2)";

        setTimeout(() => {

            trackingPulse.style.transform =
                "scale(1)";

        }, 600);

    }, 1500);

}


/* ===================================
SERVICE STATUS COLOR
=================================== */

const statusBadges =
    document.querySelectorAll(
        `
        .service-status-badge,
        .live-status
        `
    );

statusBadges.forEach((badge) => {

    const text =
        badge.innerText.toLowerCase();

    if(
        text.includes("completed")
    ){

        badge.style.background =
            "rgba(0,255,128,0.12)";

        badge.style.color =
            "#7dffb0";

    }

    else if(
        text.includes("progress")
    ){

        badge.style.background =
            "rgba(255,196,0,0.12)";

        badge.style.color =
            "#ffd86b";

    }

    else if(
        text.includes("pending")
    ){

        badge.style.background =
            "rgba(255,120,120,0.12)";

        badge.style.color =
            "#ff8d8d";

    }

    else if(
        text.includes("way")
    ){

        badge.style.background =
            "rgba(57,207,255,0.12)";

        badge.style.color =
            "#39cfff";

    }

});


/* ===================================
NOTIFICATION ANIMATION
=================================== */

const notifications =
    document.querySelectorAll(
        ".notification-card"
    );

notifications.forEach((card,index) => {

    card.style.opacity = "0";

    card.style.transform =
        "translateY(20px)";

    setTimeout(() => {

        card.style.opacity = "1";

        card.style.transform =
            "translateY(0px)";

        card.style.transition =
            "0.5s ease";

    }, index * 180);

});


/* ===================================
SERVICE STATUS AUTO REFRESH LOG
=================================== */

setInterval(() => {

    console.log(
        "Checking latest CLEANZO service status..."
    );

}, 30000);


/* ===================================
PROFILE IMAGE PREVIEW
=================================== */

const fileInput =
    document.querySelector(
        ".file-input"
    );

const profileImage =
    document.querySelector(
        ".profile-image"
    );

if(
    fileInput &&
    profileImage
){

    fileInput.addEventListener(
        "change",
        (event) => {

            const file =
                event.target.files[0];

            if(file){

                const imageURL =
                    URL.createObjectURL(
                        file
                    );

                profileImage.src =
                    imageURL;

            }

        }
    );

}


/* ===================================
BUTTON LOADING
=================================== */

const forms =
    document.querySelectorAll(
        "form"
    );

forms.forEach((form) => {

    form.addEventListener(
        "submit",
        () => {

            const submitButton =
                form.querySelector(
                    "button[type='submit']"
                );

            if(submitButton){

                submitButton.innerText =
                    "Processing...";

                submitButton.disabled =
                    true;

                submitButton.style.opacity =
                    "0.7";

                submitButton.style.cursor =
                    "not-allowed";

            }

        }
    );

});


/* ===================================
DELETE CONFIRMATION
=================================== */

const deleteButtons =
    document.querySelectorAll(
        ".delete-btn"
    );

deleteButtons.forEach((button) => {

    button.addEventListener(
        "click",
        (event) => {

            const confirmDelete =
                confirm(
                    "Are you sure you want to delete this?"
                );

            if(!confirmDelete){

                event.preventDefault();

            }

        }
    );

});


/* ===================================
ONLINE STATUS
=================================== */

window.addEventListener(
    "online",
    () => {

        console.log(
            "CLEANZO Connected"
        );

        const onlineIndicator =
            document.querySelector(
                ".online-indicator"
            );

        if(onlineIndicator){

            onlineIndicator.style.background =
                "#4dff88";

        }

    }
);

window.addEventListener(
    "offline",
    () => {

        console.log(
            "No Internet Connection"
        );

        const onlineIndicator =
            document.querySelector(
                ".online-indicator"
            );

        if(onlineIndicator){

            onlineIndicator.style.background =
                "#ff4d4d";

        }

    }
);


/* ===================================
SMOOTH SECTION OPEN
=================================== */

tabContents.forEach((section) => {

    section.style.opacity = "0";

});

document.addEventListener(
    "click",
    (event) => {

        if(
            event.target.classList.contains(
                "sidebar-btn"
            )
        ){

            setTimeout(() => {

                const activeSection =
                    document.querySelector(
                        ".active-content"
                    );

                if(activeSection){

                    activeSection.style.opacity =
                        "0";

                    setTimeout(() => {

                        activeSection.style.opacity =
                            "1";

                        activeSection.style.transition =
                            "0.4s ease";

                    }, 80);

                }

            }, 100);

        }

    }
);


/* ===================================
RIGHT-SIDE PANEL HANDLING
=================================== */

const panel = document.getElementById('right-panel');
const panelButtons = document.querySelectorAll('[data-popup-target]');

panelButtons.forEach((btn) => {

    btn.addEventListener('click', () => {

        const target = btn.dataset.popupTarget;

        // hide all panel sections
        const sections = panel.querySelectorAll('.panel-section');
        sections.forEach(s => s.classList.remove('active'));

        // show matching section
        const show = panel.querySelector(`[data-panel="${target}"]`);
        if(show) show.classList.add('active');

        // ensure panel is visible (aria)
        panel.setAttribute('aria-hidden','false');

        // mark layout as panel-active so panel expands into center
        const layout = document.querySelector('.profile-layout');
        if(layout) layout.classList.add('panel-active');

        // toggle active state on sidebar buttons
        panelButtons.forEach(b => b.classList.remove('active-tab'));
        btn.classList.add('active-tab');

        // scroll main to top for new content
        // if user opened the privacy panel, auto-load the full Privacy Policy
        if(target === 'privacy'){
            const autoLink = panel.querySelector('.popup-links a[href="/privacy"]');
            if(autoLink){
                setTimeout(() => autoLink.click(), 60);
            }
        }

        window.scrollTo({ top: 0, behavior: 'smooth' });

    });

});

// on load, show first panel section by default
window.addEventListener('load', () => {

    const firstSection = panel.querySelector('.panel-section');

    if(firstSection) firstSection.classList.add('active');

    const firstBtn = document.querySelector('[data-popup-target]');

    if(firstBtn) firstBtn.classList.add('active-tab');

});


console.log(
    "Profile UI Ready"
);

// Image modal handlers (WhatsApp-like)
const imageModal = document.getElementById('image-modal');
const modalView = document.getElementById('modal-view-photo');
const modalChange = document.getElementById('modal-change-photo');
const modalRemove = document.getElementById('modal-remove-photo');
const modalClose = document.getElementById('modal-close');
const modalImg = document.getElementById('image-modal-img');
const openImageModalBtn = document.getElementById('open-image-modal-btn');

function openImageModal(){
    if(imageModal) imageModal.classList.add('visible');
}
function closeImageModal(){
    if(imageModal) imageModal.classList.remove('visible');
}

if(profileImage){
    profileImage.style.cursor = 'pointer';
    profileImage.addEventListener('click', () => openImageModal());
}

if(openImageModalBtn){
    openImageModalBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openImageModal();
    });
}

if(modalClose){ modalClose.addEventListener('click', closeImageModal); }
if(imageModal){ imageModal.querySelector('.image-modal-backdrop').addEventListener('click', closeImageModal); }

if(modalView){
    modalView.addEventListener('click', () => {
        // open a larger view in a new tab
        const src = modalImg ? modalImg.src : (profileImage ? profileImage.src : null);
        if(src) window.open(src, '_blank');
        closeImageModal();
    });
}

if(modalChange){
    modalChange.addEventListener('click', () => {
        // trigger hidden file input in modal and submit form for upload
        const modalInput = document.getElementById('modal-profile-input');
        if(modalInput){
            modalInput.click();
        }
    });
}

if(modalRemove){
    modalRemove.addEventListener('click', () => {
        if(!confirm('Remove profile picture?')) return;
        fetch('/delete-profile-image')
            .then(() => window.location.reload())
            .catch(() => window.location.reload());
    });
}

// In-modal crop flow using Cropper.js
let cropper = null;
const modalProfileInput = document.getElementById('modal-profile-input');
const modalCropBtn = document.getElementById('modal-crop-upload');

if(modalProfileInput){
    modalProfileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if(!file) return;
        const url = URL.createObjectURL(file);
        if(modalImg){
            modalImg.src = url;
        }
        // initialize cropper after image loads
        modalImg.onload = () => {
            if(window.Cropper === undefined){
                console.error('Cropper.js not loaded');
                return;
            }
            if(cropper) cropper.destroy();
            cropper = new Cropper(modalImg, { aspectRatio: 1, viewMode: 1, background: false });
            if(modalCropBtn) modalCropBtn.style.display = 'inline-block';
            openImageModal();
        };
    });
}

if(modalCropBtn){
    modalCropBtn.addEventListener('click', () => {
        if(!cropper) return;
        cropper.getCroppedCanvas({ width: 400, height: 400 }).toBlob((blob) => {
            const fd = new FormData();
            fd.append('profile_image', blob, 'profile.png');
            fetch('/upload-profile-image', { method: 'POST', body: fd })
                .then(() => window.location.reload())
                .catch(() => window.location.reload());
        }, 'image/png');
    });
}


// Load full policy pages into right panel when links inside the privacy panel are clicked
panel.addEventListener('click', (e) => {

    const link = e.target.closest('.popup-links a, .help-action a');

    if(!link) return;

    e.preventDefault();

    const url = link.getAttribute('href');

    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(res => res.text())
        .then(html => {

            // parse response and extract the main content if present
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const main = doc.querySelector('main.static-page') || doc.querySelector('main');
            const content = main ? main.innerHTML : html;

            // hide other sections
            const sections = panel.querySelectorAll('.panel-section');
            sections.forEach(s => s.classList.remove('active'));

            // find or create a content section for policies
            let contentSection = panel.querySelector('.panel-section[data-panel="policy-content"]');

            if(!contentSection){
                const inner = panel.querySelector('.right-panel-inner');
                contentSection = document.createElement('div');
                contentSection.className = 'panel-section active';
                contentSection.setAttribute('data-panel','policy-content');
                inner.appendChild(contentSection);
            }

            contentSection.classList.add('active');
            contentSection.innerHTML = content;

            panel.setAttribute('aria-hidden','false');
            const layout = document.querySelector('.profile-layout');
            if(layout) layout.classList.add('panel-active');

            window.scrollTo({ top: 0, behavior: 'smooth' });

        })
        .catch(err => console.error('Error loading policy page:', err));

});


// CAR EDIT HANDLING
document.addEventListener('click', (e) => {

    // Edit button clicked
    const editBtn = e.target.closest('.edit-car-btn');

    if(editBtn){

        const carId = editBtn.dataset.carId;

        // fetch car data
        fetch(`/api/car/${carId}`)
            .then(res => res.json())
            .then(data => {

                const area = document.querySelector('.car-edit-area');

                if(!area) return;

                document.getElementById('car_id').value = data.id || '';
                document.getElementById('registration_number').value = data.registration_number || '';
                document.getElementById('car_model').value = data.car_model || '';
                document.getElementById('car_brand').value = data.car_brand || '';
                document.getElementById('car_colour').value = data.car_colour || '';

                area.style.display = 'block';

            })
            .catch(err => console.error('Failed to load car:', err));

    }

});

// Cancel edit
const cancelBtn = document.getElementById('cancel-car-edit');
if(cancelBtn){
    cancelBtn.addEventListener('click', () => {
        const area = document.querySelector('.car-edit-area');
        if(area) area.style.display = 'none';
    });
}

// Submit edit form (fallback to normal POST)
const carEditForm = document.getElementById('car-edit-form');
if(carEditForm){
    carEditForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const id = document.getElementById('car_id').value;

        const formData = new FormData(carEditForm);

        fetch(`/update-car/${id}`, {
            method: 'POST',
            body: formData
        }).then(() => {
            // on success, reload the page to reflect changes
            window.location.reload();
        }).catch(err => {
            console.error('Failed to update car', err);
            window.location.reload();
        });

    });
}