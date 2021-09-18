document.addEventListener("DOMContentLoaded", () => {
  setInterval(show_clock, 1000);
  document.querySelectorAll(".watchlist").forEach((watch_button) => {
    watch_button.addEventListener("click", (event) => update_watchlist(event));
  });
  document
    .querySelectorAll(".remove_from_watchlist")
    .forEach((remove_button) => {
      remove_button.addEventListener("click", (event) => {
        let stockID = event.target.dataset.stock_id;
        let confirm = prompt(
          `Are you sure you want to remove this stock from your watchlist? This will permanently delete any notes you have saved. (y/n)`
        );
        if (confirm === "y") {
          update_watchlist(event);
          document.querySelector(
            `#watchedItem${stockID}`
          ).style.animationPlayState = "running";
          document.querySelector(`#stock_link${stockID}`).style.display =
            "none";
        } else if (confirm === "n") {
          alert("No problem, we'll keep it where it is!");
        } else {
          alert("Sorry, we didn't get it! Please try again.");
        }
      });
    });

  document.querySelectorAll(".edit_notes_button").forEach((edit_button) => {
    edit_button.addEventListener("click", (event) => update_notes(event));
  });
});

function format_time(time) {
  //takes in hours/second/minutes as 1- or 2-digit number and converts it to a 2-digit number
  return time < 10 ? "0" + time : time;
}

function get_time() {
  let week = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];

  let now = new Date();
  let day = week[now.getDay()];
  let hours = format_time(now.getHours());
  let minutes = format_time(now.getMinutes());

  return `${day}, ${hours}:${minutes}`;
}

function show_clock() {
  document.querySelector("#clock").innerHTML = get_time();
}

function update_notes(event) {
  event.preventDefault();
  let stockID = event.target.dataset.stock_id;
  let updated_notes = document.querySelector(`#editContent${stockID}`).value;
  fetch(`/saved_searches/${stockID}`, {
    method: "PUT",
    body: JSON.stringify({
      notes: updated_notes,
    }),
  }).then((response) => {
    if (response.ok) {
      document.querySelector("#message_notes").innerHTML =
        "Notes saved successfully";
    }
  });
}

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
          event.target.dataset.stock_id = result.id;
          event.target.innerHTML = `Remove ${stock} from watchlist`;

          // } else {
          //   document.querySelector("#message").innerHTML = result.error;
        }
      });
  } else {
    fetch(`/saved_searches/${stockID}`, {
      method: "DELETE",
    }).then((response) => {
      if (response.ok) {
        event.target.dataset.stock_id = "None";
        if (stock !== undefined) {
          event.target.innerHTML = `Add ${stock} to watchlist`;
        }
        //   } else {
        //     document.querySelector("#message").innerHTML = result.error;
      }
    });
  }
}
