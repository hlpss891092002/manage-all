import{sentFetchWithoutBody} from "../common/sent_fetch_get_response.js"
import{getAccountFromAutho, renderSideBlockList, signOutFunction, showSideBlockFromRouter} from "../common/initial.js"
const addSubList = document.querySelector("#add-sub-list")
const searchSubList = document.querySelector("#search-sub-list")
const updateSubList = document.querySelector("#update-sub-list")
const deleteSubList = document.querySelector("#delete-sub-list")
const inputContainer = document.querySelector(".input-container")
const searchInputContainer = document.querySelector(".search-input-container")
const categoryAmountInStock= document.querySelector(".category-amount-in-stock")
const largestAmountStock = document.querySelector(".largest-amount-stock")
const categoryAddYesterday = document.querySelector(".category-add-yesterday")
const categoryConsumeYesterday = document.querySelector(".category-consume-yesterday")
const table = document.querySelector(".table")
const query = window.location.search
const tableName = query.slice(1, query.length)
const router = location.pathname.replace("/", "")
let staffId = ""

function renderMainBlock(block, dataList){

  for (let data of dataList){
    let entire = Object.entries(data)
    const blockItem = document.createElement("div")
    if (entire.length ===  3){
      const name = entire[0][1]
      const stage = entire[1][1]
      const count = entire[2][1]
      blockItem.className = "block-item"
      blockItem.innerText = `${name}-${stage} : ${count}`
    }else{
      const name = entire[0][1]
      const count = entire[1][1]
      blockItem.className = "block-item"
      blockItem.innerText = `${name} : ${count}`
    }
    block.appendChild(blockItem)
  }
}

async function initialPage(){
  let employee_id = await getAccountFromAutho()
  staffId = employee_id
  renderSideBlockList(staffId, addSubList, searchSubList,updateSubList, deleteSubList, inputContainer, tableName, router, searchInputContainer)
  signOutFunction()
  
  if(!employee_id){
    localStorage.clear()
    window.location.assign("/")
  }

}
async function getNewestData() {
  let latestData = await sentFetchWithoutBody("get", "/api/latest")
  let {yesterdayProduceMost, categoryYesterdayConsume, categoryStock, readyShippingStock} = await latestData
  // renderMainBlock(categoryAmountInStock, category_stock)
  // renderMainBlock(largestAmountStock, largest_amount)
  // renderMainBlock(categoryAddYesterday, yesterday_produce)
  // renderMainBlock(categoryConsumeYesterday, yesterday_consume)
  console.log(latestData)
}



window.addEventListener("load", (e)=>{
  initialPage()
  getNewestData()
})


