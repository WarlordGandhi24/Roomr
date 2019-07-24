const chatbox = document.querySelector("#chatbox")

var count = initialCount

chatbox.addEventListener('keypress', function (key){
  if(key.keycode == 13){
    key.preventDefault()
    document.querySelector("#send").click()
    document.querySelector("#inputBox").innerHTML = ""
  }
})

function startTimer() {
  const microseconds = 2000  // 2 seconds
  window.setTimeout(fetchUpdatedLog, microseconds)
}


// Ask the server for the current note immediately.

function fetchUpdatedLog() {
  console.log(count)

  fetch('/ajax/get_updated_log')
    .then(function(response) {

      return response.json()
    })
    .then(function (myJson) {

      // Update the div.
      console.log(myJson.msgCount)

      if(myJson.msgCount > count){
      for(i = myJson.msgCount - count; i < myJson.msgCount; i++){
      newP = document.createElement('p')
      newP.innerHTML = myJson.msgs[i]
      chatbox.appendChild(newP)
      //  initialCount = myJson.msgCount
      // Start the timer again for the next request.
      count = myJson.msgCount
    }

    }
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
