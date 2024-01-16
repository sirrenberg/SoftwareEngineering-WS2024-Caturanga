export function useAPI() {
  const API_URL = "https://sj6mxvhnt8.execute-api.eu-west-1.amazonaws.com";

  function sendRequest(route: string, 
                       method: string, 
                       body?: any) {
    const url = new URL(API_URL + route);

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
