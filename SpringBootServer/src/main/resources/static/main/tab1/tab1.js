function loadStyle(url) {
    const link = document.createElement('link');
    link.type = 'text/css'
    link.rel = 'stylesheet'
    link.href = url
    const head = document.getElementsByTagName('head')[0];
    head.appendChild(link)
}
function sleep(number){
    var now = new Date();
    var exitTime = now.getTime() + number * 1000;
    while(true){
        now = new Date();
        if(now.getTime() > exitTime)
            return;
    }
}
const loadStock = function(){
    let table_body = document.getElementById('tbody_stock')
    table_body.innerHTML = ''
    let type = document.getElementById('which')
    host = 'http://localhost:8001'
    let post_data = {'code': '8003', 'type': type.value}
    $.ajax({
        type: "POST",
        url: host + "/Req8003",
        contentType: 'application/json',
        timeout: 5000,
        cache: true,
        data: JSON.stringify(post_data),
        dataType: "text",
        success: function (data, status) {
            if (status == 'success') {
                let json = JSON.parse(JSON.parse(data))
                for (let i = 0; i < json.length; i++) {
                    table_body.innerHTML += "<tr>\n" +
                        "        <td align='center'>" + (i+1) + "</td>\n" +
                        "        <td align='center'>" + json[i]['Date'] + "</td>\n" +
                        "        <td align='center'>" + json[i]['IndexName'] + "</td>\n" +
                        "        <td align='center'>" + json[i]['Code'] + "</td>\n" +
                        "        <td align='center'>" + json[i]['Name'] + "</td>\n" +
                        "        <td align='center'>" + json[i]['Exchange'] + "</td>\n" +
                        "        <td align='center'>" + json[i]['weight'] + "</td>\n" +
                        "    </tr>";
                }
            }
        }
    })
    // 刚加载完，添加选中背景（单击事件）
    document.getElementById('tbody_stock').addEventListener('dblclick', function(){
        console.log('en')
        let tr = document.querySelectorAll('tbody tr');
        for(let i = 0; i < tr.length; i++) {
            tr[i].addEventListener('click',function (){
                // 刚加载完，需要添加一个可以获取到行索引的监听（双击事件）
                let ts_code = document.getElementById('table_stock').rows[i + 1].cells[3];
                let stock_name = document.getElementById('table_stock').rows[i + 1].cells[4];
                let msg = {'ts_code': ts_code.innerHTML, 'stock_name': stock_name.innerHTML}
                parent.parentSay(2, msg);
            })
            tr[i].addEventListener('mouseout', function() {
                this.style.backgroundColor = 'white';
            }, false)
            tr[i].addEventListener('mouseover', function() {
                this.style.backgroundColor = '#c5e9ff';
            }, false)
        }
    })


}
