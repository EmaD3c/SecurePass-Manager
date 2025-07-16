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
    if (!token) {
        alert("Token not found. Please log in again.");
        window.location.href = "index.html";
        return;
    }

    await loadAndDisplayPasswords(token);

    const logoutLink = document.getElementById('logoutLink');
    if (logoutLink) {
        logoutLink.addEventListener('click', function (e) {
            e.preventDefault();
            logout();
        });
    }

    function logout() {
        document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=Strict";
        window.location.href = "index.html";
    }

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

    // close the modal
    document.getElementById("closeModal").addEventListener("click", function () {
        document.getElementById("editModal").style.display = "none";
    });
});

async function loadAndDisplayPasswords(token) {
    try {
        const passwords = await listPasswords(token);
        displayPasswords(passwords);
    } catch (error) {
        console.error("Failed to load passwords:", error);
    }
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
        <div class="entry-info">
          <h3>${password.name}</h3>
          <div class="entry-row">
            <p class="username"><strong>Username:</strong> ${password.username}</p>
            <div class="password-row">
              <span class="password-label">Password:</span>
              <span class="password-value">••••••••</span>
              <button class="show-password" data-password="${password.password}">Show</button>
            </div>
          </div>
        </div>
        <div class="entry-actions">
          <button class="edit-btn" data-id="${password.id}" data-password="${password.password}">✏️ Edit</button>
          <button class="delete-btn" data-id="${password.id}">🗑 Delete</button>
        </div>
      `;

        passwordList.appendChild(passwordElement);
    });

    // Show/hide password toggle
    document.querySelectorAll('.show-password').forEach(btn => {
        btn.addEventListener('click', function () {
            const valueSpan = this.previousElementSibling;
            const actualPassword = this.dataset.password;
            const hidden = valueSpan.textContent === '••••••••';

            valueSpan.textContent = hidden ? actualPassword : '••••••••';
            this.textContent = hidden ? 'Hide' : 'Show';
        });
    });

    // Delete password
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', async function () {
            const passwordId = this.dataset.id;
            const token = getCookie("token");

            if (confirm("Are you sure you want to delete this password?")) {
                try {
                    const response = await fetch("http://localhost:8000/api/auth/delete_password", {
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

    // Open modal
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const modal = document.getElementById("editModal");
            const input = document.getElementById("newPasswordInput");
            const passwordId = this.dataset.id;

            modal.dataset.id = passwordId;
            input.value = this.dataset.password;
            modal.style.display = "flex";
        });
    });

    // Update password
    document.getElementById("savePasswordBtn").addEventListener("click", async function () {
        const modal = document.getElementById("editModal");
        const newPassword = document.getElementById("newPasswordInput").value;
        const passwordId = modal.dataset.id;
        const token = getCookie("token");

        try {
            const response = await fetch("http://localhost:8000/api/auth/update_password", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    password_id: parseInt(passwordId),
                    new_password: newPassword
                })
            });

            if (response.ok) {
                alert("Password updated successfully!");
                modal.style.display = "none";
                await loadAndDisplayPasswords(token);
            } else {
                const error = await response.json();
                alert("Error: " + (error.error || "Failed to update password"));
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while updating the password.");
        }
    });
}
