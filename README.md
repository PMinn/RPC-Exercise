# 網路程式設計

## Lab 7 – RPC Exercise


這一份作業請大家以 Remote Procedure Call 撰寫一個討論區。這一個討論區的運作分為 Client 端與 Server 端程式，其主要功能如下：

<ul>
    <li>使用者註冊：每一個使用者要新增討論主題或回覆前皆需先申請一帳號，所有的討論主題及回覆內容都會顯示使用者名稱。</li>
    <li>Client 端：提供一個介面讓使用者可以 (1) 註冊 (2) 新增討論主題 (3) 列出討論主題名稱 (4) 回覆討論議題 (5) 顯示一討論主題的內容及其所有回覆內容 (6) 刪除討論主題。</li>
    <ol>
        <li>註冊時要確認使用者名稱是否重覆；請使用 register() 這一個 API 向 Server 註冊使用者。</li>
        <li>新增討論主題時需分別輸入 (a) 討論主題名稱 及 (b) 討論主題內容；請使用 create() 這一個 API 向 Server 新增討論主題。(PS: 記得要傳給 Server 端使用者名稱。)</li>
        <li>請使用 subject() 這一個 API 向 Server 查詢所有討論主題名稱。</li>
        <li>使用者可以針對某一討論主題回覆其意見；請使用 reply() 這一個 API 向 Server 新增回覆內容。(PS: 記得要傳給 Server 端使用者名稱。)</li>
        <li>請使用 discussion()這一個 API 向 Server 查詢一討論主題的內容及其所有回覆內容。(PS: 記得要顯示發言人的名稱)</li>
        <li>如果一討論主題尚未有回覆或一回覆之後無其它回覆，發言人可使用 delete() API 刪除其討論主題或回覆。</li>
    </ol>
    <li>Server 端：接收 Client 端送來的資訊並將這些資訊儲存在 Server 端（請自行設計儲存格式）。Server 端同時提供 register(), create(), subject(), reply(), discussion() 及 delete() 等 API 供 Client 端程式呼叫以處理資訊。Server 端的程式需滿足以下的要求。</li>
    <ol>
        <li>允許多個 Client 同時存取 Server 端的資訊，Server 程式必須處理臨界區間 (Critical Section) 的問題。</li>
        <li>Server 端接收到討論主題或回覆時需同時儲存日期及時間。</li>
        <li>請自行定義一個 Error 回傳值，當所要求的資訊不存在時回傳 Error。</li>
    </ol>
</ul>