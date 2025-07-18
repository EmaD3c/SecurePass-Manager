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

  if (response.ok) {
    // Call login automatically after registration
    await loginUser(email, password);
  } else {
    alert(data.error || "Échec de l'inscription");
  }
}


async function loginUser(email, password) {
  const response = await fetch("http://localhost:8000/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (response.ok) {
    const data = await response.json();
    const Fulltoken = data.token;
    console.log("Réponse du serveur :", data);
    document.cookie = `token=${Fulltoken}; path=/; SameSite=Strict`;
    console.log("Token enregistré :", Fulltoken);
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
          loginUser(email, password)
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
        registerUser(email, password)
      } else {
          alert('Veuillez remplir tous les champs.');
      }
  });
});
