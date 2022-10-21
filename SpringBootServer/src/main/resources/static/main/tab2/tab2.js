let host = "ws://localhost:8001/ws";

let socket;
function Connect(host){
    try{
        let client = new WebSocket(host);
        client.onopen = sOpen;
        client.onerror = sError;
        client.onmessage = sMessage;
        client.onclose = sClose;
        socket = client;
    }catch(e){
        return;
    }
}
function sOpen(){
    console.log('connect success!');
}
function sError(e){
    // alert("error " + e);
}
function sMessage(msg) {
    console.log('hahah')
    doReceive(msg.data);
}
function sClose(e){
    // alert("connect closed:" + e.code);
}
function Send(post_data){
    console.log(post_data);
    socket.send(JSON.stringify(post_data));
}
function Close() {
    socket.close();
}
function doReceive(buffer) {
    console.log("doReceive:");
    console.log(buffer)
    let msg = JSON.parse(buffer)
    if(msg.if_get == '1') {
        path = 'data_html/' + msg.ts_code + '.html'
        document.getElementById('result').innerHTML =
            '<iframe align="center" width="100%" height="100%" ' + 'src=' + path + ' frameBorder="no" marginWidth="0" scrolling="no"></iframe>'
    }
}

/* 父界面main向该界面发送msg */
function childSay(msg){
    console.log('收到请求消息', msg.ts_code)
    let ts_code_show = document.getElementById('ts_code');
    ts_code_show.value = msg.ts_code;
    // 发送服务器，等待服务器返回数据
    send(msg.ts_code)
}
/* 发送Button事件send*/
const send = function (ts_code=null){
    let start = document.getElementById('start');
    let end = document.getElementById('end');
    if(ts_code == null)
        ts_code = document.getElementById('ts_code').value;
    console.log(ts_code)
    let post_data = {'code': '9000', 'ts_code': ts_code, 'start': start.value, 'end': end.value};
    Send(post_data);
}
window.onload = function (){
    Connect(host);
}

