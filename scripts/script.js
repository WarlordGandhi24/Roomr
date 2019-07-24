const submit = document.querySelector("#pref")
const pfp = document.querySelector("#pfp")

submit.addEventListener('click', ()=>{
  pfp_url = prompt("Enter URL:", "https://www.");
  pfp.src = pfp_url;
  pfp.width = "350";
  pfp.height = "350";

  
})
