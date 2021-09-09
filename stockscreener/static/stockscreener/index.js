document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".watchlist").forEach((watch_button) => {
    watch_button.addEventListener("click", (event) => {
      event.preventDefault();
      alert("watchlist here");
    });
  });
});
