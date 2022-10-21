host = "http://localhost:8001"

/*************** index.html ***************/
// 用户登陆
function login() {
    const login_name = document.getElementById("login_name");
    const password = document.getElementById("password");
    let post_data = {'loginName': login_name.value, 'password': password.value};

    $.ajax({
        type: "POST",
        url: host + "/login",
        contentType : "application/json;charsets=UTF-8",
        timeout: 5000,
        cache: true,
        data: JSON.stringify(post_data),
        dataType: "text",
        success: function (data, status) {
            if (status == 'success') {
                console.log("可以登录");
                window.location = "main/main.html"
            }
        }
    })
};
// 用户注册
function register() {
    const register_name = document.getElementById("register_name");
    const register_pw = document.getElementById("register_pw");
    const name = document.getElementById("name");
    let post_data = {'loginName': register_name.value, 'password': register_pw.value, 'name': name.value};

    $.ajax({
        type: "PUT",
        url: host + "/register",
        contentType : "application/json;charsets=UTF-8",
        timeout: 5000,
        cache: true,
        data: JSON.stringify(post_data),
        dataType: "text",
        success: function (data, status) {
            if (status == 'success') {
                console.log(data)
            }
        }
    })
};

/* all tabs */
const myClick = function (v) {
    let i;
    const llis = document.getElementsByTagName("li");
    for (i = 0; i < llis.length; i++) {
        const lli = llis[i];
        if (lli == document.getElementById("tab" + v)) {
            lli.style.color = "#f16060";
            lli.style.fontWeight = 'bold';
        } else {
            lli.style.color = "#242424";
            lli.style.fontWeight = 'normal';
        }
    }
    const divs = document.getElementsByClassName("tab_css");
    for (i = 0; i < divs.length; i++) {
        const divv = divs[i];
        if (divv == document.getElementById("tab" + v + "_content")) {
            divv.style.display = "block";
        } else {
            divv.style.display = "none";
        }
    }
};

