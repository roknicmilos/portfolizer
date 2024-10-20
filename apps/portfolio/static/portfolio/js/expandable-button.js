document.addEventListener("DOMContentLoaded", function () {
    if (isMobileDevice()) {
        initMobileDeviceExpandableButtons();
    } else {
        initDesktopDeviceExpandableButtons();
    }
});

function isMobileDevice() {
    return (
        /Mobi|Android|iPhone|iPad|iPod|Opera Mini|IEMobile|WPDesktop/.test(navigator.userAgent)
        || window.matchMedia("(max-width: 767px)").matches
    );
}

function initMobileDeviceExpandableButtons() {
    const expandableButtons = document.querySelectorAll(".js-expendable-button");

    expandableButtons.forEach(function (expandableButton) {
        let isExpanded = false;
        /**
         * Prevent default action of the button if it is not expanded and expand it.
         * Allow the default action if the button is expanded and collapse it.
         */
        expandableButton.addEventListener("click", function (event) {
            isExpanded = !isExpanded;
            if (isExpanded) {
                event.preventDefault();
                expandableButton.classList.add("expanded");
            } else {
                expandableButton.classList.remove("expanded");
            }
        });

        /**
         * Collapse the button if the user clicks outside the button.
         */
        document.addEventListener("click", function (event) {
            if (isExpanded && !expandableButton.contains(event.target)) {
                expandableButton.classList.remove("expanded");
                isExpanded = false;
            }
        });
    });
}

function initDesktopDeviceExpandableButtons() {
    const expandableButtons = document.querySelectorAll(".js-expendable-button");

    expandableButtons.forEach(function (expandableButton) {
        let isExpanded = false;

        /**
         * Expand the button when the user hovers over it.
         */
        expandableButton.addEventListener("mouseover", function () {
            isExpanded = true;
            expandableButton.classList.add("expanded");
        });

        /**
         * Collapse the button when the user moves the cursor away from it.
         */
        expandableButton.addEventListener("mouseout", function () {
            expandableButton.classList.remove("expanded");
            isExpanded = false;
        });
    });
}
