document.addEventListener("DOMContentLoaded", () => {
  const cookies = document.cookie.split("; ").reduce((acc, cookie) => {
    const [key, value] = cookie.split("=");
    acc[key] = value;
    return acc;
  }, {});

  if (!cookies.token) {
    window.location.href = "index.html";
  }
});
