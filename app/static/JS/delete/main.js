import{sentFetchWithoutBody, sentFetchWithBody} from "../common/sent_fetch_get_response.js"
import{getAccountFromAutho, renderSideBlockList, signOutFunction, showSideBlockFromRouter} from "../common/initial.js"
const addSubList = document.querySelector("#add-sub-list")
const searchSubList = document.querySelector("#search-sub-list")
const updateSubList = document.querySelector("#update-sub-list")
const deleteSubList = document.querySelector("#delete-sub-list")
const inputContainer = document.querySelector(".input-container")
const searchInputContainer = document.querySelector(".search-input-container")
const searchBtn = document.querySelector(".search-btn")
const deleteBtn = document.querySelector(".delete-btn")
const tableTitleContainer = document.querySelector(".table-title-container")
const table = document.querySelector(".table")
const message = document.querySelector(".message")

const query = window.location.search
const tableName = query.slice(1, query.length)
const router = location.pathname.replace("/", "")
let staffId = ""

async function initialPage(){
  let account = await getAccountFromAutho()
  staffId = account
  renderSideBlockList(staffId, addSubList, searchSubList,updateSubList, deleteSubList, inputContainer, tableName, router, searchInputContainer)
  signOutFunction()
  showSideBlockFromRouter(router)

    if(!account){
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

function clearMessageAndTable(){
  message.innerText = ""
  table.innerText = ""
  tableTitleContainer.innerText = ""
}

function search_and_render(){
  const deleteIndex = document.querySelector(".delete-index");
  let body = {};
  let value =  deleteIndex.value;
    console.log(value)
    if (value === ""){
      body = {}
    }else{
      const classList = deleteIndex.classList;
      console.log(classList)
      let columnName = classList[2].split("-")[1]
      console.log(columnName)
      body[`${columnName}`] = value ;
      console.log(columnName)
      console.log(body)
    }
 sent_input_search_and_render_table(body);
};

async function sent_input_search_and_render_table(body){
  let result = await sentFetchWithBody("post", body, `/api/search/${tableName}`)
  console.log(result)
  if(!result["data"]){
    table.innerText = "no data"
  }else{
    render_result_table(result["data"])
  }
};

async function render_result_table(search_result) {
  const resultKeys = Object.keys(search_result)
  const resultCount = resultKeys.length
  const tableTitle = document.createElement("div")
  const DataCount = document.createElement("div")
  tableTitleContainer.appendChild(tableTitle)
  tableTitleContainer.appendChild(DataCount)
  table.textContent = ""
  let columnNameArray  =  Object.keys(search_result[0])
  const columnNameContainer = document.createElement("div")
  const rowContainer = document.createElement("div")
  columnNameContainer.className = "column-name-container"
  rowContainer.className= "row-container"
  //append column title
  columnNameArray.forEach((element)=>{
    let columnName =  document.createElement("div")
    columnName.className = "column-name"
    columnName.innerText = element
    columnNameContainer.appendChild(columnName)
  })
  table.appendChild(columnNameContainer)
  //append row value
  search_result.forEach((elementName)=>{
    const columnValues = Object.values(elementName)
    const row = document.createElement("div")
    row.className = `table-row `
    columnValues.forEach((element)=>{
        let rowValue = document.createElement("div")
        rowValue.className = `row-value ${elementName}`
        rowValue.setAttribute("contenteditable", "true")
        rowValue.innerText = element 
        row.appendChild(rowValue)  
      })
    rowContainer.appendChild(row)
    })
  tableTitle.innerText = `Table ${tableName}`
  DataCount.innerText = ` Amount of row ${resultCount}`
  table.appendChild(rowContainer)

};

async function sent_input_delete(body){
  const result = await sentFetchWithBody("delete", body, `/api/delete/${tableName}`)
  console.log(result)
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
    search_and_render()
  }
};

window.addEventListener("load", (e)=>{
  initialPage()
})

searchBtn.addEventListener("click", (e)=>{
  clearMessageAndTable()
  search_and_render()
})

deleteBtn.addEventListener("click", (e)=>{
  clearMessageAndTable()
  const deleteIndex = document.querySelector(".delete-index")
  const deleteIndexValue = deleteIndex.value
  const deleteIndexColumnName = (deleteIndex.classList[2].split("-")[1])
  
  let body = {}
  let deleteIndexDict ={}
  console.log(deleteIndexValue)
  if (deleteIndexValue !== ""){
    deleteIndexDict[`${deleteIndexColumnName}`] = deleteIndexValue
    body["deleteIndex"] = deleteIndexDict
    sent_input_delete(body)
    deleteIndex.value = ""
  }else{
    alert("please input update index")
  }
})
