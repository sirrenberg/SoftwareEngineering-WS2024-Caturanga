export function useAPI() {
  const API_URL = "http://34.254.183.97";

  function sendRequest(route: string, method: string, body?: any) {
    return fetch(API_URL + route, {
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
