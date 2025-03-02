document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("togglePremium");
    const content = document.getElementById("premiumContent");

    toggleButton.addEventListener("click", function () {
        if (content.style.maxHeight === "0px" || content.style.maxHeight === "") {
            content.style.maxHeight = content.scrollHeight + "px";
        } else {
            content.style.maxHeight = "0px";
        }
    });
});