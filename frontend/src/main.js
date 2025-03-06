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
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (response.ok) {
      console.log("Token reçu :", data.token);
      localStorage.setItem("token", data.token);

  } else {
      console.error("Erreur de connexion :", data.error);
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
