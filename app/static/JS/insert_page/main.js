import{sentFetchWithoutBody, sentFetchWithBody} from "../common/sent_fetch_get_response.js"
const addSubList = document.querySelector("#add-sub-list")
const searchSubList = document.querySelector("#search-sub-list")
const inputContainer = document.querySelector(".input-container")
const submitBtn = document.querySelector(".submit-btn")
const query = window.location.search
const itemName = query.slice(1, query.length)
let staffId = ""
let variety_dict ={}
let media_dict = {}
let stage_dict = { }


async function initialPage(){
  // get auth
  const autho = await sentFetchWithoutBody("get","/api/staff/auth")
  const account = await autho["account"]
  console.log(account)
  staffId = await account

  if(!account){
    window.location.assign("/")
  }
  // get tables according auth
  const tables = await sentFetchWithoutBody("get","/api/staff/tables")
  for (let tableName of tables){
    const listItem = document.createElement("li")
    listItem.className = "list-group-item"
    const itemLink = document.createElement("a")
    itemLink.href = `/insert?${tableName}`
    itemLink.innerText= tableName
    listItem.appendChild(itemLink)
    addSubList.appendChild(listItem)
    
    const searchListItem = document.createElement("li")
    searchListItem.className = "list-group-item"
    const searchItemLink = document.createElement("a")
    searchItemLink.href = `/search?${tableName}`
    searchItemLink.innerText= tableName
    searchListItem.appendChild(searchItemLink)
    searchSubList.appendChild(searchListItem)

  }
  // get item according table
  const result = await sentFetchWithoutBody("get",`/api/tableAddItem/${itemName}`)
  const columns = result["data"]
  console.log(columns)
  // insert item block
  for (let column of columns){
    if (column === "id"){
      continue
    }
    const inputGroup = document.createElement("div")
    inputGroup.className = "input-group mb-3 "
    inputGroup.innerHTML = `<span class="input-group-text ${column}-input-disc">${column}</span>`
    let inputItem = document.createElement("input");
    inputItem.className = `form-control ${column}-input`
    inputGroup.appendChild(inputItem)
    inputContainer.appendChild(inputGroup)
    // select
    // inputGroup.innerHTML = `<label class="input-group-text " for="${column}">${column}</label>`
    // const inputSelect = document.createElement("select")
    // inputSelect.className ="form-select"
    // inputSelect.id = `${column}`
    // const optionSelect = document.createElement("option")
    // optionSelect.innerHTML = `<option selected>Choose...</option>`
    // inputSelect.appendChild(optionSelect)
    // inputGroup.appendChild(inputSelect)
    // inputContainer.appendChild(inputGroup)
  } 
  const producerInput = document.querySelector(".producer-input")
  producerInput.value = await account
  // get variety list
  const varietyResponse = await sentFetchWithoutBody("get",`/api/variety`)
  const varietyResult = varietyResponse["data"]
  console.log(varietyResult)
  for (let variety of varietyResult){
    variety_dict[`${variety["variety_code"]}`] = variety["id"];
  }
  console.log(variety_dict)
  // get media list
  const mediaResponse = await sentFetchWithoutBody("get",`/api/media`)
  const mediaResult = mediaResponse["data"]
  for (let media of mediaResult ){
    media_dict[`${media["media_name"]}`] = media["id"]
  }
  console.log(media_dict)
    // get stage list
  const stageResponse = await sentFetchWithoutBody("get",`/api/stage`)
  const stageResult = stageResponse["data"]
  for (let stage of stageResult){
    stage_dict[`${stage["stage_name"]}`] = stage["id"]
  }
  console.log(stage_dict)


}

async function sent_input_db(body){
  let result = await sentFetchWithBody("post", body, `/api/${itemName}`)
  console.log(result)
};

function createRandomId(){
  let now = new Date();
  let seconds = String(now.getSeconds());
  let minutes = String(now.getMinutes());
  let random = String(Math.floor(Math.random() * 100)).padStart(2,"0");
  let productionId = seconds + minutes + random + staffId;
  return productionId;
};

window.addEventListener("load", (e)=>{
  initialPage()
})

submitBtn.addEventListener("click", (e)=>{
  const allData = document.querySelectorAll(".form-control");

  let id  =  staffId ;
  let body = {};
  body["id"] = createRandomId();
  for (let data of allData){
    let value =  data.value;
    if( value === ""){
      value = null
    }
    if(media_dict[`${value}`]){
      value = media_dict[`${value}`]
    }
    if(stage_dict[`${value}`]){
      value = stage_dict[`${value}`]
    }
    if(variety_dict[`${value}`]){
      value = variety_dict[`${value}`]
    }
    const classList = data.classList;
    let inputTitle = classList[1].split("-")[0]+"_id";
    body[`${inputTitle}`] = value ;
  };
  console.log(body);
  sent_input_db(body);
})

