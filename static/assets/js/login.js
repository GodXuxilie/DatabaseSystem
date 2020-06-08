$(document).ready(function () {

   $(".input input").focus(function() {

      $(this).parent(".input").each(function() {
         $("label", this).css({
            "line-height": "18px",
            "font-size": "18px",
            "font-weight": "100",
            "top": "0px"
         })
         $(".spin", this).css({
            "width": "100%"
         })
      });
   }).blur(function() {
      $(".spin").css({
         "width": "0px"
      })
      if ($(this).val() == "") {
         $(this).parent(".input").each(function() {
            $("label", this).css({
               "line-height": "60px",
               "font-size": "24px",
               "font-weight": "300",
               "top": "10px"
            })
         });

      }
   });

   // $(".button").click(function(e) {
   //    var pX = e.pageX,
   //       pY = e.pageY,
   //       oX = parseInt($(this).offset().left),
   //       oY = parseInt($(this).offset().top);
   //
   //    $(this).append('<span class="click-efect x-' + oX + ' y-' + oY + '" style="margin-left:' + (pX - oX) + 'px;margin-top:' + (pY - oY) + 'px;"></span>')
   //    $('.x-' + oX + '.y-' + oY + '').animate({
   //       "width": "500px",
   //       "height": "500px",
   //       "top": "-250px",
   //       "left": "-250px",
   //
   //    }, 600);
   //    $("button", this).addClass('active');
   // })

   function checkUID(uid)
   {
      if(uid===""){alert("请输入UID"); return false}
      var regPos = /^\d+$/;
      if(!regPos.test(uid))
      {
         alert("UID由11位数字组成。您输入的UID中含有非数字字符，请重新输入哦^_^")
         return false
      }
      //if(uid.length!==11){alert("您输入的UID长度不是11位，请重新输入哦^_^"); return false}

      return true
   }

   function checkJobID(jobid)
   {
      if(jobid===""){alert("请输入JobID"); return false}
      var regPos = /^\d+$/;
      if(!regPos.test(jobid))
      {
         alert("JobID由11位数字组成。您输入的JobID中含有非数字字符，请重新输入哦^_^")
         return false
      }
      //if(jobid.length!==11){alert("您输入的JobID长度不是11位，请重新输入哦^_^"); return false}

      return true
   }


   function checkAge(age)
   {
      if(age===""){alert("请输入年龄"); return false}
      var regAgePos = /^[123456789]\d+$/;
      if(!regAgePos.test(age) || parseInt(age)>120 || parseInt(age)<0)
      {
         alert("请输入0-120以内的整数，包括0和120哦*&*");
         return false
      }

      return true
   }


   $("#loginB").click(function(e)
   {
      var uid = $("#loginUID").val();
      var pwd = $("#loginPass").val();
      //alert("uid:"+uid+"\npwd:"+pwd);

      if(!checkUID(uid)) return;

      if(pwd===""){alert("请输入密码"); return}

      $.post("http://127.0.0.1:5000/login",
          {
             username:uid,
             passwd:pwd
          },
          function(data, status)
          {
             //alert("数据："+ data +"\n状态："+status)
             if(status!=="success")
             {
                alert("数据发送失败，请尝试重新登录一次哦^_^");
                return
             }

             if(data==="Not Exist")
             {
                alert("该用户名不存在，请重新输入哦^_^");
                return
             }

             if(data==="fail")
             {
                alert("您输入的密码有误，请重新输入呀@_@");
                return
             }

             if(data==="success")
             {
                //显示登录图标动画
                // var pX = e.pageX,
                //     pY = e.pageY,
                //     oX = parseInt($(this).offset().left),
                //     oY = parseInt($(this).offset().top);
                //
                // $(this).append('<span class="click-efect x-' + oX + ' y-' + oY + '" style="margin-left:' + (pX - oX) + 'px;margin-top:' + (pY - oY) + 'px;"></span>')
                // $('.x-' + oX + '.y-' + oY + '').animate({
                //    "width": "500px",
                //    "height": "500px",
                //     "top": "-250px",
                //     "left": "-250px",
                //      }, 600);
                // $("button", this).addClass('active');
                alert("登录成功！")

                //跳转页面
                location.reload()
             }
          }
          )

      //下面代码仅调试登录用
      // if(uid==="12345678901" && pwd=== "123")
      // {
      //    //显示登录图标动画
      //    var pX = e.pageX,
      //        pY = e.pageY,
      //        oX = parseInt($(this).offset().left),
      //        oY = parseInt($(this).offset().top);
      //
      //    $(this).append('<span class="click-efect x-' + oX + ' y-' + oY + '" style="margin-left:' + (pX - oX) + 'px;margin-top:' + (pY - oY) + 'px;"></span>')
      //    $('.x-' + oX + '.y-' + oY + '').animate({
      //              "width": "500px",
      //              "height": "500px",
      //               "top": "-250px",
      //               "left": "-250px",
      //                }, 600);
      //    $("button", this).addClass('active');
      //    alert("登录成功！")
      //
      //    //跳转页面
      //    // window.location.href("http://127.0.0.1:5000/index")
      // }

   })

   $("#registerButton").click(function()
   {
      var uid =$("#regname").val();
      var pwd = $("#regpass").val();
      var jobid = $("#jobid").val();
      var age = $("#age").val();
      var sex = $("#sex").val();
      var zipCode = $("#zipCode").val();
      var movieType = selectMultip.getVal("movieType")


      if(!checkUID(uid)) return;
      if(pwd===""){alert("请输入密码"); return}
      //if(!checkJobID(jobid)){return}
      //if(!checkAge(age)) return;

       alert('zhangzhiwei');
       $.post("http://127.0.0.1:5000/register",
          {
             username:uid,
             passwd:pwd,
             gender:sex,
             jobid:jobid,
             zipCode:zipCode,
             age:age,
             types:movieType
          },
          function(data, status)
          {
             alert("数据："+ data +"\n状态："+status);
             if(status!=="success")
             {
                alert("数据发送失败，请尝试重新登录一次哦^_^");
                return
             }
            if(data==="invalid")
            {
               alert("注册失败");
               return
            }
            if(data==="invalid")
            {
               alert("密码长度超了，或者username必须是数字但是输入了别的符号，或者类型一个都没选导致传回来的是空list");
               return
            }

             if(data==="Existed")
             {
                alert("该UID已存在，请换个UID注册吧^_^");
                return
             }

             if(data==="tologin")
             {
                alert('hahaha');
                //跳转页面
                location.reload()
             }
          }
          )





   })

   $(".alt-2").click(function() {
      if (!$(this).hasClass('material-button')) {
         $(".shape").css({
            "width": "100%",
            "height": "100%",
            "transform": "rotate(0deg)"
         })

         setTimeout(function() {
            $(".overbox").css({
               "overflow": "initial"
            })
         }, 600);

         $(this).animate({
            "width": "140px",
            "height": "140px"
         }, 500, function() {
            $(".box").removeClass("back");

            $(this).removeClass('active')
         });

         $(".overbox .title").fadeOut(300);
         $(".overbox .input").fadeOut(300);
         $(".overbox .button").fadeOut(300);

         $(".alt-2").addClass('material-buton');
      }

   })

   $(".material-button").click(function() {

      if ($(this).hasClass('material-button')) {
         setTimeout(function() {
            $(".overbox").css({
               "overflow": "hidden"
            })
            $(".box").addClass("back");
         }, 200)
         $(this).addClass('active').animate({
            "width": "1200px",
            "height": "1200px"
         });

         setTimeout(function() {

            if(!$(".alt-2").hasClass('material-buton'))
            {
               $(".shape").css({
               "width": "50%",
               "height": "50%",
               "left":"40%",
               "top":"5%",
               "transform": "rotate(45deg)"
            })
            }

            $(".overbox .title").fadeIn(300);
            $(".overbox .input").fadeIn(300);
            $(".overbox .button").fadeIn(300);
         }, 600)

         $(this).removeClass('material-button');

      }


      if ($(".alt-2").hasClass('material-buton')) {
         $(".alt-2").removeClass('material-buton');
         $(".alt-2").addClass('material-button');
         $(".shape").css({
               "width": "50%",
               "height": "50%",
               "left":"25%",
               "top":"25%"
            })
      }

   });

});