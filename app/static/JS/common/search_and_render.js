import {render_result_table, render_pagination, render_table_from_pagination, clearMessageAndTable} from "../common/render_table.js"
import{sentFetchWithParams} from "../common/sent_fetch_get_response.js"

export async function sent_input_search_and_render_table(body, tableName, PageAmount, paginationContainer, nowPage, search_and_render, tableTitleContainer, message, table, dataAmount){
  let result = await sentFetchWithParams("get", body, `/api/${tableName}`)
  console.log(result)
  let data = result["data"]
  nowPage = parseInt(result["startPage"])
  dataAmount = result["dataAmount"]
  console.log(nowPage)
  if(data.length < 1){
    message.innerText = "no data"
  }else{
    PageAmount = result["PageAmount"]
    // render_table_from_pagination(nowPage, PageAmount)
    render_pagination(PageAmount, paginationContainer, nowPage)
    render_table_from_pagination(nowPage, PageAmount, search_and_render)
    render_result_table(data, tableName, tableTitleContainer, table, PageAmount, dataAmount )
  }
  return result
};