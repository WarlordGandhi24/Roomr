const submit = document.querySelector("#pref")
const pfp = document.querySelector("#pfp")

function postData(url = '/ajax/update_pfp', data = {}) {
  // Default options are marked with *
    return fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, cors, *same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            // 'Content-Type': 'application/json',
             'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrer: 'no-referrer', // no-referrer, *client
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    })
    .then(response => response.json()); // parses JSON response into native JavaScript objects
}

submit.addEventListener('click', ()=>{
  pfp_url = prompt("Enter URL:", "https://www.");
  pfp.src = pfp_url;
  pfp.width = "350";
  pfp.height = "350";

  console.log(pfp_url)

  postData('/ajax/update_pfp', {answer: pfp_url})
  .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
  .catch(error => console.error(error));
})
