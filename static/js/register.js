document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    if (!form) return;

    const firstName = document.querySelector("input[name='first_name']");
    const lastName = document.querySelector("input[name='last_name']");
    const fatherName = document.querySelector("input[name='father_name']");
    const mobile = document.querySelector("input[name='mobile']");
    const photo = document.querySelector("input[name='photo']");
    const plan = document.querySelector("select[name='membership_plan']");

    function showError(input, message) {
        input.classList.add("is-invalid");
        input.classList.remove("is-valid");
        let errorDiv = input.parentElement.querySelector(".invalid-feedback-custom");
        if (!errorDiv) {
            errorDiv = document.createElement("div");
            errorDiv.className = "invalid-feedback-custom";
            input.parentElement.appendChild(errorDiv);
        }
        errorDiv.innerText = message;
        errorDiv.style.display = "block";
    }

    function showSuccess(input) {
        input.classList.remove("is-invalid");
        input.classList.add("is-valid");
        let errorDiv = input.parentElement.querySelector(".invalid-feedback-custom");
        if (errorDiv) {
            errorDiv.style.display = "none";
        }
    }

    const nameRegex = /^[A-Za-z\s]{2,30}$/;
    const mobileRegex = /^[6-9]\d{9}$/;

    if(firstName) {
        firstName.addEventListener("input", () => {
            if (!nameRegex.test(firstName.value.trim())) {
                showError(firstName, "⚠️ Enter a valid first name (letters only, min 2 chars).");
            } else {
                showSuccess(firstName);
            }
        });
    }

    if(lastName) {
        lastName.addEventListener("input", () => {
            if (!nameRegex.test(lastName.value.trim())) {
                showError(lastName, "⚠️ Enter a valid last name (letters only).");
            } else {
                showSuccess(lastName);
            }
        });
    }

    if(fatherName) {
        fatherName.addEventListener("input", () => {
            if (!nameRegex.test(fatherName.value.trim())) {
                showError(fatherName, "⚠️ Enter a valid father's name (letters only).");
            } else {
                showSuccess(fatherName);
            }
        });
    }

    if(mobile) {
        mobile.addEventListener("input", () => {
            if (!mobileRegex.test(mobile.value.trim())) {
                showError(mobile, "⚠️ Enter a valid 10-digit Indian mobile number starting with 6-9.");
            } else {
                showSuccess(mobile);
            }
        });
    }

    if(photo) {
        photo.addEventListener("change", () => {
            const file = photo.files[0];
            if (file) {
                const fileType = file.type;
                const validTypes = ["image/jpeg", "image/png", "image/jpg"];
                if (!validTypes.includes(fileType)) {
                    showError(photo, "⚠️ Only JPG, JPEG or PNG image formats are allowed.");
                    photo.value = "";
                } else if (file.size > 2 * 1024 * 1024) {
                    showError(photo, "⚠️ Image size must be less than 2MB.");
                    photo.value = "";
                } else {
                    showSuccess(photo);
                }
            }
        });
    }

    form.addEventListener("submit", function (event) {
        let isValid = true;

        if (firstName && !nameRegex.test(firstName.value.trim())) {
            showError(firstName, "⚠️ First name is required and must be valid.");
            isValid = false;
        }
        if (lastName && !nameRegex.test(lastName.value.trim())) {
            showError(lastName, "⚠️ Last name is required and must be valid.");
            isValid = false;
        }
        if (fatherName && !nameRegex.test(fatherName.value.trim())) {
            showError(fatherName, "⚠️ Father's name is required and must be valid.");
            isValid = false;
        }
      if (mobile && !mobileRegex.test(mobile.value.trim())) {
            showError(mobile, "⚠️ Valid 10-digit mobile number is mandatory.");
            isValid = false;
        }
        if (photo && photo.files.length === 0) {
            showError(photo, "⚠️ Please upload your passport size photo.");
            isValid = false;
        }
        if (plan && !plan.value) {
            plan.classList.add("is-invalid");
            isValid = false;
        } else if(plan) {
            plan.classList.remove("is-invalid");
            plan.classList.add("is-valid");
        }

        if (!isValid) {
            event.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
});