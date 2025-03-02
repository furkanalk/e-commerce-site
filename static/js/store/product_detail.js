let defaultTransform = 0;
function goNext() {
    defaultTransform = defaultTransform - 498;
    var slider = document.getElementById("slider");
    if (Math.abs(defaultTransform) >= slider.scrollWidth / 1.7) defaultTransform = 0;
    slider.style.transform = "translateX(" + defaultTransform + "px)";
}
next.addEventListener("click", goNext);
function goPrev() {
    var slider = document.getElementById("slider");
    if (Math.abs(defaultTransform) === 0) defaultTransform = 0;
    else defaultTransform = defaultTransform + 498;
    slider.style.transform = "translateX(" + defaultTransform + "px)";
}
prev.addEventListener("click", goPrev);
