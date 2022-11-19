const main = document.getElementById("main");
const nameDOM = document.getElementById("name");
const title = document.getElementById("title");
const replyDOM = document.getElementById("reply");
const create_btn = document.getElementById("create_btn");
const time = document.getElementById("time");

if (location.search.startsWith('?id=')) {
    const id = parseInt(location.search.replace("?id=", ""));
    eel.discussion(id)()
        .then(response => {
            if (response.code < 200 || response.code >= 300) return Promise.reject(response.text);
            response = JSON.parse(response.text);
            console.log(response);
            nameDOM.innerText = response.owneUsername + ':';
            time.innerText = new Date(response.time * 1000).toLocaleString();
            const EDITOR_JS_TOOLS = {
                embed: Embed,
                table: Table,
                marker: Marker,
                list: List,
                warning: Warning,
                code: CodeTool,
                image: SimpleImage,
                raw: RawTool,
                header: Header,
                checklist: Checklist,
                delimiter: Delimiter,
                inlineCode: InlineCode,
                underline: Underline
            };

            new EditorJS({
                holder: "title",
                tools: {
                    header: Header
                },
                minHeight: 30,
                defaultBlock: 'header',
                placeholder: '標題',
                readOnly: true,
                data: { "blocks": response.topic }
            });

            new EditorJS({
                holder: "content",
                tools: EDITOR_JS_TOOLS,
                readOnly: true,
                data: { "blocks": response.content }
            });

            response.reply.forEach(reply => {
                console.log(reply)
                var outer = document.createElement("div");
                var name = document.createElement("div");
                var time = document.createElement("div");
                time.classList.add("time");
                time.innerText = new Date(reply.time * 1000).toLocaleString();
                var hr = document.createElement("hr");
                name.classList.add("username");
                name.innerText = reply.owneUsername + ':';
                var inner = document.createElement("div");
                inner.id = `reply_${reply.id}`;
                outer.appendChild(name);
                outer.appendChild(inner);
                outer.appendChild(time);
                replyDOM.appendChild(outer);
                replyDOM.appendChild(hr);
                new EditorJS({
                    holder: `reply_${reply.id}`,
                    tools: EDITOR_JS_TOOLS,
                    readOnly: true,
                    data: { "blocks": reply.content }
                });
                if (window.parent.loginedUsername == reply.owneUsername) {
                    var delete_btn = create_delete({
                        type: 'reply',
                        postId: response.id,
                        replyId: reply.id
                    });
                    outer.appendChild(delete_btn);
                }
            });

            if (window.parent.isLogin) {
                document.querySelector(".editor-group ").style.display = "block";
                var editorEditor = new EditorJS({
                    holder: "editor",
                    tools: EDITOR_JS_TOOLS,
                    i18n: i18n,
                    placeholder: '新增回覆內容',
                    onReady: () => {
                        new DragDrop(editorEditor);
                    }
                });
                if (window.parent.loginedUsername == response.owneUsername) {
                    var delete_btn = create_delete({
                        type: 'post',
                        postId: response.id
                    });
                    main.appendChild(delete_btn);
                }
            }

            create_btn.addEventListener('click', () => {
                editorEditor.save()
                    .then(savedata => {
                        eel.reply(id, savedata.blocks)()
                            .then(response => {
                                window.parent.reload();
                            });
                    })
            })
        })
        .catch(error => {
            window.parent.post_init();
        })

    function create_delete(option) {
        var outer = document.createElement('div');
        outer.classList.add("align-right");
        outer.innerHTML = `<svg class="delete-btn" onclick="delete_postOrReply('${JSON.stringify(option).replaceAll('"', '\\\'')}')" width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M11.1 3C11.1 2.17157 11.7716 1.5 12.6 1.5H23.4C24.2284 1.5 24.9 2.17157 24.9 3C24.9 3.82843 24.2284 4.5 23.4 4.5H12.6C11.7716 4.5 11.1 3.82843 11.1 3ZM1.5 8.4C1.5 7.57157 2.17157 6.9 3 6.9H33C33.8284 6.9 34.5 7.57157 34.5 8.4C34.5 9.22843 33.8284 9.9 33 9.9H30.9V27.6C30.9 31.4284 27.8284 34.5 24 34.5H12C8.14476 34.5 5.09999 31.4014 5.09999 27.45V9.9H3C2.17157 9.9 1.5 9.22843 1.5 8.4ZM8.09999 9.9V27.45C8.09999 29.7986 9.85523 31.5 12 31.5H24C26.1716 31.5 27.9 29.7716 27.9 27.6V9.9H8.09999ZM13.95 13.8C14.7784 13.8 15.45 14.4716 15.45 15.3V26.25C15.45 27.0784 14.7784 27.75 13.95 27.75C13.1216 27.75 12.45 27.0784 12.45 26.25V15.3C12.45 14.4716 13.1216 13.8 13.95 13.8ZM22.05 13.8C22.8784 13.8 23.55 14.4716 23.55 15.3V26.25C23.55 27.0784 22.8784 27.75 22.05 27.75C21.2216 27.75 20.55 27.0784 20.55 26.25V15.3C20.55 14.4716 21.2216 13.8 22.05 13.8Z" fill="black"/></svg>`;
        return outer;
    }
}

function delete_postOrReply(option) {
    option = JSON.parse(option.replaceAll("'", "\""));
    window.parent.delete_check_body.innerText = `確定要刪除${option.type == 'post' ? '討論' : '回應'}嗎?`;
    window.parent.delete_check.show();
    window.parent.delete_check_btn.onclick = () => {
        eel.delete(option)()
            .then(response => {
                window.parent.delete_check.hide();
                window.parent.reload();
            });
    }
}
