import{sentFetchWithoutBody, sentFetchWithBody, sentFetchWithParams} from "../common/sent_fetch_get_response.js"
import {render_result_table, render_pagination, render_table_from_pagination, clearMessageAndTable} from "../common/render_table.js"
import{getAccountFromAutho, renderSideBlockList, signOutFunction, showSideBlockFromRouter, renderStaffInNav} from "../common/initial.js"
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
let staffPosition = ""
let nowPage= 0
let PageAmount = 0
let dataAmount = 0

async function initialPage(){
  let staffData = await getAccountFromAutho()
  if(!staffData){
    localStorage.clear()
    window.location.assign("/")
  }
  staffId = staffData["employee_id"]
  staffPosition = staffData["job_position"]
  
  renderSideBlockList(staffId, addSubList, searchSubList,updateSubList, deleteSubList, inputContainer, tableName, router, searchInputContainer)
  signOutFunction()
  
  renderStaffInNav(staffData)
  
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
  const result = await sent_input_search_and_render_table(body, tableName, PageAmount, paginationContainer, nowPage, search_and_render, tableTitleContainer, message, table, dataAmount, router, staffPosition, searchBtn);
  PageAmount = result["PageAmount"]
  nowPage = parseInt(result["startPage"])
  dataAmount = parseInt(result["dataAmount"])
  const updateBtn = document.querySelector(".update-btn")
  updateBtn.addEventListener("click",(e)=>{
    const updatableArray = document.querySelectorAll(".updatable")
    updateBtn.disabled = true;
    let body ={}
    for (let updatable of updatableArray){
      const updatableClassList = updatable.classList
      const updateIndexColumn = updatableClassList[1].split("-")[1] 
      const updateColumn = updatableClassList[2].split("-")[1]
      const updateValueOrigin  = updatable.placeholder
      const updateValue = updatable.value
      let updateIndexValue = []
      if(updatableClassList.length > 5){
        let updateIndexArray = Array.apply(null, updatableClassList).slice(4, updatableArray.length)
        updateIndexArray[0] = updateIndexArray[0].split("-")[2]
        updateIndexValue = updateIndexArray.join(" ")
        console.log(updateIndexValue)
      }else{
        const updateIndexArray = updatableClassList[3].split("-").splice(2,updatableClassList[3].length)
        updateIndexValue = updateIndexArray.join("-") 
      }
      if(updateValue === "" && updateValueOrigin === "null"){
        console.log("empty")
        continue
      }else  if (updateValue !== updateValueOrigin){
        console.log(updateValue === null)
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
  searchBtn.disabled = true;
})




