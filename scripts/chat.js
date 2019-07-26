const chatbox = document.querySelector("#chatbox")
const inputBox = document.querySelector("#inputBox")
const form = document.querySelector("#chat")
var count = initialCount
const urlParams = new URLSearchParams(window.location.search);
const otherId = urlParams.get('otherId');

form.addEventListener('submit', function (){
    console.log("TEST")

})

function startTimer() {
  const microseconds = 800  // 2 seconds
  window.setTimeout(fetchUpdatedLog, microseconds)
}


// Ask the server for the current note immediately.
function makeParaElement(element, index){
  newP = document.createElement('p')
  user = document.createElement('p')
  if(element[1] != currentUser){
    user.classList.add("otherUser")
    user.classList.add("msgTag")
    user.innerHTML = element[2]
    newP.classList.add("otherUser")
  }else{
    user.classList.add("msgTag")
    user.innerHTML = "me"
  }

  newP.innerHTML = element[0]
  chatbox.appendChild(user)
  chatbox.appendChild(newP)

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
    inputBox.value = ""
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
