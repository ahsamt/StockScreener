document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".watchlist").forEach((watch_button) => {
    watch_button.addEventListener("click", (event) => {
      event.preventDefault();
      alert("watchlist here");
      let stock = document.querySelector("#stock_name").innerHTML;
      alert(stock);
      fetch("/saved_searches", {
        method: "POST",
        body: JSON.stringify({
          stock: stock,
        }),
      })
        .then((response) => response.json())
        .then((result) => {
          if (result.message === "Search saved successfully") {
            document.querySelector("#message").innerHTML =
              "Search saved successfully";
          } else {
            document.querySelector("#message").innerHTML = result.error;
          }
        });
    });
  });
});
