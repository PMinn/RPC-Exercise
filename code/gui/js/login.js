document.getElementById("sub_btn").addEventListener("click", () => {
    var username = document.querySelector("#usernameInput").value;
    window.parent.login(username)
});