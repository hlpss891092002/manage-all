import{sentFetchWithoutBody, sentFetchWithBody} from "../common/sent_fetch_get_response.js"
import{getAccountFromAutho, renderSideBlockList, signOutFunction, showSideBlockFromRouter} from "../common/initial.js"
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
let variety_dict ={}
let media_dict = {}
let stage_dict = { }

console.log(tableName)

async function initialPage(){
  let employee_id = await getAccountFromAutho()
   if(!employee_id){
    localStorage.clear()
    window.location.assign("/")
  }
  staffId = employee_id
  renderSideBlockList(staffId, addSubList, searchSubList, updateSubList, deleteSubList, inputContainer, tableName, router)
  signOutFunction(tableName)
  showSideBlockFromRouter(router)
 
  


  // // get variety list
  // const varietyResponse = await sentFetchWithoutBody("get",`/api/variety`)
  // const varietyResult = varietyResponse["data"]
  // console.log(varietyResult)
  // for (let variety of varietyResult){
  //   variety_dict[`${variety["variety_code"]}`] = variety["id"];
  // }
  // // console.log(variety_dict)
  // // get media list
  // const mediaResponse = await sentFetchWithoutBody("get",`/api/media`)
  // const mediaResult = mediaResponse["data"]
  // for (let media of mediaResult ){
  //   media_dict[`${media["name"]}`] = media["id"]
  // }
  // // console.log(media_dict)
  //   // get stage list
  // const stageResponse = await sentFetchWithoutBody("get",`/api/stage`)
  // const stageResult = stageResponse["data"]
  // for (let stage of stageResult){
  //   stage_dict[`${stage["name"]}`] = stage["id"]
  // }
  // // console.log(stage_dict)


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
  if (tableName === "produce_record"){
    body["id"] = createRandomId();
  };
  for (let data of allData){

    let value =  String(data.value);
    if( value === ""){
      value = null
    }
    const classList = data.classList;
    let inputTitle = classList[1].split("-")[0];
    body[`${inputTitle}`] = value ;
  };
  sent_input_db(body);
})

