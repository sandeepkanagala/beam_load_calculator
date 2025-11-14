// Login Modal Functions
function openModal() {
    document.getElementById("signinModal").style.display = "block";
}

function closeModal() {
    document.getElementById("signinModal").style.display = "none";
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById("signinModal");
    if (event.target === modal) {
        closeModal();
    }
};

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});

