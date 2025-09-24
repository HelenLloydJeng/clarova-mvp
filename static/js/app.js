// static/js/app.js

document.addEventListener('DOMContentLoaded', function () {
  // ✅ Confirm script is loaded
  console.log("Clarova JS loaded.");

  // 🔁 Toggle lesson descriptions
  const toggles = document.querySelectorAll('.lesson-toggle');
  toggles.forEach(toggle => {
    toggle.addEventListener('click', () => {
      const targetId = toggle.getAttribute('data-target');
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        targetEl.classList.toggle('hidden');
      }
    });
  });

  // 🛑 Confirm before deleting scenarios
  const deleteButtons = document.querySelectorAll('.btn-delete-scenario');
  deleteButtons.forEach(btn => {
    btn.addEventListener('click', function (event) {
      const confirmDelete = confirm("Are you sure you want to delete this scenario?");
      if (!confirmDelete) {
        event.preventDefault();
      }
    });
  });

  // ⚠️ Simple form validation
  const requiredForms = document.querySelectorAll('form.validate-required');
  requiredForms.forEach(form => {
    form.addEventListener('submit', function (event) {
      const requiredFields = form.querySelectorAll('[required]');
      let valid = true;
      requiredFields.forEach(field => {
        if (!field.value.trim()) {
          field.classList.add('input-error');
          valid = false;
        } else {
          field.classList.remove('input-error');
        }
      });
      if (!valid) {
        event.preventDefault();
        alert("Please fill in all required fields.");
      }
    });
  });
  // ↑ Back to Top button
  const backBtn = document.createElement("button");
  backBtn.innerText = "↑ Back to Top";
  backBtn.id = "back-to-top";
  backBtn.setAttribute("aria-label", "Back to top");
  backBtn.classList.add("back-to-top"); // use CSS instead of inline styles
  document.body.appendChild(backBtn);

  window.addEventListener("scroll", function () {
    backBtn.style.display = window.scrollY > 200 ? "block" : "none";
  });

  backBtn.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});
