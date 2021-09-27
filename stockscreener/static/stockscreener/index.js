document.addEventListener("DOMContentLoaded", () => {
  // get the clock working
  setInterval(show_clock, 1000);

  // check on scroll if "back to top" button should be displayed
  window.addEventListener("scroll", () => top_scroll());

  // update watchlist when the relevant button is clicked on the index page
  document.querySelectorAll(".watchlist").forEach((watch_button) => {
    watch_button.addEventListener("click", (event) => update_watchlist(event));
  });

  // remove stock from watchlist when the relevant button is clicked on the watchlist page
  document
    .querySelectorAll(".remove_from_watchlist")
    .forEach((remove_button) => {
      remove_button.addEventListener("click", (event) => {
        remove_from_watchlist(event);
      });
    });

  // save notes when the relevant button is clicked on the watchlist page
  document.querySelectorAll(".save_notes_button").forEach((save_button) => {
    save_button.addEventListener("click", (event) => update_notes(event));
  });

  // display the relevant stocks when a letter button is clicked on the ticker list page
  document.querySelectorAll(".abc").forEach((letter) => {
    letter.addEventListener("click", (event) => {
      display_stock_list(event);
    });
  });
});

function top_scroll() {
  // insert "back to top" button when user scrolls down the page
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("topButton").style.display = "block";
  } else {
    document.getElementById("topButton").style.display = "none";
  }
}

function format_time(time) {
  // formats hours/second/minutes as a 2-digit number
  return time < 10 ? "0" + time : time;
}

function get_time() {
  // get user's current time to start the clock
  let now = new Date();
  let hours = format_time(now.getHours());
  let minutes = format_time(now.getMinutes());
  return `${hours}:${minutes}`;
}

function show_clock() {
  document.querySelector("#clock").innerHTML = get_time();
}

function update_notes(event) {
  // use internal API to update user's notes for specific stock
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
      let time = document.querySelector("#clock").innerHTML;
      document.querySelector(
        `#messageNotes${stockID}`
      ).innerHTML = `Notes saved at ${time}`;
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

function remove_from_watchlist(event) {
  let stockID = event.target.dataset.stock_id;
  let confirm = prompt(
    `Are you sure you want to remove this stock from your watchlist? This will permanently delete any notes you have saved. (y/n)`
  );
  if (confirm === "y") {
    update_watchlist(event);
    document.querySelector(`#watchedItem${stockID}`).style.animationPlayState =
      "running";
    document.querySelector(`#stock_link${stockID}`).style.display = "none";
  } else if (confirm === "n") {
    alert("No problem, we'll keep it where it is!");
  } else {
    alert("Sorry, we didn't get it! Please try again.");
  }
}

function display_stock_list(event) {
  event.preventDefault();
  document.querySelectorAll(".abc_tickers").forEach((section) => {
    section.style.display = "none";
  });
  document.querySelector(`#${letter.dataset.letter}`).style.display = "block";
}
