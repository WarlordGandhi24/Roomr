const chatbox = document.querySelector("#chatbox")

var count = initialCount
const urlParams = new URLSearchParams(window.location.search);
const otherId = urlParams.get('otherId');
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
function makeParaElement(element, index){
  newP = document.createElement('p')
  if(element[1] != currentUser){
    newP.classList.add("otherUser")
  }
  newP.innerHTML = element[0]
  chatbox.appendChild(newP)
/*  if(myJson.ids[i] != currentUser){
  newP.classList.add("otherUser")*/
}

function fetchUpdatedLog() {
	console.log(count)
	fetch('/ajax/get_updated_log?otherId='+otherId ).then(function(response) {
		return response.json()
	}).then(function(myJson) {
		// Update the div.
		console.log(myJson.msgCount)
		if (myJson.msgCount > count) {
      chatbox.innerHTML = ""
			myJson.msgs.forEach(makeParaElement)
			}
    count = myJson.msgCount
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
