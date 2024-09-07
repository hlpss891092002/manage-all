import{sentFetchWithoutBody, sentFetchWithBody} from "../common/sent_fetch_get_response.js"
import{getAccountFromAutho, renderSideBlockList, signOutFunction, showSideBlockFromRouter, renderStaffInNav} from "../common/initial.js"
import { formateAddResponse } from "../common/formate_response_message.js"
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

  renderSideBlockList(staffId,  staffPosition, inputContainer, tableName, router)
  signOutFunction(tableName)
  renderStaffInNav(staffData)
}

async function sent_input_db(body){
  const keys = Object.keys(body)
  const firstColumnValue = body[keys[0]]
  const  result = await sentFetchWithBody("post", body, `/api/${tableName}`)
  if(result){
    responseMessage.innerText=""
  }

  formateAddResponse(result, responseMessage, tableName, firstColumnValue)

};

function createRandomId(){
  let now = new Date();
  let seconds = String(now.getSeconds());
  let minutes = String(now.getMinutes());
  let milliseconds = String(now.getMilliseconds());
  let random = String(Math.floor(Math.random() * 100000000)).padStart(8,"0");
  const uuid = String(crypto.randomUUID());
  let productionId = seconds + minutes + milliseconds + random +  uuid;
 
  return productionId;
};

window.addEventListener("load", (e)=>{
  initialPage()
})

submitBtn.addEventListener("click", (e)=>{
  const spinnerBorder = document.createElement("div")
  spinnerBorder.className = "spinner-border"
  spinnerBorder.setAttribute("role", "status")
  const spinner = document.createElement("span")
  spinner.className = "sr-only"
  spinnerBorder.appendChild(spinner)
  
  const allData = document.querySelectorAll(".form-control");
  responseMessage.innerText =""
  let body = {};
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
      responseMessage.appendChild(spinnerBorder)
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

