$(document).ready(function() {
    host = 'http://localhost:8001'
    $("#pullData").click(function() {
        const start = document.getElementById("start");
        const end = document.getElementById("end");
        const radio = document.getElementsByName("type")
        const exchange = document.getElementById("exchange")
        let type = "1"
        for(let i = 0; i < radio.length; i++)
            if(radio[i].checked)
                type = radio[i].value
        let post_data = {'code': '8002', 'type': type, 'start': start.value, 'end': end.value, 'exchange': exchange.value};
        $.ajax({
            type: "POST",
            url: host + "/Req8002",
            data: JSON.stringify(post_data),
            contentType : "application/json;charsets=UTF-8",  //发送参数时必须添加此句
            timeout: 5000,
            dataType: 'text',
            success: function (data, status) {
                if (status == 'success') {
                    let p = JSON.parse(data)
                    alert('Pull Succeed!')
                } else {
                    alert('Failed');
                }
            }
        })
    })
})
