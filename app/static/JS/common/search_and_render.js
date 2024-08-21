import {render_result_table, render_pagination, render_table_from_pagination, clearMessageAndTable} from "../common/render_table.js"
import{sentFetchWithParams} from "../common/sent_fetch_get_response.js"

export async function sent_input_search_and_render_table(body, tableName, PageAmount, paginationContainer, nowPage, search_and_render, tableTitleContainer, message, table, dataAmount, router){
  let searchResult = await sentFetchWithParams("get", body, `/api/${tableName}`)
  console.log(searchResult)
  let data = searchResult["data"]
  nowPage = parseInt(searchResult["startPage"])
  dataAmount = searchResult["dataAmount"]
  console.log(nowPage)
  if(data.length < 1){
    message.innerText = "no data"
  }else{
    PageAmount = searchResult["PageAmount"]
    // render_table_from_pagination(nowPage, PageAmount)
    render_pagination(PageAmount, paginationContainer, nowPage, router)
    render_table_from_pagination(nowPage, PageAmount, search_and_render)
    render_result_table(data, tableName, tableTitleContainer, table, PageAmount, dataAmount, router )
    
  }
  return result
};