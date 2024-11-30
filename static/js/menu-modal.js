document.addEventListener("DOMContentLoaded", function () {
    prepareLanguageModal();
});

function prepareLanguageModal() {
    const mainMenu = document.querySelector(".js-main-menu");
    const mainMenuBurger = document.querySelector(".js-main-menu-burger");

    // Activate the menu when the burger is clicked:
    mainMenuBurger.addEventListener("click", () => {
        mainMenu.classList.add("menu__right--active");
        console.log("OPEN MENU");
    });

    // Deactivate the menu when the menu background is clicked:
    mainMenu.addEventListener("click", (event) => {
        // TODO: Prevent closing the menu if a child element inside the menu is clicked
        if (event.target !== mainMenu) return;
        mainMenu.classList.remove("menu__right--active");
        console.log("CLOSE MENU");
    });
}
