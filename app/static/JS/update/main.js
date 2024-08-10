import{sentFetchWithoutBody, sentFetchWithBody} from "../common/sent_fetch_get_response.js"
import {render_result_table, render_pagination, render_table_from_pagination, clearMessageAndTable} from "../common/render_table.js"
import{getAccountFromAutho, renderSideBlockList, signOutFunction, showSideBlockFromRouter} from "../common/initial.js"
const addSubList = document.querySelector("#add-sub-list")
const searchSubList = document.querySelector("#search-sub-list")
const updateSubList = document.querySelector("#update-sub-list")
const deleteSubList = document.querySelector("#delete-sub-list")
const inputContainer = document.querySelector(".input-container")
const searchInputContainer = document.querySelector(".search-input-container")
const searchBtn = document.querySelector(".search-btn")
const updateBtn = document.querySelector(".update-btn")
const tableTitleContainer = document.querySelector(".table-title-container")
const paginationContainer = document.querySelector(".pagination-container")
const table = document.querySelector(".table")
const message = document.querySelector(".message")
const query = window.location.search
const tableName = query.slice(1, query.length)
const router = location.pathname.replace("/", "")
let staffId = ""
let nowPage= 0
let PageAmount = 0

async function initialPage(){
  let employee_id = await getAccountFromAutho()
  if(!employee_id){
    localStorage.clear()
    window.location.assign("/")
  }
  staffId = employee_id
  renderSideBlockList(staffId, addSubList, searchSubList,updateSubList, deleteSubList, inputContainer, tableName, router, searchInputContainer)
  signOutFunction()
  showSideBlockFromRouter(router)

 if(!employee_id){
    localStorage.clear()
    window.location.assign("/")
  }
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

// function clearMessageAndTable(){
//   message.innerText = ""
//   table.innerText = ""
//   tableTitleContainer.innerText = ""
//   paginationContainer.innerText = ""
// }

export function search_and_render(nowPage){
  const data = document.querySelector(".update-index");
  let body = {};
  body["page"] = nowPage
  let condition ={}
  body["condition"] = condition
  let value =  data.value;
    if (value === ""){
      condition = {}
    }else{
      const classList = data.classList;
      let columnName = classList[2].split("-")[1]
      condition[`${columnName}`] = value ;
    }
 sent_input_search_and_render_table(body);
 
};

async function sent_input_search_and_render_table(body){
  let result = await sentFetchWithBody("post", body, `/api/search/${tableName}`)
  console.log(result)
  let data = result["data"]
  nowPage = parseInt(result["startPage"])
  console.log(nowPage)
  if(data.length < 1){
    table.innerText = "no data"
  }else{
    PageAmount = result["PageAmount"]
    render_pagination(PageAmount, paginationContainer, nowPage)
    render_table_from_pagination(nowPage, PageAmount, search_and_render)
    render_result_table(data, tableName, tableTitleContainer, table, PageAmount)
  }
};

async function sent_input_update(body){
  let result = await sentFetchWithBody("put", body, `/api/update/${tableName}`)
  console.log(result)
  if(!result["ok"]){
    const errorMessage = result["message"]
    if( errorMessage.includes("variety is invalid") ){
      message.innerText = " Please check input value"
    }else{
      message.innerText = errorMessage
    }
    
  }else{
    message.innerText = "update success"
    search_and_render(nowPage)
  }
};


window.addEventListener("load", (e)=>{
  initialPage()
})

searchBtn.addEventListener("click", (e)=>{
  nowPage= 0
  clearMessageAndTable()
  search_and_render(nowPage)
})

updateBtn.addEventListener("click",((e)=>{
  clearMessageAndTable()
  const updateItemArray = document.querySelectorAll(".update-item")
  const updateIndex = document.querySelector(".update-index")
  const updateIndexColumnName = (updateIndex.classList[2].split("-")[1])
  const updateIndexValue = updateIndex.value
  let body = {}
  let updateItems = {}
  let updateIndexDict ={}
  updateIndexDict[`${updateIndexColumnName}`] = updateIndexValue
  if (updateIndexValue !== ""){
    for (let updateItem of updateItemArray){
    const updateItemValue = updateItem.value
      if(updateItemValue !== ""){
      const columnName = updateItem.classList[1].split("-")[0]
      updateItems[`${columnName}`] = updateItemValue
      if(updateIndexColumnName === columnName){
        updateIndex.value = updateItemValue
      }
      }else{
        continue
      }
    }
    console.log(Object.keys(updateItems).length)
    if(Object.keys(updateItems).length === 0){
      alert("please input update value")
    }else{
      body["updateIndex"] = updateIndexDict
      body["updateItems"] = updateItems
      const result = sent_input_update(body)
    }
    
  }else{
    alert("please input update index")
  }

  console.log(body)
  
}))
