$(document).ready(function() {
    host = 'http://localhost:8001'
    $("#send").click(function() {
        const start = document.getElementById("start");
        const end = document.getElementById("end");
        // 传数组
        let SHFE = []
        const SHFECheckbox = $("input[name='SHFEcheck']");
        for (let i = 0; i < SHFECheckbox.length; i++)
            if(SHFECheckbox[i].checked)
                SHFE.push(SHFECheckbox[i].value);
        let CZCE = []
        const CZCECheckbox = $("input[name='CZCEcheck']");
        for (let i = 0; i < CZCECheckbox.length; i++)
            if(CZCECheckbox[i].checked)
                CZCE.push(CZCECheckbox[i].value);
        let DCE = []
        const DCECheckbox = $("input[name='DCEcheck']");
        for (let i = 0; i < DCECheckbox.length; i++)
            if(DCECheckbox[i].checked)
                DCE.push(DCECheckbox[i].value);
        let post_data = {'code': '8001', 'SHFE': SHFE, 'CZCE': CZCE, 'DCE': DCE, 'start': start.value, 'end': end.value};
        console.log(post_data)
        document.getElementById("div_result").innerHTML = "" +
            "<table class=\"tb\" id=\"cluster\">" +
            "<th class='th1' class='th2'>序号</th>" +
            "<th class='th1'>合约品种</th>" +
            "</table>";
        $.ajax({
            type: "POST",
            url: host + "/Req8001",
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
