const chatbox = document.querySelector("#chatbox")
chatbox.addEventListener('keypress', function (key){
  if(key.keycode == 13){
    key.preventDefault()
    document.querySelector("#send").click()
  }
})

function startTimer() {
  const microseconds = 2000  // 2 seconds
  window.setTimeout(fetchUpdatedLog, microseconds)
}

// Ask the server for the current note immediately.
function fetchUpdatedLog() {
  fetch('/ajax/get_updated_log')
    .then(function(response) {
      return response.json()
    })
    .then(function (myJson) {
      // Update the div.
      var newP = document.createElement("p")
      var newMsg = document.createTextNode(myJson.logs);
      newP.appendChild(newMsg)
      chatbox.appendChild(newP)

      // Start the timer again for the next request.
      startTimer()
    })
}

if (chatbox != null) {
  // If note_div is null it means that the user is not logged in.  This is
  // because the jinja template for the '/' handler only renders this div
  // when the user is logged in.  Querying for a node that does not exist
  // returns null.

  // Start by fetching the current note without any delay.
  fetchUpdatedLog()
}
