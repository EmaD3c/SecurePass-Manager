async function registerUser(email, password) {
  const response = await fetch("http://localhost:8000/api/auth/register", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
  });

  const data = await response.json();
  console.log(data);
}

async function loginUser(email, password) {
  const response = await fetch("http://localhost:8000/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (response.ok) {
    const data = await response.json();
    const token = data.access_token;
    document.cookie = `token=${token}; path=/; Secure; SameSite=Strict`;
    console.log("Token enregistré :", token);
    window.location.href = "dashboard.html";
  } else {
    alert("Login failed");
  }
}


// butons

document.getElementById("register-btn").addEventListener("click", () => {
  const email = document.getElementById("register-email").value;
  const password = document.getElementById("register-password").value;
  registerUser(email, password);
});

document.getElementById("login-btn").addEventListener("click", () => {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;
  loginUser(email, password);
});
