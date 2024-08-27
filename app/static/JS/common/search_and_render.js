import {render_result_table, render_pagination, render_table_from_pagination, clearMessageAndTable} from "../common/render_table.js"
import{sentFetchWithParams} from "../common/sent_fetch_get_response.js"
export async function sent_input_search_and_render_table(body, tableName, PageAmount, paginationContainer, nowPage, search_and_render, tableTitleContainer, message, table, dataAmount, router, staffPosition, searchBtn){
  let searchResult = await sentFetchWithParams("get", body, `/api/${tableName}`)
  if(searchResult){
    searchBtn.disabled = false
  }
  console.log(searchResult)
  let data = searchResult["data"]
  let error = searchResult["error"]
  nowPage = parseInt(searchResult["startPage"])
  dataAmount = searchResult["dataAmount"]
  console.log(nowPage)
  if (error){
    const errorMessage = searchResult["message"]
    table.innerText = ""
    if(errorMessage.includes("NoneType")){
      message.innerText = "The input value isn't exist.  Please check input value"
    }else{
      message.innerText = errorMessage
    }
    
  }else if(data.length < 1){
    message.innerText = "no data"
    console.log(table)
    table.innerText = ""
  }else{
    PageAmount = searchResult["PageAmount"]
    // render_table_from_pagination(nowPage, PageAmount)
    render_pagination(PageAmount, paginationContainer, nowPage, router)
    render_table_from_pagination(nowPage, PageAmount, addSpinner, search_and_render, table)
    render_result_table(data, tableName, tableTitleContainer, table, PageAmount, dataAmount, router, staffPosition )
    
  }
  return searchResult
};

export function addSpinner(table){
  const spinnerBorder = document.createElement("div")
  spinnerBorder.className = "spinner-border"
  spinnerBorder.setAttribute("role", "status")
  const spinner = document.createElement("span")
  spinner.className = "sr-only"
  spinnerBorder.appendChild(spinner)
  table.innerText = ""
  table.appendChild(spinnerBorder)
}