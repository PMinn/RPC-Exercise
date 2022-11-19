const listGroup = document.querySelector('#left>div');
const createDiv = document.getElementById('createDiv');
const createFrame = document.getElementById('createFrame');
const registerFrame = document.getElementById('registerFrame');
const postFrame = document.getElementById('postFrame');

var isLogin = false;
var loginedUsername = "";

var subjects = [];

const warn = new bootstrap.Modal(document.getElementById('warn'), {
    keyboard: false
})
const warn_body = document.querySelector("#warn .modal-body");

var delete_check = new bootstrap.Modal(document.getElementById('delete_check'), {
    keyboard: false
})
var delete_check_body = document.querySelector("#delete_check .modal-body");
var delete_check_btn = document.querySelector("#delete_check .btn-primary");

function left_init() {
    listGroup.innerHTML = '';
}

function getSubjects() {
    return eel.subject()()
        .then(s => {
            subjects = JSON.parse(s)
        })
}

function render_subject() {
    subjects.forEach(subject => {
        var button = document.createElement('button');
        button.type = "button";
        button.classList.add('list-group-item');
        button.classList.add('list-group-item-action');
        button.classList.add('d-flex');
        button.classList.add('justify-content-between');
        button.classList.add('align-items-start');
        button.innerHTML = `
                <div class="fw-bold">${subject.topic.map(t => t.data.text).join('')}</div>
                <span class="badge rounded-pill">${subject.numOfReply}</span>
            `;
        listGroup.appendChild(button);

        button.addEventListener('click', () => {
            post_to(subject.id);
        });
    })
}

function post_init() {
    postFrame.src = `./post.html?id=${subjects[0].id}`;
    eel.setLastViewPost(subjects[0].id);
}

function post_to(id) {
    postFrame.src = `./post.html?id=${id}`;
    eel.setLastViewPost(id);
}

function createFrameClear() {
    createFrame.contentWindow.clear();
}

function create() {
    createFrame.contentWindow.save()
        .then(savedata => {
            if (savedata[0].blocks.length > 0 && savedata[0].blocks.length > 0) {
                // console.log(savedata);//savedata[i].blocks
                eel.create({
                    "topic": savedata[0].blocks,
                    "content": savedata[1].blocks
                })()
                    .then(response => {
                        createFrameClear();
                        reload();
                        post_to(JSON.parse(response.text).id);
                    })
            }
            close_fixedPage('#createDiv');
        });
}

function open_fixedPage(query) {
    var targetDOM = document.querySelector(query);
    targetDOM.style.display = "block";
    setTimeout(() => {
        targetDOM.style.opacity = "1";
    }, 100)
}

function close_fixedPage(query) {
    var targetDOM = document.querySelector(query);
    targetDOM.style.opacity = "0";
    setTimeout(() => {
        targetDOM.style.display = "none";
    }, 300)
}

function register(username) {
    eel.register(username)()
        .then(response => {
            if (response.code >= 200 && response.code <= 299) {
                isLogin = true;
                loginedUsername = username;
                document.getElementById("loginedUsername").innerText = username;
                close_fixedPage('#registerDiv');
                document.getElementById("register_btn").remove();
                document.getElementById("login_btn").remove();
                document.getElementById('create_btn').style.display = 'block';
                postFrame.contentWindow.location.reload();
            } else return Promise.reject(JSON.parse(response.text).error);
        })
        .catch(warning)
}

function login(username) {
    eel.login(username)()
        .then(response => {
            if (response.code >= 200 && response.code <= 299) {
                isLogin = true;
                loginedUsername = username;
                document.getElementById("loginedUsername").innerText = username;
                close_fixedPage('#loginDiv');
                document.getElementById("register_btn").remove();
                document.getElementById("login_btn").remove();
                document.getElementById('create_btn').style.display = 'block';
                postFrame.contentWindow.location.reload();
            } else return Promise.reject(JSON.parse(response.text).error);
        })
        .catch(warning)
}

getSubjects()
    .then(() => {
        render_subject();
    })

eel.init()()
    .then(response => {
        if (response.isLogin) {
            isLogin = true;
            loginedUsername = response.loginedUsername;
            document.getElementById("loginedUsername").innerText = loginedUsername;
            document.getElementById("register_btn").remove();
            document.getElementById("login_btn").remove();
            document.getElementById('create_btn').style.display = 'block';
            postFrame.contentWindow.location.reload();
        }
        if (response.lastViewPost) {
            post_to(response.lastViewPost);
        } else {
            post_init();
        }
    })

function reload() {
    left_init();
    getSubjects()
        .then(() => {
            render_subject();
        })
    postFrame.contentWindow.location.reload();
}

function warning(error) {
    warn_body.innerText = error;
    warn.show();
}