import{sentFetchWithoutBody, sentFetchWithBody} from "../common/sent_fetch_get_response.js"
import{getAccountFromAutho, renderSideBlockList, signOutFunction, showSideBlockFromRouter} from "../common/initial.js"
const addSubList = document.querySelector("#add-sub-list")
const searchSubList = document.querySelector("#search-sub-list")
const inputContainer = document.querySelector(".input-container")
const updateSubList = document.querySelector("#update-sub-list")
const deleteSubList = document.querySelector("#delete-sub-list")
const submitBtn = document.querySelector(".submit-btn")
const tableTitleContainer = document.querySelector(".table-title-container")
const table = document.querySelector(".table")
const query = window.location.search
const tableName = query.slice(1, query.length)
const router = location.pathname.replace("/", "")
let staffId = ""
let variety_dict ={}
let media_dict = {}
let stage_dict = { }


async function initialPage(){
  let account = await getAccountFromAutho()
  staffId = account
  renderSideBlockList(staffId, addSubList, searchSubList, updateSubList, deleteSubList, inputContainer, tableName, router)
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
  table.innerText = ""
  tableTitleContainer.innerText = ""
}

async function sent_input_search_and_render_table(body,){
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
  search_result.forEach((element)=>{
    console.log(element)
    const columnValues = Object.values(element)
    const row = document.createElement("div")
    row.className = "table-row"
    columnValues.forEach((element)=>{
        let rowValue = document.createElement("div")
        rowValue.className ="row-value"
        rowValue.innerText = element 
        row.appendChild(rowValue)  
      })
    rowContainer.appendChild(row)
    })
  table.appendChild(rowContainer)

}

window.addEventListener("load", (e)=>{
  initialPage()
})

submitBtn.addEventListener("click", (e)=>{
  clearMessageAndTable()
  const allData = document.querySelectorAll(".form-control");
  let body = {};
  for (let data of allData){
    let value =  data.value;
    if( value === ""){
      continue
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
    let columnName = classList[1].split("-")[0]
    if ( columnName === "mother_produce" ){
      let inputTitle = columnName +"_id";
      body[`${inputTitle}`] = value ;
    }else{
      body[`${columnName}`] = value ;
    }

  };
 sent_input_search_and_render_table(body);
})

