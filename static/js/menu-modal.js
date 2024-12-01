document.addEventListener("DOMContentLoaded", function () {
    prepareLanguageModal();
});

function prepareLanguageModal() {
    const mainMenu = document.querySelector(".js-main-menu");
    const mainMenuBurger = document.querySelector(".js-main-menu-burger");

    // Activate the menu when the burger is clicked:
    mainMenuBurger.addEventListener("click", () => {
        mainMenu.classList.add("menu__main--opened");
    });

    // Deactivate the menu when the menu background is clicked:
    mainMenu.addEventListener("click", (event) => {
        // Prevent closing the menu if a child element inside the menu is clicked
        if (event.target !== mainMenu) return;
        mainMenu.classList.remove("menu__main--opened");
    });
}
