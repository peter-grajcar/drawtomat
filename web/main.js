function resizeTextarea() {
  var element = document.getElementById("description-input");
  window.setTimeout(() => {
    element.style.height = "auto";
    element.style.height = element.scrollHeight - 10 + "px";
  }, 0);
}

window.addEventListener("resize", resizeTextarea);
window.addEventListener("load", resizeTextarea);
