export function useAPI() {
  const API_URL = "http://localhost:8080";

  function sendRequest(route: string, method: string, body?: any) {
    const url = new URL(API_URL + route);
    
    // locations, routes and conflicts should not be POSTed to the server
    if (body) {
      delete body['locations']
      delete body['routes']
      delete body['conflicts']
    }

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
