import{sentFetchWithoutBody} from "../common/sent_fetch_get_response.js"
const addSubList = document.querySelector("#add-sub-list")
const searchSubList = document.querySelector("#search-sub-list")


async function initialPage(){
// get auth
  const autho = await sentFetchWithoutBody("get","/api/staff/auth")
  const account = await autho["account"]
  console.log(account)
  let staffId = await account

  if(!account){
    window.location.assign("/")
  }
  // get tables according auth for side block
  const tables = await sentFetchWithoutBody("get","/api/staff/tables")
  for (let tableName of tables){
    const addListItem = document.createElement("li")
    addListItem.className = "list-group-item"
    const addItemLink = document.createElement("a")
    addItemLink.href = `/insert?${tableName}`
    addItemLink.innerText= tableName
    addListItem.appendChild(addItemLink)
    addSubList.appendChild(addListItem)

    const searchListItem = document.createElement("li")
    searchListItem.className = "list-group-item"
    const searchItemLink = document.createElement("a")
    searchItemLink.href = `/search?${tableName}`
    searchItemLink.innerText= tableName
    searchListItem.appendChild(searchItemLink)
    searchSubList.appendChild(searchListItem)

  }
}

window.addEventListener("load", (e)=>{
  initialPage()
})


