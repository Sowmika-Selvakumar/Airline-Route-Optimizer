document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const submitBtn = document.querySelector("button[type='submit']");

    form.addEventListener("submit", () => {
        submitBtn.disabled = true;
        submitBtn.textContent = "Finding route...";
    });

    window.addEventListener("pageshow", () => {
        submitBtn.disabled = false;
        submitBtn.textContent = "Find Route";
    });
});
