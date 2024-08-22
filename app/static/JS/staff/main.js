import{sentFetchWithoutBody} from "../common/sent_fetch_get_response.js"
import{getAccountFromAutho, renderSideBlockList, signOutFunction, showSideBlockFromRouter} from "../common/initial.js"
const addSubList = document.querySelector("#add-sub-list")
const searchSubList = document.querySelector("#search-sub-list")
const updateSubList = document.querySelector("#update-sub-list")
const deleteSubList = document.querySelector("#delete-sub-list")
const inputContainer = document.querySelector(".input-container")
const searchInputContainer = document.querySelector(".search-input-container")
const categoryStockContainer= document.querySelector(".category-stock")
const readyShippingStockContainer = document.querySelector(".ready-shipping-stock")
const yesterdayProduceMostContainer = document.querySelector(".yesterday-produce-most")
const categoryYesterdayConsumeContainer = document.querySelector(".category-yesterday-consume")
const table = document.querySelector(".table")
const query = window.location.search
const tableName = query.slice(1, query.length)
const router = location.pathname.replace("/", "")
let staffId = ""

function renderMainBlock(block, dataList){
  const itemContainer = document.createElement("div") 
  itemContainer.className = "item-container"
  const titleRow = document.createElement("div")
  titleRow.className = "title-row"
  block.appendChild(titleRow)
  for (let data of dataList){
    if (dataList.indexOf(data) === 0){
      let keys = Object.keys(data)
      for (let key of keys){
        key === "count" ? key = "amount" : key = key
        const titleItem = document.createElement("div")
        titleItem.className = "title-item"
        titleItem.innerText= `${key}`
        titleRow.appendChild(titleItem)
      }
    }
    let entire = Object.entries(data)
    const itemRow = document.createElement("div")
    itemRow.className = "item-row"
    // if (entire.length ===  3){
      console.log(entire)
      for (let item of entire){
        let value = item[1]
        let rowItem = document.createElement("div")
        rowItem.className = "row-item"
        rowItem.innerText = value
        itemRow.append(rowItem)
      }
    // }else{
    //   const name = entire[0][1]
    //   const count = entire[1][1]
    //   itemRow.className = "item-row"
    //   itemRow.innerText = `${name} : ${count}`
    // }
    itemContainer.appendChild(itemRow)
  }
  block.appendChild(itemContainer)
}

function renderMainImg(block, dataList){
  const itemContainer = document.createElement("div") 
  itemContainer.className = "item-container"
  const itemImg = document.createElement("img")
  itemImg.className = "item-img"
  let image = dataList["image"]
  console.log(image)
  itemImg.src = image
  itemContainer.appendChild(itemImg)
  block.appendChild(itemContainer)
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
  // renderMainBlock(categoryStockContainer, categoryStock)
  renderMainImg(readyShippingStockContainer, readyShippingStock)
  // renderMainBlock(readyShippingStockContainer, readyShippingStock)
  // renderMainBlock(yesterdayProduceMostContainer, yesterdayProduceMost)
  // renderMainBlock(categoryYesterdayConsumeContainer, categoryYesterdayConsume)
  console.log(latestData)
}



window.addEventListener("load", (e)=>{
  initialPage()
  getNewestData()
})


