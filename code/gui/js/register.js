document.getElementById("sub_btn").addEventListener("click", () => {
    var username = document.querySelector("#usernameInput").value;
    if (username == '') {
        window.parent.warning('名稱不能為空');
    } else {
        window.parent.register(username);
    }
});