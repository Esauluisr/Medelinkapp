document.querySelectorAll(".input100").forEach((input) => {
  input.addEventListener("input", function () {
    if (this.value.trim() !== "") {
      this.classList.add("has-val");
    } else {
      this.classList.remove("has-val");
    }
  });
});

document.querySelectorAll(".btn-show-pass").forEach((button) => {
  button.addEventListener("click", () => {
    const input = button.nextElementSibling;
    const icon = button.querySelector("i");

    if (input.type === "password") {
      input.type = "text";
      icon.classList.replace("bx-show-alt", "bx-hide");
    } else {
      input.type = "password";
      icon.classList.replace("bx-hide", "bx-show-alt");
    }
  });
});
