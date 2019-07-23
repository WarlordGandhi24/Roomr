let ball = document.querySelector("#ball")
let triangle = document.querySelector("#triangle")
let positive = ["Okay Sure", "Ye", "For sure", "Nah. <br> sike! haha! yeah bro, positivity!"]
let neutral = ["maybe", "I'm busy.", "eh.", "hm."]
let negative = ["No", "False, cretin.", "Nice try buddy, but no dice", "Imagine being as wrong as you are"]
let responseType = [positive, neutral, negative]
let colors = ["green", "goldenrod", "red"]

let pfp = document.querySelector("pfp")

ball.addEventListener('click', ()=>{
  let paragraph = document.querySelector("#answer")
  listNum = Math.floor(Math.random() * 3)
  chosenList = responseType[listNum]
  paragraph.innerHTML = chosenList[Math.floor(Math.random() * chosenList.length)]
  triangle.setAttribute("style", "border-top: 120px solid " + colors[listNum] )
})
