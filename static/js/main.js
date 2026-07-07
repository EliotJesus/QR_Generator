document.addEventListener("DOMContentLoaded", () => {
    const copyButtons = document.querySelectorAll(".copy-button");

    copyButtons.forEach((button) => {
        button.addEventListener("click", async () => {
            const textToCopy = button.dataset.copy;

            if (!textToCopy) {
                return;
            }

            try {
                await navigator.clipboard.writeText(textToCopy);

                const originalText = button.textContent;
                button.textContent = "Copiado";

                setTimeout(() => {
                    button.textContent = originalText;
                }, 1400);
            } catch (error) {
                alert("No se pudo copiar el enlace.");
            }
        });
    });

    const toasts = document.querySelectorAll(".toast");

    toasts.forEach((toast) => {
        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateY(-10px)";
            toast.style.transition = "all 0.25s ease";

            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    });
});