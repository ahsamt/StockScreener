document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".watchlist").forEach((watch_button) => {
    watch_button.addEventListener("click", (event) => {
      event.preventDefault();
      let stock = event.target.dataset.stock_name;
      let stockID = event.target.dataset.stock_id;
      console.log(`Stock id is ${stockID}`);
      let user = document.querySelector("#username").innerHTML;

      function update_watchlist() {}

      // Check via internal API if this stock is in user's watchlist
      if (stockID === "None") {
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

              event.target.dataset.stock_id = result.id;
              event.target.innerHTML = `Remove ${stock} from watchlist`;
            } else {
              document.querySelector("#message").innerHTML = result.error;
            }
          });
      } else {
        fetch(`/saved_searches/${stockID}`, {
          method: "Delete",
        }).then((response) => {
          console.log(response);
          if (response.ok) {
            document.querySelector("#message").innerHTML =
              "Search deleted successfully";
            event.target.dataset.stock_id = "None";
            event.target.innerHTML = `Add ${stock} to the watchlist`;
          } else {
            document.querySelector("#message").innerHTML = result.error;
          }
        });
      }
    });
  });
});

function add_to_watchlist(stock) {}

function remove_from_watchlist(stockID) {}
