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
const tableTitleContainer = document.querySelector(".table-title-container")
const paginationContainer = document.querySelector(".pagination-container")
const showDataSection = document.querySelector(".show-data-section")
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
  const allData = document.querySelectorAll(".form-control");
  let body = {};
  body["page"] = nowPage
  let condition ={}
  body["condition"] = condition
  for (let data of allData){
    let value =  data.value;
    if( value === ""){
      continue
    }
    const classList = data.classList;
    let columnName = classList[1].split("-")[0]
    if ( columnName === "mother_produce" ){
      let inputTitle = columnName +"_id";
      condition[`${inputTitle}`] = value ;
    }else{
      condition[`${columnName}`] = value ;
    }
  }
  const result = await sent_input_search_and_render_table(body, tableName, PageAmount, paginationContainer, nowPage, search_and_render, tableTitleContainer, message, table, dataAmount, router);
  PageAmount = result["PageAmount"]
  nowPage = parseInt(result["startPage"])
  dataAmount = parseInt(result["dataAmount"])
  const updateBtn = document.querySelector(".update-btn")
  updateBtn.addEventListener("click",(e)=>{
    const updatableArray = document.querySelectorAll(".updatable")
    let body ={}
    for (let updatable of updatableArray){
      const updateIndexColumn = updatable.classList[2].split("-")[1]
      const updateIndexArray = updatable.classList[3].split("-").splice(2,updatable.classList[3].length)
      const updateIndexValue = updateIndexArray.join("-")  
      const updateColumn = updatable.classList[4].split("-")[1]
      const updateValueOrigin  = updatable.placeholder
      const updateValue = updatable.value
      if (updateValue !== updateValueOrigin){
        console.log(updateValue)
        console.log(updateValueOrigin)
        if(!body[updateIndexValue]){
          body[updateIndexValue] = {}
          body[updateIndexValue]["indexColumn"] = updateIndexColumn
          body[updateIndexValue][updateColumn] = updateValue 
        }else{
          body[updateIndexValue][updateColumn] = updateValue 
        }
      }
    }
    console.log(body)
    if(Object.keys(body).length === 0){
      e.preventDefault()
    }else{
      sent_input_update(body)
    }
    
  })
 
};


async function sent_input_update(body){
  let result = await sentFetchWithBody("put", body, `/api/${tableName}`)
  if(!result["ok"]){
    const errorMessage = result["message"]
    if( errorMessage.includes("variety is invalid") ){
      message.innerText = " Please check input value"
    }else{
      message.innerText = errorMessage
    }
    
  }else{
    message.innerText = "update success"
    clearMessageAndTable()
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




