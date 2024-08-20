import{sentFetchWithoutBody,sentFetchWithBody, sentFetchWithParams} from "../common/sent_fetch_get_response.js"
import {render_result_table, render_pagination, render_table_from_pagination, clearMessageAndTable} from "../common/render_table.js"
import{getAccountFromAutho, renderSideBlockList, signOutFunction, showSideBlockFromRouter} from "../common/initial.js"
import {sent_input_search_and_render_table } from "../common/search_and_render.js"
const addSubList = document.querySelector("#add-sub-list")
const searchSubList = document.querySelector("#search-sub-list")
const inputContainer = document.querySelector(".input-container")
const updateSubList = document.querySelector("#update-sub-list")
const deleteSubList = document.querySelector("#delete-sub-list")
const submitBtn = document.querySelector(".submit-btn")
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
  staffId = employee_id
  renderSideBlockList(staffId, addSubList, searchSubList, updateSubList, deleteSubList, inputContainer, tableName, router)
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
  };
 const result = await sent_input_search_and_render_table(body, tableName, PageAmount, paginationContainer, nowPage, search_and_render, tableTitleContainer, message, table, dataAmount, router);
 PageAmount = result["PageAmount"]
 nowPage = parseInt(result["startPage"])
 dataAmount = parseInt(result["dataAmount"])
}


window.addEventListener("load", (e)=>{
  initialPage()
})

submitBtn.addEventListener("click", (e)=>{
  nowPage= 0
  clearMessageAndTable()
  search_and_render(nowPage)
})

