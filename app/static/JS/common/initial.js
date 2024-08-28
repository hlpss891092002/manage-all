import{sentFetchWithoutBody, sentFetchWithBody} from "../common/sent_fetch_get_response.js"

export async function getAccountFromAutho() {
  const autho = await sentFetchWithoutBody("get","/api/staff/auth")
  const employee_id = await autho["employee_id"]
  const job_position = await autho["job_position"]
  const name = await autho["sub"]
  console.log(autho)
  let staffData = {}
  staffData["employee_id"] = employee_id
  staffData["job_position"] = job_position
  staffData["name"] = name
  if(autho["error"]){
    return false
  }else{
    return staffData
  }   
}

export async function renderSideBlockList(employee_id, staffPosition, inputContainer, tableName, router, searchInputContainer){
  if(!employee_id){
    localStorage.clear()
    window.location.assign("/")
  }

  console.log(router)
  // get tables according auth
  const tables = await sentFetchWithoutBody("get","/api/staff/tables")
  //render side block
  for (let table of tables){
    const listGroup = document.querySelector(".list-group")
    const sideMainList = document.createElement("li")
    sideMainList.className ="list-group-item list-group-item-primary side-title "
    sideMainList.id = `side-block-${table}`
    sideMainList.setAttribute("data-bs-toggle", "collapse")
    sideMainList.setAttribute("data-bs-target",`#${table}-sub-list`)
    sideMainList.innerText = table
    listGroup.appendChild(sideMainList)
    const methodArray = ["add","search & modified"]
    const subList = document.createElement("ul")
    subList.className = "list-group  collapse"
    subList.id = `${table}-sub-list`
    listGroup.appendChild(subList)
    for (let method of methodArray){
      const listItem = document.createElement("li")
      listItem.className = "list-group-item"
      const methodItem = document.createElement("a")
      switch (method){
        case "add":
          if(table == "staff" && staffPosition !="Engineer"){
            break
          }else{
            listItem.id = `add-${table}`
            methodItem.className= ""
            methodItem.href = `/add?${table}`
            methodItem.innerText = "add"
            listItem.appendChild(methodItem)
            subList.appendChild(listItem)
            break
          }
        case "search & modified":
          listItem.id = `search-${table}`
          methodItem.className= ""
          methodItem.href = `/search?${table}`
          methodItem.innerText = "search & modified"
          listItem.appendChild(methodItem)
          subList.appendChild(listItem)
          break
      }
    }
    // sideMainList.addEventListener("click",(e)=>{
    //   e.preventDefault()
    //   window.location.assign(`/search?${table}`)
    // })
  }
    showSideBlockFromRouter(tableName)
    if (router === "add"){
      const activeSubListItem = document.querySelector(`#${router}-${tableName}`)
      activeSubListItem.classList.add("active")
    }else if (router === "search"){
      const activeSubListItem = document.querySelector(`#${router}-${tableName}`)
      activeSubListItem.classList.add("active")
    }

    
  //disabled select
  const selectRouter = document.querySelector(`#side-block-${tableName}`) 
  selectRouter.classList.add("disabled")
  selectRouter.style.backgroundColor = "#CFE2FF"
  
  // get item according table
  if(router !== "staffIndex"){
    const columnInputResult = await sentFetchWithoutBody("get",`/api/${router}/tableItem/${tableName}`)
    const foreignColumnResult = await sentFetchWithoutBody("get",`/api/foreignList/${tableName}`)
    const foreignColumnArray = foreignColumnResult["data"]
    const columns = columnInputResult["data"]
    if(searchInputContainer){
      let searchIndex = ""
      switch (tableName){
        case "staff":
          searchIndex = "employee_id"
          break
        case "client_order":
          searchIndex = "id"
          break
        default:
          searchIndex = columns[0]
          break
      }
      const inputGroup = document.createElement("div")
      inputGroup.className = "input-group "
      const inputGroupText = document.createElement("div")
      inputGroupText.className = "input-group-text"
      inputGroupText.innerText = `${searchIndex}`
      const categoryInput = document.createElement("input")
      categoryInput.className = `form-control  ${router}-index search-${searchIndex}`
      inputGroup.appendChild(inputGroupText)
      inputGroup.appendChild(categoryInput)
      searchInputContainer.prepend(inputGroup)
    }
    // insert item block
    if (inputContainer){
      for (let column of columns){
      if (column === "id" && router === "add"){
        continue
      } else if(column === "produce_time"){
        continue 
      }else if (router === "add" && column ==="consumed_date"){
        continue
      }else if( column === "authorization"){
        column = "job_position"
      }
      const inputGroup = document.createElement("div")
      inputGroup.className = "input-group "
      inputGroup.innerHTML = `<span class="input-group-text ${column}-input-disc">${column}</span>`
      let inputItem = document.createElement("input");
      inputItem.className = `form-control ${column}-input update-item`
      if (column.includes("date")){
        inputItem.type = "date"
      }
      if(foreignColumnArray[column]){
        let foreignColumnValueArray = foreignColumnArray[column]
        const dropdown = document.createElement("div")
        dropdown.className = "dropdown"
        const dropdownBtn = document.createElement("button")
        dropdownBtn.className = "btn btn-secondary dropdown-toggle"
        dropdownBtn.setAttribute("data-bs-toggle", "dropdown" )
        dropdownBtn.setAttribute("aria-expanded","false")
        const dropdownMenu = document.createElement("ul")
        dropdownMenu.className = `dropdown-menu dropdown-menu-${column} dropdown-menu-end scrollable-list`
        dropdownMenu.id = ""
        for(let value of foreignColumnValueArray){
          if(foreignColumnValueArray.indexOf(value) === 0){
            const dropdownItem = document.createElement("li")
            dropdownItem.className = "dropdown-item clear-item"
            dropdownItem.innerText = "CLEAR"
            dropdownMenu.appendChild(dropdownItem)
          }
          const dropdownItem = document.createElement("li")
          dropdownItem.className = "dropdown-item"
          dropdownItem.innerText = value
          dropdownMenu.appendChild(dropdownItem)
        }
        dropdown.appendChild(dropdownBtn)
        dropdown.appendChild(dropdownMenu)
        inputGroup.appendChild(inputItem)
        inputGroup.append(dropdown)
        dropdownMenu.addEventListener("click", (e)=>{
          const targetText = e.target.innerText
          const targetElementName = e.target.nodeName
          if(targetText === "CLEAR"){
            inputItem.value = ""
          }else if(targetElementName === "LI"){
            inputItem.value = targetText
          }else{
            return
          }
        })
      }else{
        inputGroup.appendChild(inputItem)
        // inputGroup.appendChild(clearBtn)
      }
      inputContainer.appendChild(inputGroup)
      
      }
      console.log(inputContainer.children.length)
      console.log(window.innerWidth)
      const windowInnerWith = window.innerWidth
      const inputContainerChildrenNum = inputContainer.children.length
      if(inputContainerChildrenNum == 2 && windowInnerWith > 1000){
        console.log("true")
        inputContainer.style.gridTemplateColumns ="1fr 1fr" 
      }else if(inputContainerChildrenNum == 3 && windowInnerWith > 1200){
        console.log("true 2 ")
        inputContainer.style.gridTemplateColumns ="1fr 1fr 1fr" 
      }
      if (tableName === "produce_record" && router === "add"){
        console.log(employee_id)
        const producerInput = document.querySelector(".employee_id-input")
        producerInput.value =  employee_id
        
      }
    }else{
      return
    }
    
  }
}

export function signOutFunction(){
  const sigOutBTN = document.querySelector(".sign-out")
  sigOutBTN.addEventListener("click",()=>{
    localStorage.clear()
    location.assign("/")
  })
}

export function showSideBlockFromRouter(tableName){
  console.log(tableName)
  const sideBlock = document.querySelector(`#side-block-${tableName}`)
  console.log(`#side-block-${tableName}`)
  console.log(sideBlock)
  const sideSubList = document.querySelector(`#${tableName}-sub-list`)
  sideBlock.classList.remove("collapsed")
  sideSubList.classList.add("show")
}

export function renderSlogan(router){
  const mainPAge=  document.querySelector("main-page")
  const welcome = document.createElement("section")
  mainPAge.prepend()
}

export async function renderStaffInNav(staffData){
  const navbarNav = document.querySelector(".navbar-nav")
  console.log(staffData)
  const staffName = staffData["name"]
  const staffPosition = staffData["job_position"]
  const nameBlock = document.createElement("div")
  nameBlock.className="name-block"
  nameBlock.innerText = `${staffName} ${staffPosition}`
  navbarNav.prepend(nameBlock)
}
