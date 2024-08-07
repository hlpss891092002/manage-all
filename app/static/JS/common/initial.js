import{sentFetchWithoutBody, sentFetchWithBody} from "../common/sent_fetch_get_response.js"

export async function getAccountFromAutho() {
    const autho = await sentFetchWithoutBody("get","/api/staff/auth")
  const account = await autho["account"]
  // console.log(account)
  // staffId = await account
  return account

}

export async function renderSideBlockList(account, addSubList, searchSubList, updateSubList, inputContainer, tableName, router, searchInputContainer){
  if(!account){
    window.location.assign("/")
  }
  console.log(updateSubList)
  console.log(router)
  // get tables according auth
  const tables = await sentFetchWithoutBody("get","/api/staff/tables")
  //render side block
  for (let tableName of tables){
    if(tableName === "current_stock"){
      continue
    }
    const searchListItem = document.createElement("li")
    searchListItem.className = "list-group-item"
    const searchItemLink = document.createElement("a")
    searchItemLink.href = `/search?${tableName}`
    searchItemLink.innerText= tableName
    searchListItem.appendChild(searchItemLink)
    searchSubList.appendChild(searchListItem)


    const addListItem = document.createElement("li")
    addListItem.className = "list-group-item"
    const addItemLink = document.createElement("a")
    addItemLink.href = `/add?${tableName}`
    addItemLink.innerText= tableName
    addListItem.appendChild(addItemLink)
    addSubList.appendChild(addListItem)

    const updateListItem = document.createElement("li")
    updateListItem.className = "list-group-item"
    const updateItemLink = document.createElement("a")
    updateItemLink.href = `/update?${tableName}`
    updateItemLink.innerText= tableName
    updateListItem.appendChild(updateItemLink)
    updateSubList.appendChild(updateListItem)
    
  }
  // get item according table
  if(router !== "staffIndex"){
    const result = await sentFetchWithoutBody("get",`/api/${router}/tableItem/${tableName}`)
    const columns = result["data"]
    if(searchInputContainer){
      let searchIndex = ""
      switch (tableName){
        case "staff":
          searchIndex = "account"
          break
        case "client_order":
          searchIndex = "id"
          break
        default:
          searchIndex = columns[0]
          break
      }
      const inputGroup = document.createElement("div")
      inputGroup.className = "input-group mb-3 "
      const inputGroupText = document.createElement("div")
      inputGroupText.className = "input-group-text"
      inputGroupText.innerText = `${searchIndex}`
      const categoryInput = document.createElement("input")
      categoryInput.className = `form-control  update-index search-${searchIndex}`
      inputGroup.appendChild(inputGroupText)
      inputGroup.appendChild(categoryInput)
      searchInputContainer.appendChild(inputGroup)
    }
    // insert item block
    for (let column of columns){
      if (column === "id" && router === "add"){
        continue
      }else if(column === "manufacturing_time"){
        continue
      }else if(column === "authorization"){
        continue
      }
      const inputGroup = document.createElement("div")
      inputGroup.className = "input-group mb-3 "
      inputGroup.innerHTML = `<span class="input-group-text ${column}-input-disc">${column}</span>`
      let inputItem = document.createElement("input");
      inputItem.className = `form-control ${column}-input update-item`
      if (column.includes("date")){
        inputItem.type = "date"
      }
      inputGroup.appendChild(inputItem)
      inputContainer.appendChild(inputGroup)
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
    if (tableName === "produce_record" && router === "add"){
      const producerInput = document.querySelector(".producer_id-input")
      producerInput.value = await account
    }
  }
}

export function signOutFunction(){
  const sigOutBTN = document.querySelector(".sign-out")
  sigOutBTN.addEventListener("click",()=>{
    localStorage.clear()
    location.reload()
  })
}

export function showSideBlockFromRouter(router){
  const sideBlock =document.querySelector(`#side-block-${router}`)
  const sideSubList =document.querySelector(`#${router}-sub-list`)
  console.log(sideBlock)
  console.log(sideSubList) 
  sideBlock.classList.remove("collapsed")
  sideSubList.classList.add("show")
}