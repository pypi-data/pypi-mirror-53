function getCsrfTokenCookie() {
    console.log(document.cookie.split(";"));
    for (const cookie of document.cookie.split(";")) {
        if (cookie.includes("csrftoken")) {
            const substring = null;

            if (cookie.indexOf(" ") !== -1) {
                console.log(cookie.substring(11))
                return cookie.substring(11)
            }

            else {
                console.log(cookie.substring(10))
                return cookie.substring(10)
            }
        }
    }
    return null
}

export function AJAXRequest(method, target, callback, async = true, data = null) {
    const xhr = new XMLHttpRequest();
    let response = null;

    xhr.addEventListener("readystatechange", function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                response = JSON.parse(xhr.responseText);
                callback(response)
            }
        }
    });

    xhr.open(method, target, async);

    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

    const csrf_token = getCsrfTokenCookie();
    console.log("CSRF = " + csrf_token);

    if (csrf_token) {
        xhr.setRequestHeader("X-CSRFToken", csrf_token);
        console.log("CSRF = " + csrf_token);
    }

    xhr.send(data);
}