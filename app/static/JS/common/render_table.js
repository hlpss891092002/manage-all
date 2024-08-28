import{sentFetchWithoutBody} from "../common/sent_fetch_get_response.js"
import{addSpinner} from "../common/search_and_render.js"

export async function render_result_table(search_result, tableName, tableTitleContainer, table, PageAmount, dataAmount, router, staffPosition = null) {
  const resultKeys = Object.keys(search_result)
  tableTitleContainer.innerText =""
  const tableTitle = document.createElement("div")
  const DataCount = document.createElement("div")
  tableTitleContainer.appendChild(tableTitle)
  tableTitleContainer.appendChild(DataCount)
  // tableTitle.innerText = `Table ${tableName}`
  DataCount.innerText = ` Amount of row ${dataAmount }`
  table.innerText = ""
  let columnNameArray  =  Object.keys(search_result[0])
  const columnNameContainer = document.createElement("div")
  const rowContainer = document.createElement("div")
  columnNameContainer.className = "column-name-container "
  rowContainer.className= "row-container"
  //append column title
  columnNameArray.forEach((element)=>{
    if(element === "id" && tableName === "authorization"){
          return
        }
    let columnName =  document.createElement("div")
    columnName.className = "column-name row-value"
    columnName .innerText = element
    columnNameContainer.appendChild(columnName)
  })
  table.appendChild(columnNameContainer)
  //append row value
  const foreignColumnResult = await sentFetchWithoutBody("get",`/api/foreignList/${tableName}`)
  search_result.forEach((elementName)=>{
    const row = document.createElement("div")
    const elementArray = Object.entries(elementName)
    const valueKey = Object.values(elementName)[0]
    let updateIndexColumn = ""
    let updateIndexValue = ""
    row.className = `table-row `
    elementArray.forEach((element)=>{
      let  [key, value] = element
        if(key.includes("in_")){
          value = value === 1 ? "YES" : "NO";
        }else if(key === "id" && tableName === "authorization"){
          return
        }else if (tableName === "authorization"){
          value =  value === 1 ? "Authorized" : "Unauthorized"
        }
        let rowValue = document.createElement("div")
        rowValue.className = `row-value ${key}`
        rowValue.innerText = value
        if(elementArray.indexOf(element)===0){
          if (tableName ==="staff" && staffPosition === "Engineer"){
            return
          }
          updateIndexColumn = key
          updateIndexValue = value
          const formCheck = document.createElement("div")
          formCheck.className = `form-check checkbox row-value ${key}`
          if (staffPosition !== "Engineer" && tableName === "staff"){
            
          }else{
            formCheck.innerHTML= `<div class="form-check inner-from-check">
            <input class="form-check-input column-name-${key}" type="checkbox" id="${value}">
            `
          }
          
          row.addEventListener("click", (e)=>{
            if(e.target.nodeName === "INPUT" && e.target.classList.contains("form-check-input")){
              row.classList.toggle("border-primary") 
              row.classList.toggle("border") 
            }
          })
          let rowValueContainer = document.createElement("div")
          rowValueContainer.className = " row-value-container"
          rowValue = document.createElement("input")
          rowValue.className = `updatable index-${updateIndexColumn} column-${key} index-value-${updateIndexValue} `
          rowValue.placeholder = `${value}`
          rowValue.value = value
          if(key === "id" || (tableName === "produce_record" && key ==="variety") ||  (tableName === "produce_record" && key ==="producer") ){
            rowValue.disabled = true
          }else if ( tableName === "staff" && staffPosition !== 'Engineer'){
            rowValue.disabled = true
          }else if (staffPosition === 'Operator' && key === "employee_id"){
            console.log(staffPosition , key)
            rowValue.disabled = true
          }
          rowValue.addEventListener("input",(e)=>{
            const updateBtn = document.querySelector(".update-btn")
            rowValue.value !== updateIndexValue ? updateBtn.classList.add("bg-primary") : updateBtn.classList.remove("bg-primary")
          })
          formCheck.appendChild(rowValue)
          row.appendChild(formCheck)
          
        }else{
          let rowValueContainer = document.createElement("div")
          rowValueContainer.className = " row-value-container"
          rowValue = document.createElement("input")
          rowValue.className = `updatable index-${updateIndexColumn} column-${key} index-value-${updateIndexValue} `
          rowValue.placeholder = `${value}`
          rowValue.value = value
          if(key === "id"){
            rowValue.disabled = true
            rowValue.style.width = "auto"
          }else if( (tableName === "produce_record" && key ==="variety") ||  (tableName === "produce_record" && key ==="producer") ){
            rowValue.disabled = true
          }else if ( tableName === "staff"  && staffPosition !== 'Engineer'){
            rowValue.disabled = true
          }else if (staffPosition === 'Operator' && (key !== "variety_code"  || key !== "stage")){
            rowValue.disabled = true
          }
          rowValue.addEventListener("input",(e)=>{
            const updateBtn = document.querySelector(".update-btn")
            rowValue.value !== updateIndexValue ? updateBtn.classList.add("bg-primary") : updateBtn.classList.remove("bg-primary")
          })
          rowValueContainer.appendChild(rowValue)
          row.appendChild(rowValueContainer)
          const foreignColumnArray = foreignColumnResult["data"]
          if (foreignColumnArray[key]){
            let foreignColumnValueArray = foreignColumnArray[key]
            const dropdown = document.createElement("div")
            dropdown.className = "dropdown"
            const dropdownBtn = document.createElement("button")
            dropdownBtn.className = "btn btn-secondary dropdown-toggle"
            dropdownBtn.setAttribute("data-bs-toggle", "dropdown" )
            dropdownBtn.setAttribute("aria-expanded","false")
            const dropdownMenu = document.createElement("ul")
            dropdownMenu.className = `dropdown-menu dropdown-menu-${key} dropdown-menu-end scrollable-list`
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
            if ( tableName === "staff" && key === "job_position" && staffPosition !== 'Engineer'){
              return
            }else if(staffPosition === 'Operator' && key === "employee_id"){
              return
            }else{
              dropdown.appendChild(dropdownBtn)
            }
            
            dropdown.appendChild(dropdownMenu)
            rowValueContainer.appendChild(dropdown)
            
            dropdownMenu.addEventListener("click", (e)=>{
              const targetText = e.target.innerText
              const targetElementName = e.target.nodeName
              if(targetText === "CLEAR"){
                rowValue.value = ""
              }else if(targetElementName === "LI"){
                if(rowValue.value === targetText){
                  return
                }else{
                  rowValue.value = targetText
                  const updateBtn = document.querySelector(".update-btn")
                  updateBtn.classList.add("bg-primary")  
                }
                
              }else{
                return
              }
            })
          }
        }
  
      })
    rowContainer.appendChild(row)
    })
  table.appendChild(rowContainer)
  rowContainer.addEventListener("click",(e)=>{
    const target = e.target
    if (target.classList.contains("form-check-input")){
      const deleteBtn = document.querySelector(".delete-btn")
      let formCheckArray = document.querySelectorAll(".form-check-input")

      let unselectedNum = 0
      for (let check of formCheckArray){
         if (check.checked === true){
          continue
         }else{
          unselectedNum+=1                
         }
      }
      if(unselectedNum === formCheckArray.length){
        deleteBtn.classList.remove("bg-primary")
      }else{
        deleteBtn.classList.add("bg-primary")
      }
    }
  })
};

export async function render_pagination(pageAmount, paginationContainer, nowPage, router){
  paginationContainer.innerText =""
  const paginationNav= document.createElement("nav")
  paginationNav.className = "pagination-nav"
  paginationNav.setAttribute("aria-label", "Page navigation")
  const pagination = document.createElement("ul")
  let startPage = 0
  let endPage = 0
  paginationContainer.appendChild(pagination)

    const updateBTN = document.createElement("button")
    updateBTN.className = `update-btn`
    const updateImg = document.createElement("img")
    updateImg.src = "./static/icon/upload.png"
    updateBTN.appendChild(updateImg)
    paginationContainer.appendChild(updateBTN)

    const deleteBTN = document.createElement("button")
    deleteBTN.className = `delete-btn `
    const deleteImg = document.createElement("img")
    deleteImg.src = "./static/icon/trash-can.png"
    deleteBTN.appendChild(deleteImg)
    paginationContainer.appendChild(deleteBTN)

    
 
  pagination.className = "pagination justify-content-center"
  const frontArrow = document.createElement("li")
  frontArrow.className = "page-item front-arrow"
  const frontSpan = document.createElement("span")
  frontSpan.className = "page-link"
  frontSpan.innerText = "Previous"
  frontArrow.appendChild(frontSpan)
  pagination.appendChild(frontArrow)

  
  if (nowPage <= 4){
    startPage = 0
  }else if( pageAmount - nowPage  <= 10){
    startPage =  pageAmount - 10
  }else{
    startPage = nowPage - 4
  }

  if(pageAmount <10){
    endPage = endPage + pageAmount
  }else{
    endPage = endPage + 10
  }
  for (let i = startPage; i < startPage + endPage ; i++){
    const pageItem = document.createElement("li")
    if(i === nowPage ){
      pageItem.className = `page-item page${i} active`
    }else{
      pageItem.className = `page-item page${i}`
    }
    const num = i +1 
    const pageSpan = document.createElement("span")
    pageSpan.className = "page-link"
    pageSpan.innerText = num
    pageItem.append(pageSpan)
    pagination.appendChild(pageItem)
  }

  const backArrow = document.createElement("li")
  backArrow.className = "page-item back-arrow"
  const backSpan = document.createElement("span")
  backSpan.className = "page-link"
  backSpan.innerText = "Next"
  backArrow.appendChild(backSpan)
  pagination.appendChild(backArrow)

}

export function clearMessageAndTable(){
  const message = document.querySelector(".message")
  const table = document.querySelector(".table")
  const tableTitleContainer = document.querySelector(".table-title-container")
  const paginationContainer = document.querySelector(".pagination-container")
  message.innerText = ""
  table.innerText = ""
  tableTitleContainer.innerText = ""
  paginationContainer.innerText = ""
}

export async function render_table_from_pagination(nowPage, PageAmount, callback1, callback2,table) {
  const pagination = document.querySelector(".pagination")
  let targetPage = 0
  pagination.addEventListener("click",(e)=>{
    const target = e.target.innerText
    const targetElementName = e.target.nodeName
    if(targetElementName !== "SPAN"){
      return
    }else if (nowPage === target -1){
      e.preventDefault()
    }else if(target === "Previous" && nowPage === 0){
      e.preventDefault()
    }else if(target === "Next" && nowPage === PageAmount -1 ){
      e.preventDefault()
    }else{
      if(target === "Previous"){
          targetPage = nowPage - 1
      }else if(target === "Next"){
        targetPage = nowPage + 1
      }else{
        targetPage = target - 1
      }
      callback1(table)
      callback2(targetPage)
    }
  })
}