import{sentFetchWithoutBody, sentFetchWithBody} from "../common/sent_fetch_get_response.js"
import{getAccountFromAutho, renderSideBlockList, signOutFunction, showSideBlockFromRouter, renderStaffInNav} from "../common/initial.js"
const addSubList = document.querySelector("#add-sub-list")
const searchSubList = document.querySelector("#search-sub-list")
const updateSubList = document.querySelector("#update-sub-list")
const deleteSubList = document.querySelector("#delete-sub-list")
const inputContainer = document.querySelector(".input-container")
const submitBtn = document.querySelector(".submit-btn")
const responseMessage = document.querySelector(".response-message")

const query = window.location.search
const tableName = query.slice(1, query.length)
const router = location.pathname.replace("/", "")
let staffId = ""
let staffPosition = ""
let variety_dict ={}
let media_dict = {}
let stage_dict = { }

console.log(tableName)

async function initialPage(){
  let staffData = await getAccountFromAutho()
  if(!staffData){
    localStorage.clear()
    window.location.assign("/")
  }
  if(!tableName){
    window.location.assign(`/${router}?category`)
  }
  staffId = staffData["employee_id"]
  staffPosition = staffData["job_position"]

  renderSideBlockList(staffId, addSubList, searchSubList, updateSubList, deleteSubList, inputContainer, tableName, router)
  signOutFunction(tableName)
  renderStaffInNav(staffData)
}

async function sent_input_db(body){
  const  result = await sentFetchWithBody("post", body, `/api/${tableName}`)
  if (result["ok"]){
    responseMessage.innerText = "add success"
  }else{
    const message = result["message"].replaceAll("'", "")
    console.log(message)
    const  messageArray = message.split(" ")
    if (message.includes("Duplicate entry")){
      const key = messageArray[messageArray.indexOf("key")+1].split(".")[1]
      console.log(key)
      const value = body[`${key}`]
      console.log()
      responseMessage.innerText = `${key} : "${value}"  already exist`
    }else if(message.includes("cannot be null")){
      const column = messageArray[messageArray.indexOf("Column")+1].split("_")[0]
      let item = ""
      let value = ""
      console.log(column)
      if(column === "variety"){
        item = column + "_code"
        value = body[`${item}`]
      }else{
        item = column
        value = body[`${item}`]
      }
      responseMessage.innerText = `${item} : "${value}"  is not  exist`
    }else{
      responseMessage.innerText = message
    }
  }

};

function createRandomId(){
  let now = new Date();
  let seconds = String(now.getSeconds());
  let minutes = String(now.getMinutes());
  let random = String(Math.floor(Math.random() * 10000)).padStart(2,"0");
  let productionId = seconds + minutes + random ;
  return productionId;
};

window.addEventListener("load", (e)=>{
  initialPage()
})

submitBtn.addEventListener("click", (e)=>{
  
  const allData = document.querySelectorAll(".form-control");
  responseMessage.innerText =""
  let body = {};
  console.log(allData.length)
  if (tableName === "produce_record"){
    body["id"] = createRandomId();
  };
  for (let data of allData){
    const classList = data.classList;
    let inputTitle = classList[1].split("-")[0];
    let value =  String(data.value);
    if( (inputTitle === "mother_produce_id" | inputTitle === "consumed_reason" ) && value === ""){
      value = null
      submitBtn.disabled = true
    }else if( value === ""){
      alert(`${inputTitle} can't be null`)
      return
    }
    body[`${inputTitle}`] = value ;
  };
  let result = sent_input_db(body)

  if (result){
    submitBtn.disabled = false
  }
})

