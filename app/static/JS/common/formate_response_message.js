
export function formateAddResponse(result, responseMessage, tableName, firstColumnValue){
  if (result["ok"]){
    renderOkMessage(responseMessage, tableName, firstColumnValue)
  }else{
    const message = result["message"].replaceAll("'", "")

    const  messageArray = message.split(" ")
    if (message.includes("Duplicate entry")){
      console.log(messageArray)
      const key = messageArray[messageArray.indexOf("key")+1].split(".")[1]
      console.log(key)
      const value = messageArray[messageArray.indexOf("entry")+1]
      responseMessage.innerText = `${key} : "${value}"  already exist`
    }else if(message.includes("cannot be null")){
      const column = messageArray[messageArray.indexOf("Column")+1].split("_")[0]
      let item = ""
      let value = ""
      if(column === "variety"){
        item = column + "_code"
        value = body[`${item}`]
      }else{
        item = column
        value = body[`${item}`]
      }
      responseMessage.innerText = `${item} : "${value}"  is not  exist`
    }else{
      responseMessage.innerText = message
    }
  }
}
export function renderOkMessage(responseMessage, tableName, firstColumnValue){
  const successMessage = document.createElement("div")
  successMessage.className = "success-message"
  successMessage.innerText = "add success"
  responseMessage.appendChild(successMessage)
  const guidMessage = document.createElement("div")
  guidMessage.className = "guid-message"
  

  switch(tableName){
    case "category":
      createGuideNext(guidMessage, firstColumnValue,"variety", tableName)
      createGuideSearch(guidMessage, firstColumnValue,tableName)
      break
    case "client":
      createGuideNext(guidMessage, firstColumnValue,"client_order", tableName)
      createGuideSearch(guidMessage, firstColumnValue,tableName)
      break
    case "client_order":
      createGuideSearch(guidMessage, firstColumnValue,tableName)
      break
    case "media":
      createGuideNext(guidMessage, firstColumnValue,"produce_record", tableName)
      createGuideSearch(guidMessage, firstColumnValue,tableName)
      break
    case "produce_record":
      createGuideSearch(guidMessage, firstColumnValue,tableName)
      break
    case "staff":
      createGuideNext(guidMessage, firstColumnValue,"produce_record", tableName)
      createGuideSearch(guidMessage, firstColumnValue,tableName)
      break
    case "stage":
      createGuideNext(guidMessage, firstColumnValue,"produce_record", tableName)
      createGuideSearch(guidMessage, firstColumnValue,tableName)
      break
    case "variety":
      createGuideNext(guidMessage, firstColumnValue,"client_order", tableName)
      createGuideNext(guidMessage, firstColumnValue,"produce_record", tableName)
      createGuideSearch(guidMessage, firstColumnValue,tableName)
      break
  }
  responseMessage.appendChild(guidMessage)
}
export function createGuideNext(guidMessage, firstColumnValue, LinkTableName, tableName){
  const guidNextBlock = document.createElement("div")
  guidNextBlock.className = "guid-next-block guide-block" 
  const guidLinkNext = document.createElement("a")
  guidLinkNext.className = "guid-link-next "
  const guidNextText = document.createElement("div")
  guidNextText.className = "guid-next-text "
  guidNextText.innerText=`Would you want to add new ${LinkTableName} for ${firstColumnValue} ${tableName}?` 
  guidNextBlock.appendChild(guidNextText)
  guidLinkNext.innerText="Please click here"
  guidLinkNext.href = `/add?${LinkTableName}`
  guidNextBlock.appendChild(guidLinkNext)
  guidMessage.appendChild(guidNextBlock)
}

export function createGuideSearch(guidMessage, firstColumnValue,tableName){
  const guidSearchBlock = document.createElement("div")
  guidSearchBlock.className = "guid-search-block guide-block" 
  const guidLinkSearch = document.createElement("a")
  guidLinkSearch.className = "guid-link-search"
  const guidSearchText = document.createElement("div")
  guidSearchText.className = "guid-search-text"
  guidSearchText.innerText=`Would  you  to  check the information of  ${firstColumnValue} ${tableName} ?`
  guidLinkSearch.innerText="Please click here"
  guidLinkSearch.href = `/search?${tableName}`
  guidSearchBlock.appendChild(guidSearchText) 
  guidSearchBlock.appendChild(guidLinkSearch) 
  guidMessage.appendChild(guidSearchBlock)
}