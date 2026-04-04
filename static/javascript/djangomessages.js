document.querySelectorAll('.message').forEach((msg) => {

    // Auto remove after 4s
    setTimeout(() => {
        msg.style.animation = "fadeOut 0.4s ease forwards";
        setTimeout(() => msg.remove(), 400);
    }, 4000);

    // Close button
    msg.querySelector('.close-btn').addEventListener('click', () => {
        msg.style.animation = "fadeOut 0.3s ease forwards";
        setTimeout(() => msg.remove(), 300);
    });
});
