document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".watchlist").forEach((watch_button) => {
    watch_button.addEventListener("click", (event) => {
      event.preventDefault();
      let stock = event.target.dataset.stockname;
      let stockID = event.target.dataset.stockID;

      let user = document.querySelector("#username").innerHTML;

      function update_watchlist() {}

      // Check via internal API if this stock is in user's watchlist
      if (!stockID) {
        console.log("adding to watchlist");
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
              event.target.dataset.stockID = result.id;
            } else {
              document.querySelector("#message").innerHTML = result.error;
            }
          });
        event.target.innerHTML = `Remove ${stock} from watchlist`;
      } else {
        remove_from_watchlist(stock);
        event.target.innerHTML = `Add ${stock} to watchlist`;
      }
    });
  });
});

function add_to_watchlist(stock) {}

function remove_from_watchlist(stock) {
  fetch(`/saved_searches/${stockID}`, {
    method: "Delete",
  }).then((response) => {
    console.log(response);
  });
}
