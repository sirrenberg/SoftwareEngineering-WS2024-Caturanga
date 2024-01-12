export function useAPI() {
  const API_URL = "http://localhost:8080";

  function sendRequest(route: string, 
                       method: string, 
                       body?: any, 
                       params?: {simulation_id: string, simsettings_id: string}) {
    const url = new URL(API_URL + route);

    if(params) {
      url.search = new URLSearchParams(params).toString();
    }

    console.log(body)
    return fetch(url.toString(), {
      method,
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    }).then((res) => res.json());
  }

  function delay(time: number) {
    return new Promise((resolve) => setTimeout(resolve, time));
  }

  return { sendRequest, delay };
}
