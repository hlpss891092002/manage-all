export async function render_result_table(search_result, tableName, tableTitleContainer, table, PageAmount, dataAmount ) {
  const resultKeys = Object.keys(search_result)
  const tableTitle = document.createElement("div")
  const DataCount = document.createElement("div")
  tableTitleContainer.appendChild(tableTitle)
  tableTitleContainer.appendChild(DataCount)
  tableTitle.innerText = `Table ${tableName}`
  DataCount.innerText = ` Amount of row ${dataAmount }`
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
    const row = document.createElement("div")
    const elementArray = Object.entries(elementName)
    row.className = `table-row `
    elementArray.forEach((element)=>{
        let  [key, value] = element 
        if(key.includes("in_")){
          value = value === 1 ? "YES" : "NO";
        }
        let rowValue = document.createElement("div")
        rowValue.className = `row-value ${key}`
        rowValue.innerText = value 
        row.appendChild(rowValue)  
      })
    rowContainer.appendChild(row)
    })
  table.appendChild(rowContainer)

};

export async function render_pagination(pageAmount, paginationContainer, nowPage){
  const paginationNav= document.createElement("nav")
  paginationNav.className = "pagination-nav"
  paginationNav.setAttribute("aria-label", "Page navigation")
  const pagination = document.createElement("ul")
  let startPage = 0
  let endPage = 0
  paginationContainer.appendChild(pagination)
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
    startPage = nowPage - 5
  }

  if(pageAmount <10){
    endPage = endPage + pageAmount
  }else if(pageAmount- nowPage < 6){
    endPage = startPage + 5
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


  // <nav aria-label="Page navigation example">
  //   <ul class="pagination">
  //     <li class="page-item"><a class="page-link" href="#">Previous</a></li>
  //     <li class="page-item"><a class="page-link" href="#">1</a></li>
  //     <li class="page-item"><a class="page-link" href="#">2</a></li>
  //     <li class="page-item"><a class="page-link" href="#">3</a></li>
  //     <li class="page-item"><a class="page-link" href="#">Next</a></li>
  //   </ul>
  // </nav>
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

export async function render_table_from_pagination(nowPage, PageAmount, callback) {
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
      clearMessageAndTable()
      if(target === "Previous"){
          targetPage = nowPage - 1
      }else if(target === "Next"){
        targetPage = nowPage + 1
      }else{
        targetPage = target - 1
      }
      callback(targetPage)
    }
  })
}