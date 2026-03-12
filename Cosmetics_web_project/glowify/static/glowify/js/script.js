const placeholders = [
    "Search lipsticks...",
    "Search foundations...",
    "Search skincare...",
    "Search blush..."
];

let index = 0;
const input = document.getElementById("searchInput");

setInterval(() => {
    index = (index + 1) % placeholders.length;
    input.setAttribute("placeholder", placeholders[index]);
}, 2000); // change every 2 seconds


// wishlist by heart tag
// ================= SEARCH PLACEHOLDER ROTATOR =================
document.addEventListener("DOMContentLoaded", function () {
    const placeholders = [
        "Search lipsticks...",
        "Search foundations...",
        "Search skincare...",
        "Search blush..."
    ];

    const input = document.getElementById("searchInput");
    if (!input) return;   // prevents error on pages without search

    let index = 0;

    setInterval(() => {
        index = (index + 1) % placeholders.length;
        input.placeholder = placeholders[index];
    }, 2000);
});


// ================= WISHLIST HEART TOGGLE =================
function toggleFavorite(btn, productId) {
    fetch(`/wishlist/toggle/${productId}/`)
        .then(res => res.json())
        .then(data => {
            const icon = btn.querySelector("i");

            if (data.status === "added") {
                btn.classList.add("active");
                icon.classList.remove("far");
                icon.classList.add("fas");
            } else {
                btn.classList.remove("active");
                icon.classList.remove("fas");
                icon.classList.add("far");
            }
        })
        .catch(err => console.error("Wishlist error:", err));
}

// Simple toggle function
function toggleFilter(header) {
    // Find the parent filter-item
    const filterItem = header.closest('.filter-item');

    // Toggle the active class
    filterItem.classList.toggle('active');
}

// Make sure all filters are visible by default when page loads
document.addEventListener('DOMContentLoaded', function () {
    // Add 'active' class to all filter items if they don't have it
    document.querySelectorAll('.filter-item').forEach(item => {
        item.classList.add('active');
    });
});


let currentIndex = 0;
const slides = document.querySelectorAll(".hero-slide");
const slider = document.querySelector(".hero-slider");

function updateSlider() {
    slider.style.transform = `translateX(-${currentIndex * 100}%)`;
}

function nextSlide() {
    currentIndex = (currentIndex + 1) % slides.length;
    updateSlider();
}

function prevSlide() {
    currentIndex = (currentIndex - 1 + slides.length) % slides.length;
    updateSlider();
}

/* Auto Slide */
setInterval(nextSlide, 4000);



const autoFillData = {
    firstName: "Narmatha",
    lastName: "Tharmaraj",
    mobile: "1234567890",
    address: "123 Luxury street,",
    city: "Tenkasi",
    state: "TamilNadu",
    pincode: "627859"
};

Object.keys(autoFillData).forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener("focus", () => {
        if (el.value.trim() === "") {
            el.value = autoFillData[id];
        }
    });
});

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function () {
    // Create mobile menu toggle button
    const header = document.querySelector('.nav-container');
    const navLinks = document.querySelector('.nav-links');
    const searchBox = document.querySelector('.search-box');
    const navIcons = document.querySelector('.nav-icons');

    // Add mobile menu toggle if it doesn't exist
    if (!document.querySelector('.mobile-menu-toggle')) {
        const toggle = document.createElement('div');
        toggle.className = 'mobile-menu-toggle';
        toggle.innerHTML = '<span></span><span></span><span></span>';

        // Insert after logo or at beginning of nav-container
        const logo = document.querySelector('.logo');
        if (logo) {
            logo.after(toggle);
        } else {
            header.prepend(toggle);
        }

        // Toggle menu
        toggle.addEventListener('click', function () {
            navLinks.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Handle dropdowns on mobile
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function (e) {
            if (window.innerWidth <= 767) {
                e.preventDefault();
                this.classList.toggle('active');
            }
        });
    });

    // Handle search icon on mobile
    const searchIcon = document.querySelector('.nav-icons img[alt*="Search"]');
    if (searchIcon) {
        searchIcon.addEventListener('click', function () {
            if (window.innerWidth <= 767) {
                document.body.classList.toggle('mobile-search-active');
                const searchBox = document.querySelector('.search-box');
                if (searchBox) {
                    searchBox.style.display = searchBox.style.display === 'none' ? 'flex' : 'none';
                }
            }
        });
    }

    // Close menus when clicking outside
    document.addEventListener('click', function (e) {
        if (window.innerWidth <= 767) {
            if (!e.target.closest('.nav-container')) {
                navLinks.classList.remove('active');
                document.querySelectorAll('.dropdown').forEach(d => d.classList.remove('active'));
                document.body.classList.remove('mobile-search-active');
            }
        }
    });

    // Handle window resize
    window.addEventListener('resize', function () {
        if (window.innerWidth > 767) {
            // Reset mobile styles
            navLinks.classList.remove('active');
            navLinks.style.display = 'flex';
            document.querySelectorAll('.dropdown').forEach(d => d.classList.remove('active'));
            document.body.classList.remove('mobile-search-active');

            // Reset search box
            const searchBox = document.querySelector('.search-box');
            if (searchBox) {
                searchBox.style.display = 'flex';
            }
        } else {
            // Set mobile defaults
            const searchBox = document.querySelector('.search-box');
            if (searchBox && !document.body.classList.contains('mobile-search-active')) {
                searchBox.style.display = 'none';
            }
        }
    });

    // Trigger resize on load
    window.dispatchEvent(new Event('resize'));
});
