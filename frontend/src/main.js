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

document.addEventListener('DOMContentLoaded', () => {
  // Récupérer les éléments du DOM
  const showLoginButton = document.getElementById('show-login');
  const showRegisterButton = document.getElementById('show-register');
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');

  // Afficher le formulaire de connexion
  showLoginButton.addEventListener('click', () => {
      loginForm.classList.add('active');
      registerForm.classList.remove('active');
      showLoginButton.classList.add('active');
      showRegisterButton.classList.remove('active');
  });

  // Afficher le formulaire d'inscription
  showRegisterButton.addEventListener('click', () => {
      registerForm.classList.add('active');
      loginForm.classList.remove('active');
      showRegisterButton.classList.add('active');
      showLoginButton.classList.remove('active');
  });

  // Gestion de la soumission du formulaire de connexion
  loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value;
      const password = document.getElementById('login-password').value;

      if (email && password) {
          alert('Connexion réussie !');
          window.location.href = '/dashboard.html'; // Redirection vers le tableau de bord
      } else {
          alert('Veuillez remplir tous les champs.');
      }
  });

  // Gestion de la soumission du formulaire d'inscription
  registerForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = document.getElementById('register-email').value;
      const password = document.getElementById('register-password').value;

      if (email && password) {
          alert('Inscription réussie !');
      } else {
          alert('Veuillez remplir tous les champs.');
      }
  });
});