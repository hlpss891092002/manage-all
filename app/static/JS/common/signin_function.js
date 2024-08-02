import{sentFetchWithBody} from "./sent_fetch_get_response.js"


export async function signInStaff() {
  // try{
    const responseMessage = document.querySelector(".response-message")
    const account = document.querySelector("#staff-id").value
    const password = document.querySelector("#staff-password").value
    console.log(account + password)
    switch (true){
      case !account ||  !password:
        responseMessage.innerText = "請輸入帳號密碼"
        return
      case account !== null &&  password !== null:
        responseMessage.innerText = ""
        const body = {
          "account": `${account}`,
          "password": `${password}`
        }
        console.log(body)
        const response = await sentFetchWithBody("put", body, "/api/staff/auth")
        const responseJSON = await response
        if (responseJSON["token"]){     
          localStorage.setItem("userState", `${responseJSON["token"]}`)
          responseMessage.innerText = "登入成功"
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

