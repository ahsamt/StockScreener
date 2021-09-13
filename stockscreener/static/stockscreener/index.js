document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".watchlist").forEach((watch_button) => {
    watch_button.addEventListener("click", (event) => update_watchlist(event));
  });
});

function update_watchlist(event) {
  event.preventDefault();
  let stock = event.target.dataset.stock_name;
  let stockID = event.target.dataset.stock_id;
  let user = document.querySelector("#username").innerHTML;

  // Check via internal API if this stock is in user's watchlist
  if (stockID === "None") {
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
          event.target.dataset.stock_id = result.id;
          event.target.innerHTML = `Remove ${stock} from watchlist`;
          // } else {
          //   document.querySelector("#message").innerHTML = result.error;
        }
      });
  } else {
    fetch(`/saved_searches/${stockID}`, {
      method: "Delete",
    }).then((response) => {
      if (response.ok) {
        document.querySelector("#message").innerHTML =
          "Search deleted successfully";
        event.target.dataset.stock_id = "None";
        event.target.innerHTML = `Add ${stock} to watchlist`;
        //   } else {
        //     document.querySelector("#message").innerHTML = result.error;
      }
    });
  }
}
