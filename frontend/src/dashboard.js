function getCookie(name) {
  // .split(';') divise la chaine en un tableau de cookie individuel
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
      // .trim() enleve les espaces inutiles autour du cookie
      const [key, value] = cookie.trim().split('=');
      if (key === name) return value;
  }
  return null;
}

document.addEventListener("DOMContentLoaded", () => {
  const token = getCookie("token");
  console.log("Token trouvé :", token);

  if (!token) {
      alert("Token non trouvé. Veuillez vous reconnecter.");
      window.location.href = "index.html";
      return;
  }

  listPassword(token)


  const addPasswordForm = document.getElementById('addPasswordForm');
  if (addPasswordForm) {
      addPasswordForm.addEventListener('submit', async function(event) {
          event.preventDefault();

          const name = document.getElementById('name').value;
          const password = document.getElementById('password').value;

          if (!name || !password) {
              alert("Veuillez remplir tous les champs requis.");
              return;
          }

          try {
              const response = await fetch("http://localhost:8000/api/auth/add_password", {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                      "Authorization": `Bearer ${token}`
                  },
                  body: JSON.stringify({ name, password }),
              });

              if (response.ok) {
                  const data = await response.json();
                  console.log("Réponse du serveur :", data);
                  alert("Mot de passe ajouté avec succès !");
                  window.location.reload();
              } else {
                  const errorData = await response.json();
                  console.error("Détails de l'erreur :", errorData);
                  alert("Erreur lors de l'ajout du mot de passe : " + (errorData.msg || "Erreur inconnue"));
              }
          } catch (error) {
              console.error("Erreur :", error);
              alert("Une erreur s'est produite. Veuillez réessayer.");
          }
      });
  }
});

async function listPassword(token) {
  const response = await fetch("http://localhost:8000/api/auth/list_passwords", {
      method: "GET",
      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
    });
      const data = await response.json();
      console.log(data)
      return data
  }
