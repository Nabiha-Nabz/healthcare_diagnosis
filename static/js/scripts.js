// Update your existing scripts.js with this content
document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation for password match
    function validatePassword() {
        const password = document.getElementById('password');
        const confirm_password = document.getElementById('confirm_password');
        
        if (password.value !== confirm_password.value) {
            confirm_password.setCustomValidity("Passwords don't match");
        } else {
            confirm_password.setCustomValidity('');
        }
    }

    // Attach password validation if forms exist
    const password = document.getElementById('password');
    const confirm_password = document.getElementById('confirm_password');
    
    if (password && confirm_password) {
        password.onchange = validatePassword;
        confirm_password.onkeyup = validatePassword;
    }

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Initialize particles if the element exists
    const particlesCanvas = document.getElementById('particles-js');
    if (particlesCanvas) {
        initParticles();
    }
});

// GSAP animations
if (typeof gsap !== 'undefined') {
    gsap.from(".navbar", {duration: 1, y: -100, opacity: 0, ease: "power4.out"});
    gsap.from(".hero-content", {duration: 1, y: 50, opacity: 0, delay: 0.3, ease: "power4.out"});
}

// Particles.js initialization
function initParticles() {
    const canvas = document.getElementById('particles-js');
    if (!canvas) return;

    const particles = [];
    const particleCount = window.innerWidth < 768 ? 30 : 60;

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.offsetWidth,
            y: Math.random() * canvas.offsetHeight,
            size: Math.random() * 5 + 2,
            speedX: Math.random() * 0.5 - 0.25,
            speedY: Math.random() * 0.5 - 0.25,
            color: `rgba(78, 115, 223, ${Math.random() * 0.4 + 0.1})`
        });
    }

    function updateParticles() {
        particles.forEach(particle => {
            particle.x += particle.speedX;
            particle.y += particle.speedY;

            if (particle.x > canvas.offsetWidth + 20 || particle.x < -20) {
                particle.speedX = -particle.speedX;
            }
            if (particle.y > canvas.offsetHeight + 20 || particle.y < -20) {
                particle.speedY = -particle.speedY;
            }
        });

        drawParticles();
        requestAnimationFrame(updateParticles);
    }

    function drawParticles() {
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.offsetWidth, canvas.offsetHeight);

        particles.forEach(particle => {
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fillStyle = particle.color;
            ctx.fill();
        });
    }

    // Handle resize
    window.addEventListener('resize', () => {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
    });

    // Initialize
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    updateParticles();
}