const button = document.getElementById("submit-button");
button.addEventListener("click", addURL);
button.addEventListener("click", displayURLs);

let url;

function addURL() {
    url = document.getElementById("url").value;
    url = url.toLowerCase();
}

function displayURLs(){
    document.getElementById("urls").innerHTML = url;
}