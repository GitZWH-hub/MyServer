/* all tabs */
const myClick = function (v) {
    let i;
    const llis = document.getElementsByTagName("li");
    for (i = 0; i < llis.length; i++) {
        const lli = llis[i];
        if (lli == document.getElementById("tab" + v)) {
            lli.style.color = "#f16060";
            lli.style.fontWeight = 'bold';
            lli.style.borderBottom = '1px solid #ffffff';
            lli.style.borderLeft = lli.style.borderTop = lli.style.borderRight = '1px solid #000000';
            lli.style.borderTopLeftRadius = lli.style.borderTopRightRadius = '5px';
        } else {
            lli.style.color = "#242424";
            lli.style.fontWeight = 'normal';
            lli.style.borderBottom = '1px solid #000000';
            lli.style.borderLeft = lli.style.borderTop = lli.style.borderRight = '1px solid #ffffff';

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

function parentSay(i, msg){
    console.log('收到跳转指令', i, msg);
    callChild(msg)
    myClick(i);
    // 需要将str传递给html5界面
}
function callChild(msg){
    let child = document.getElementById("tab2_child").contentWindow;//获取id为tab5_content的iframe的对象
    child.childSay(msg);//执行子界面中的函数
}


