// Account Sidebar Elements
        const accountBtn = document.getElementById("accountBtn");
        const accountSidebar = document.getElementById("accountSidebar");
        const overlay = document.getElementById("overlay");
        const closeSidebar = document.getElementById("closeSidebar");

        // Account Sidebar Functions
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

       // Account Event Listeners
        accountBtn.addEventListener("click", openAccountSidebar);
        closeSidebar.addEventListener("click", closeAccountSidebar);
        overlay.addEventListener("click", closeAccountSidebar);

        // Menu Item Event Listeners
        document.getElementById("personalDetails").addEventListener("click", () => {
            console.log("Personal Details clicked");
            closeAccountSidebar();
            alert("Personal Details - Feature coming soon!");
        });

        document.getElementById("recentHistory").addEventListener("click", () => {
            console.log("Recent History clicked");
            closeAccountSidebar();
            alert("Recent History - Feature coming soon!");
        });

        document.getElementById("privacy").addEventListener("click", () => {
            console.log("Privacy clicked");
            closeAccountSidebar();
            alert("Privacy Settings - Feature coming soon!");
        });

        document.getElementById("security").addEventListener("click", () => {
            console.log("Security clicked");
            closeAccountSidebar();
            alert("Security Settings - Feature coming soon!");
        });

        // Close sidebar with ESC key
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && accountSidebar.classList.contains("show")) {
                closeAccountSidebar();
            }
        });

        // Search Functionality
        document.querySelector('.search-btn').addEventListener('click', () => {
            const query = document.querySelector('.search-input').value;
            if (query.trim()) {
                console.log("Searching for:", query);
                alert(`Searching for: ${query} - Songs Feature coming soon!`);
            }
        });

        // Search on Enter key
        document.querySelector('.search-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                document.querySelector('.search-btn').click();
            }
        });