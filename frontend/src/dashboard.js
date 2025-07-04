function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value;
    }
    return null;
}

document.addEventListener("DOMContentLoaded", async () => {
    const token = getCookie("token");
    console.log("Token found:", token);

    if (!token) {
        alert("Token not found. Please log in again.");
        window.location.href = "index.html";
        return;
    }

    // Load and display passwords
    await loadAndDisplayPasswords(token);

    // Add logout handler
    const logoutLink = document.getElementById('logoutLink');
    if (logoutLink) {
        logoutLink.addEventListener('click', function (e) {
            e.preventDefault(); // avoids a default behavior of the link
            logout();
        });
    }

    function logout() {
        // Delete cookie for logout
        document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=Strict";
        console.log("Déconnexion réussie, redirection...");
        window.location.href = "index.html";
    }

    // Add password form handler
    const addPasswordForm = document.getElementById('addPasswordForm');
    if (addPasswordForm) {
        addPasswordForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            const service = document.getElementById('service').value;
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            if (!service || !password) {
                alert("Please fill in all required fields.");
                return;
            }

            try {
                const response = await fetch("http://localhost:8000/api/auth/add_password", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({ 
                        name: service,
                        username: username,
                        password: password 
                    }),
                });

                if (response.ok) {
                    alert("Password added successfully!");
                    addPasswordForm.reset();
                    await loadAndDisplayPasswords(token);
                } else {
                    const error = await response.json();
                    alert("Error: " + (error.error || "Failed to add password"));
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred. Please try again.");
            }
        });
    }
});


async function loadAndDisplayPasswords(token) {
    try {
        const passwords = await listPasswords(token);
        displayPasswords(passwords);
    } catch (error) {
        console.error("Failed to load passwords:", error);
    }
}

const logoutLink = document.getElementById('logoutLink');
if (logoutLink) {
    logoutLink.addEventListener('click', logout);
}

async function listPasswords(token) {
    const response = await fetch("http://localhost:8000/api/auth/list_passwords", {
        method: "GET",
        headers: { 
            "Content-Type": "application/json", 
            "Authorization": `Bearer ${token}` 
        },
    });
    
    if (!response.ok) {
        throw new Error("Failed to fetch passwords");
    }
    
    return await response.json();
}

function displayPasswords(passwords) {
    const passwordList = document.getElementById('passwordList');
    passwordList.innerHTML = '';

    if (!passwords || passwords.length === 0) {
        passwordList.innerHTML = '<p class="no-passwords">No passwords saved yet</p>';
        return;
    }

    passwords.forEach(password => {
        const passwordElement = document.createElement('div');
        passwordElement.className = 'password-entry';
        passwordElement.innerHTML = `
            <h3>${password.name}</h3>
            <p class="username">${password.username || 'Not specified'}</p>
            <div class="password-row">
                <span class="password-label">Password:</span>
                <span class="password-value">••••••••</span>
                <button class="show-password" data-password="${password.password}">Show</button>
            </div>
            <button class="delete-btn" data-id="${password.id}">Delete</button>
            <hr>
        `;
        passwordList.appendChild(passwordElement);
    });

    // Add event listeners for show password buttons
    document.querySelectorAll('.show-password').forEach(btn => {
        btn.addEventListener('click', function() {
            const passwordValue = this.getAttribute('data-password');
            const passwordDisplay = this.previousElementSibling;
            
            if (passwordDisplay.textContent === '••••••••') {
                passwordDisplay.textContent = passwordValue;
                this.textContent = 'Hide';
            } else {
                passwordDisplay.textContent = '••••••••';
                this.textContent = 'Show';
            }
        });
    });

 // Add event listeners for delete buttons
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', async function() {
            const passwordId = this.getAttribute('data-id');
            const token = getCookie("token");

            if (confirm("Are you sure you want to delete this password?")) {
                try {
                    const response = await fetch('http://localhost:8000/api/auth/delete_password', {
                        method: "DELETE",
                        headers: { 
                            "Content-Type": "application/json", 
                            "Authorization": `Bearer ${token}` 
                        },
                        body: JSON.stringify({ password_id: parseInt(passwordId) })
                    });

                    if (response.ok) {
                        alert("Password deleted successfully!");
                        await loadAndDisplayPasswords(token);
                    } else {
                        const error = await response.json();
                        alert("Error: " + (error.error || "Failed to delete password"));
                    }
                } catch (error) {
                    console.error("Error:", error);
                    alert("An error occurred. Please try again.");
                }
            }
        });
    });
}