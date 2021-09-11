document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".watchlist").forEach((watch_button) => {
    watch_button.addEventListener("click", (event) => {
      event.preventDefault();
      let stock = event.target.dataset.stockname;
      if (event.target.id === `Add${stock}`) {
        console.log("adding to watchlist");
        add_to_watchlist(stock);
        event.target.innerHTML = `Remove ${stock} from watchlist`;
      } else {
        remove_from_watchlist(stock);
        event.target.innerHTML = `Add ${stock} to watchlist`;
      }
    });
  });
});

function add_to_watchlist(stock) {
  fetch("/saved_searches", {
    method: "POST",
    body: JSON.stringify({
      stock: stock,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      console.log(result);
      if (result.message === "Search saved successfully") {
        document.querySelector("#message").innerHTML =
          "Search saved successfully";
      } else {
        document.querySelector("#message").innerHTML = result.error;
      }
    });
}

function remove_from_watchlist(stock) {
  fetch(`/saved_searches/${search}`, {
    method: "Delete",
  }).then((response) => {
    console.log(response);
  });
}
