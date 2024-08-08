import{sentFetchWithoutBody, sentFetchWithBody} from "../common/sent_fetch_get_response.js"
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
  const data = document.querySelector(".update-index");
  let body = {};
  let value =  data.value;
    console.log(value)
    if (value === ""){
      body = {}
    }else{
      const classList = data.classList;
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
    search_and_render()
  }
};

async function render_result_table(search_result) {
  const resultKeys = Object.keys(search_result)
  const resultCount = resultKeys.length
  const tableTitle = document.createElement("div")
  const DataCount = document.createElement("div")
  tableTitleContainer.appendChild(tableTitle)
  tableTitleContainer.appendChild(DataCount)
  tableTitle.innerText = `Table ${tableName}`
  DataCount.innerText = ` Amount of row ${resultCount}`
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
    columnName .innerText = element
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
  table.appendChild(rowContainer)

};

window.addEventListener("load", (e)=>{
  initialPage()
})

searchBtn.addEventListener("click", (e)=>{
  clearMessageAndTable()
  search_and_render()
})

updateBtn.addEventListener("click",((e)=>{
  clearMessageAndTable()
  const updateItemArray = document.querySelectorAll(".update-item")
  console.log(updateItemArray)
  const updateIndex = document.querySelector(".update-index")
  const updateIndexColumnName = (updateIndex.classList[2].split("-")[1])
  const updateIndexValue = updateIndex.value
  console.log(updateIndexValue)
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
