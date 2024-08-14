import{sentFetchWithoutBody, sentFetchWithBody, sentFetchWithParams} from "../common/sent_fetch_get_response.js"
import {render_result_table, render_pagination, render_table_from_pagination, clearMessageAndTable} from "../common/render_table.js"
import{getAccountFromAutho, renderSideBlockList, signOutFunction, showSideBlockFromRouter} from "../common/initial.js"
import {sent_input_search_and_render_table } from "../common/search_and_render.js"
const addSubList = document.querySelector("#add-sub-list")
const searchSubList = document.querySelector("#search-sub-list")
const updateSubList = document.querySelector("#update-sub-list")
const deleteSubList = document.querySelector("#delete-sub-list")
const inputContainer = document.querySelector(".input-container")
const searchInputContainer = document.querySelector(".search-input-container")
const searchBtn = document.querySelector(".search-btn")
const deleteBtn = document.querySelector(".delete-btn")
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
let dataAmount = 0


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


async function search_and_render(nowPage){
const data = document.querySelector(".delete-index");
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
  const result = await sent_input_search_and_render_table(body, tableName, PageAmount, paginationContainer, nowPage, search_and_render, tableTitleContainer, table, dataAmount);
    PageAmount = result["PageAmount"]
    nowPage = parseInt(result["startPage"])
    dataAmount = parseInt(result["dataAmount"])
};



async function sent_input_delete(body){
  const result = await sentFetchWithBody("delete", body, `/api/${tableName}`)
  if(!result["ok"]){
    const errorMessage = result["message"]
    if( errorMessage.includes("variety is invalid") ){
      message.innerText = " Please check input value"
    }else if (errorMessage.includes("Cannot delete")){
      message.innerText = " This data were linked by order data. Please check the input value."
    }else{
      message.innerText = errorMessage
    }
    
  }else{
    message.innerText = "delete success"
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

deleteBtn.addEventListener("click", (e)=>{
  clearMessageAndTable()
  const deleteIndex = document.querySelector(".delete-index")
  const deleteIndexValue = deleteIndex.value
  const deleteIndexColumnName = (deleteIndex.classList[2].split("-")[1])
  
  let body = {}
  let deleteIndexDict ={}
  if (deleteIndexValue !== ""){
    deleteIndexDict[`${deleteIndexColumnName}`] = deleteIndexValue
    body["deleteIndex"] = deleteIndexDict
    sent_input_delete(body)
    deleteIndex.value = ""
  }else{
    alert("please input update index")
  }
})
