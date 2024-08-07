import{sentFetchWithoutBody} from "../common/sent_fetch_get_response.js"
import{getAccountFromAutho, renderSideBlockList, signOutFunction, showSideBlockFromRouter} from "../common/initial.js"
const addSubList = document.querySelector("#add-sub-list")
const searchSubList = document.querySelector("#search-sub-list")
const updateSubList = document.querySelector("#update-sub-list")
const inputContainer = document.querySelector(".input-container")
const searchInputContainer = document.querySelector(".search-input-container")
const table = document.querySelector(".table")
const query = window.location.search
const tableName = query.slice(1, query.length)
const router = location.pathname.replace("/", "")
let staffId = ""


async function initialPage(){
  let account = await getAccountFromAutho()
  staffId = account
  renderSideBlockList(staffId, addSubList, searchSubList,updateSubList, inputContainer, tableName, router, searchInputContainer)
  signOutFunction()

  if(!account){
    window.location.assign("/")
  }

}

window.addEventListener("load", (e)=>{
  initialPage()
})


