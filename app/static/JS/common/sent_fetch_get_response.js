export async function sentFetchWithBody(method , body, url){
  const token = localStorage["userState"] ? localStorage["userState"] : ""
  const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": `Bearer ${token}`
      }
        let response = await fetch(`${url}`,{
          method:`${method.toUpperCase()}`,
          headers: headers,
          body: JSON.stringify(body)
        })
        let data = response.json()
      return data
}
export async function sentFetchWithoutBody(method,url){
  const token = localStorage["userState"] ? localStorage["userState"] : ""
  const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": `Bearer ${token}`
      }
      let response = await fetch(`${url}`,{
        method:`${method.toUpperCase()}`,
        headers: headers,
      })
      let data = response.json()
      return data
}

export async function sentFetchWithParams(method , params, url){
  console.log(params)
  console.log(url)
  params["condition"] = JSON.stringify(params["condition"])
  const searchParams = new URLSearchParams(params).toString()
  console.log(searchParams)
  url = `${url}?${searchParams}`
  const token = localStorage["userState"] ? localStorage["userState"] : ""
  const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": `Bearer ${token}`
      }
        let response = await fetch(`${url}`,{
          method:`${method.toUpperCase()}`,
          headers: headers,
        })
        let data = response.json()
      return data
}