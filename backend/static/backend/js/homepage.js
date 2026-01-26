// ========== ACCOUNT SIDEBAR ==========
const accountBtn = document.getElementById("accountBtn");
const accountSidebar = document.getElementById("accountSidebar");
const overlay = document.getElementById("overlay");
const closeSidebar = document.getElementById("closeSidebar");

function openAccountSidebar() {
    accountSidebar.classList.add("show");
    overlay.classList.add("show");
    document.body.style.overflow = "hidden";
}

function closeAccountSidebar() {
    accountSidebar.classList.remove("show");
    overlay.classList.remove("show");
    document.body.style.overflow = "auto";
}

accountBtn.addEventListener("click", openAccountSidebar);
closeSidebar.addEventListener("click", closeAccountSidebar);
overlay.addEventListener("click", closeAccountSidebar);

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && accountSidebar.classList.contains("show")) {
        closeAccountSidebar();
    }
});


// ========== MODALS ==========
const personalModal = document.getElementById("personalModal");
const historyModal = document.getElementById("historyModal");
const likedModal = document.getElementById("likedModal");

const closePersonalModal = document.getElementById("closePersonalModal");
const closeHistoryModal = document.getElementById("closeHistoryModal");
const closeLikedModal = document.getElementById("closeLikedModal");

// Open Modal Function
function openModal(modal) {
    modal.classList.add("show");
    document.body.style.overflow = "hidden";
}

// Close Modal Function
function closeModal(modal) {
    modal.classList.remove("show");
    document.body.style.overflow = "auto";
}

// Close buttons
closePersonalModal.addEventListener("click", () => closeModal(personalModal));
closeHistoryModal.addEventListener("click", () => closeModal(historyModal));
closeLikedModal.addEventListener("click", () => closeModal(likedModal));

// Close modal when clicking outside
[personalModal, historyModal, likedModal].forEach(modal => {
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            closeModal(modal);
        }
    });
});

// ESC key to close modals
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        closeModal(personalModal);
        closeModal(historyModal);
        closeModal(likedModal);
    }
});


// ========== PERSONAL DETAILS ==========
document.getElementById("personalDetails").addEventListener("click", async () => {
    console.log("Personal Details clicked");
    closeAccountSidebar();
    openModal(personalModal);

    const content = document.getElementById("personalDetailsContent");
    content.innerHTML = '<div class="loading">Loading...</div>';

    try {
        const response = await fetch('/api/personal-details/');
        const data = await response.json();

        content.innerHTML = `
            <div class="detail-item">
                <div class="detail-label">Full Name</div>
                <div class="detail-value">${data.full_name}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Username</div>
                <div class="detail-value">@${data.username}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Email Address</div>
                <div class="detail-value">${data.email}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Member Since</div>
                <div class="detail-value">${data.date_joined}</div>
            </div>
        `;
    } catch (error) {
        console.error("Error fetching personal details:", error);
        content.innerHTML = '<div class="empty-state"><p>Failed to load personal details</p></div>';
    }
});


// ========== RECENT HISTORY - 🔥 UPDATED ==========
document.getElementById("recentHistory").addEventListener("click", async () => {
    console.log("Recent History clicked");
    closeAccountSidebar();
    openModal(historyModal);

    const content = document.getElementById("historyContent");
    content.innerHTML = '<div class="loading">Loading...</div>';

    try {
        // 🔥 ADD: Disable cache
        const response = await fetch('/api/recent-history/', {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        });
        const data = await response.json();

        // 🔥 ADD: Console log to verify user data
        console.log('Recent History Data:', data);
        console.log('Number of songs:', data.songs.length);

        if (data.songs.length === 0) {
            content.innerHTML = `
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="M12 6v6l4 2"/>
                    </svg>
                    <p>No songs played yet. Start listening to build your history!</p>
                </div>
            `;
            return;
        }

        const songsHTML = data.songs.map(song => `
            <div class="song-item">
                <img src="${song.cover}" alt="${song.title}" class="song-cover">
                <div class="song-info">
                    <div class="song-title">${song.title}</div>
                    <div class="song-artist">${song.artist}</div>
                </div>
                <div class="song-meta">
                    <span class="song-duration">${song.duration}</span>
                    <span class="song-time">${song.played_at}</span>
                </div>
            </div>
        `).join('');

        content.innerHTML = `<div class="song-list">${songsHTML}</div>`;
    } catch (error) {
        console.error("Error fetching recent history:", error);
        content.innerHTML = '<div class="empty-state"><p>Failed to load recent history</p></div>';
    }
});


// ========== LIKED SONGS - 🔥 UPDATED ==========
document.getElementById("likedSongs").addEventListener("click", async () => {
    console.log("Liked Songs clicked");
    closeAccountSidebar();
    openModal(likedModal);

    const content = document.getElementById("likedContent");
    content.innerHTML = '<div class="loading">Loading...</div>';

    try {
        // 🔥 ADD: Disable cache
        const response = await fetch('/api/liked-songs/', {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        });
        const data = await response.json();

        // 🔥 ADD: Console log to verify user data
        console.log('Liked Songs Data:', data);
        console.log('Number of liked songs:', data.songs.length);

        if (data.songs.length === 0) {
            content.innerHTML = `
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                    </svg>
                    <p>No liked songs yet. Start liking songs to see them here!</p>
                </div>
            `;
            return;
        }

        const songsHTML = data.songs.map(song => `
            <div class="song-item">
                <img src="${song.cover}" alt="${song.title}" class="song-cover">
                <div class="song-info">
                    <div class="song-title">${song.title}</div>
                    <div class="song-artist">${song.artist}</div>
                </div>
                <div class="song-meta">
                    <span class="song-duration">${song.duration}</span>
                    <span class="song-time">Liked ${song.liked_at}</span>
                </div>
            </div>
        `).join('');

        content.innerHTML = `<div class="song-list">${songsHTML}</div>`;
    } catch (error) {
        console.error("Error fetching liked songs:", error);
        content.innerHTML = '<div class="empty-state"><p>Failed to load liked songs</p></div>';
    }
});

// ========== HELPER FUNCTIONS FOR SONG PAGES ==========

// Call this function when a song is played
async function trackSongPlay(songId) {
    try {
        const response = await fetch(`/api/track-play/${songId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        const data = await response.json();
        console.log('Song play tracked:', data);
    } catch (error) {
        console.error('Error tracking song play:', error);
    }
}

// Call this function when like button is clicked
async function toggleLikeSong(songId) {
    try {
        const response = await fetch(`/api/like-song/${songId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        const data = await response.json();
        console.log('Like toggled:', data);
        return data;
    } catch (error) {
        console.error('Error toggling like:', error);
    }
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Export functions for use in other pages
window.trackSongPlay = trackSongPlay;
window.toggleLikeSong = toggleLikeSong;