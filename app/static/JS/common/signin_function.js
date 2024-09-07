import{sentFetchWithBody} from "./sent_fetch_get_response.js"


export async function signInStaff() {
  // try{
    const responseMessage = document.querySelector(".response-message")
    const employee_id = document.querySelector("#staff-id").value
    const password = document.querySelector("#staff-password").value
    console.log(employee_id + password)
    switch (true){
      case !employee_id :
        responseMessage.innerText = "Please input staff ID. "
        return
      case !password:
        responseMessage.innerText = "Please input password."
        return
      case employee_id !== null &&  password !== null:
        responseMessage.innerText = ""
        const body = {
          "employee_id": `${employee_id}`,
          "password": `${password}`
        }
        console.log(body)
        const response = await sentFetchWithBody("put", body, "/api/staff/auth")
        const responseJSON = await response
        if (responseJSON["token"]){     
          localStorage.setItem("userState", `${responseJSON["token"]}`)
          responseMessage.innerText = "Sign in success!"
          window,location.assign("/staffIndex")
        }else{
          responseMessage.classList.remove("success")
          responseMessage.innerText = responseJSON["message"]
        }
    }
  // }catch{
  //   console.log("loading signin popup page fail")
  // }
  
};

