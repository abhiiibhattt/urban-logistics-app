document.addEventListener("DOMContentLoaded", () => {
    setupConfirmActions();
    preventDoubleSubmit();
    autoDismissFlashMessages();
    setupStatusAjax();
});

/* ---------- Confirm Destructive Actions ---------- */
function setupConfirmActions() {
    document.querySelectorAll("[data-confirm]").forEach(form => {
        form.addEventListener("submit", event => {
            if (!confirm(form.dataset.confirm)) {
                event.preventDefault();
            }
        });
    });
}

/* ---------- Prevent Double Submit ---------- */
function preventDoubleSubmit() {
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", () => {
            form.querySelectorAll("button[type='submit']").forEach(btn => {
                btn.disabled = true;
                btn.innerText = "Processing...";
            });
        });
    });
}

/* ---------- Flash Auto-dismiss ---------- */
function autoDismissFlashMessages() {
    document.querySelectorAll(".flash").forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = "0";
            setTimeout(() => flash.remove(), 400);
        }, 3500);
    });
}

function setupStatusAjax() {
    const form = document.getElementById("status-form");
    if (!form) return;

    form.addEventListener("submit", async event => {
        event.preventDefault();

        const deliveryId = form.dataset.deliveryId;
        const status = form.querySelector("select").value;
        const feedback = document.getElementById("status-feedback");

        feedback.innerText = "Updating...";

        const response = await fetch(`/deliveries/${deliveryId}/status/json`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status })
        });

        const data = await response.json();

        if (!data.success) {
            feedback.innerText = data.error;
            feedback.style.color = "#fca5a5";
            return;
        }

        location.reload(); // clean refresh, keeps logic simple
    });
}


