
$(document).ready(
    function () {

        var t =$("#basic-datatable").DataTable();

        // 调试用
        // var tests = [{"title":"123","genre":"comedy","rank":"98"},{"title":"124","genre":"comedy","rank":"98"}];
        //
        // $("#loadTable").on("click",function()
        // {
        //     alert("删除");
        //     t.clear();
        //     for (var i=0; i<tests.length; i++)
        //     {
        //         t.row.add([tests[i]["title"], tests[i]["genre"], tests[i]["rank"]]);
        //     }
        //     t.draw();
        // });

        $('#loadTable').on("click", function ()
            {
                var ws = new WebSocket('ws://127.0.0.1:5000/list');
                ws.onopen = function (evt)
                {
                    // alert("已经与服务器建立了连接\n当前连接状态是：" + this.readyState);
                    ws.send("请求电影推荐列表")
                };

                $("#wait-img").html("<img src='/static/assets/images/loading.gif' width='50' height='50'  alt=''> 加载中，请耐心等待");

                ws.onmessage = function (evt)
                {
                    if (evt.data === "nothing") {
                alert("未从服务器获得新的推荐电影列表")
            }
                    var jdata = $.parseJSON(evt.data);
                    // alert(evt.data);
                    alert("加载数据完成辣o(*￣︶￣*)o");
                    t.clear();
                    for (var i = 0; i < jdata.length; i++)
                    {
                        t.row.add([jdata[i]["title"], jdata[i]["genre"], jdata[i]["rate"]]);
                    }
                     $("#wait-img").html("");
                    t.draw()
                };

                ws.onclose = function ()
                {
                    // alert("ws连接已关闭")
                }
            }
        )
    }
);

function click_logout()
{
    $.get("http://127.0.0.1:5000/logout", function (data,status)
    {
        if(data==="successful_logout")
        {
            alert("您已经成功登出~下次见哦^_^");
            location.href="http://127.0.0.1:5000"
        }

    })
}