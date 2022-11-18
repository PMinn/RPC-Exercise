const title = document.getElementById("title");
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

var editorTitle = new EditorJS({
    holder: "title",
    tools: {
        header: Header
    },
    minHeight: 30,
    defaultBlock: 'header',
    placeholder: '標題'
});


var editorBody = new EditorJS({
    holder: "content",
    tools: EDITOR_JS_TOOLS,
    i18n: i18n,
    placeholder: '內文',
    onReady: () => {
        new DragDrop(editorBody);
    }
});

function save() {
    var data = [editorTitle.save(), editorBody.save()]
    return Promise.all(data);
}

function clear() {
    editorTitle.blocks.clear()
    editorBody.blocks.clear()
}