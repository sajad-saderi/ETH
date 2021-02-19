let getCookie = function(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

let close_issue = function(id) {
    let httpRequest = new XMLHttpRequest();
    httpRequest.open('DELETE', "/issues/" + id + "/close");
    httpRequest.setRequestHeader('X-XSRFToken', getCookie("_xsrf"));
    httpRequest.onreadystatechange = function () {
            console.log(this.responseText);
            window.location.replace("/issues/");
        };
    httpRequest.send();
}
