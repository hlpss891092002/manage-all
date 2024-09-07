import {signInStaff} from "../common/signin_function.js" 

const signInBtn = document.querySelector("#sign-in-btn")

signInBtn.addEventListener("click", (e)=>{
  signInStaff()
})

window.addEventListener("load", ()=>{
  if (localStorage["userState"]){
    window.location.assign("/staffIndex")
  }
})