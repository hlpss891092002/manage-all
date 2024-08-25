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
    if(errorMessage.includes("NoneType")){
      message.innerText = "The input value isn't exist.  Please check input value"
    }else{
      message.innerText = errorMessage
    }
    
  }else if(data.length < 1){
    message.innerText = "no data"
  }else{
    PageAmount = searchResult["PageAmount"]
    // render_table_from_pagination(nowPage, PageAmount)
    render_pagination(PageAmount, paginationContainer, nowPage, router)
    render_table_from_pagination(nowPage, PageAmount, search_and_render)
    render_result_table(data, tableName, tableTitleContainer, table, PageAmount, dataAmount, router, staffPosition )
    
  }
  return searchResult
};