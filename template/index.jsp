<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <style>
        .content {
            width: 100%;
            position: relative;
            margin: 64px 0 64px 0;
        }
        .content-op{
            height: 600px;
            width: 100%;
            opacity: 0.3;
            background-color: #fbd3ad;
            position:relative;
        }
        .content-in {
            top: 0;
            z-index: 999;
            height: 600px;
            width: 100%;
            position: absolute;
        }
        .content-wrap {
            margin: 0 auto;
            text-align: center;
        }
        .content-text {     
            padding: 30px;
            font-size: 30px;
            font-weight: bolder;
        }
        .p-1{
            color:rgb(176, 108, 101);
            margin: 0;
        }
        .p-2{
            color:rgb(112, 97, 97);
        }
        /* .content-button button {
            
            width: 200px;
            height: 200px;
            border-radius: 30px;
            border: 0;
            background-color: white;
        }
        .content-button button:hover {
            color:black;
            background-color: orange;
            transition:background-color 1s;
        }    */
        .btn-3d.yellow {
            background-color: #F0D264;
            box-shadow: 0 0 0 1px #F0D264 inset, 0 0 0 2px rgba(255,255,255,0.15) inset, 0 8px 0 0 rgba(196, 172, 83, .7), 0 8px 0 1px rgba(0,0,0,.4), 0 8px 8px 1px rgba(0,0,0,0.5);
        }
        a[class*="btn"] {
            text-decoration: none;
        }
        .btn-3d {
            position: relative;
            display: inline-block;
            font-size: 22px;
            padding: 20px 60px;
            color: white;
            margin: 20px 10px 10px;
            border-radius: 6px;
            text-align: center;
            transition: top .01s linear;
            text-shadow: 0 1px 0 rgba(0,0,0,0.15);
        }
    </style>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
<div>
    <!-- 헤더 파일 -->
    <div>
        <%@ include file ="header.jsp" %>
    </div>
    <!-- 메인 컨테이너 -->
    <div class="content">
        <div class="content-op" style="background-image: url('../static/image/toy.jpg'); background-size: 100%; background-repeat: no-repeat;">
        </div>
        <div class="content-in">
            <!-- font -->
            <div class="content-wrap">
                <div class="content-text">
                    <p class="p-1">무료로 물건을 이용할 수 있는 정보를 담은 페이지. </p>
                    <p class="p-2">A page containing free access and reservation information.</p>
                </div>
                <!-- button -->
                <div class="btn-container">
                    <a href="#" class="btn-3d yellow">Button</a>
                    <pre>&lt;<span class="anc">a</span> <span class="att">href</span>=<span class="val">"#"</span> <span class="att">class</span>=<span class="val">"btn-3d yellow"</span>>Button&lt;/<span class="anc">a</span>></pre>
                  </div>
            </div>
        </div>
    </div>
    <div>
        <%@ include file ="footer.jsp" %>
    </div>
    <!-- 푸터 파일 -->
</div> 
</body>
</html>
<script src="https://code.jquery.com/jquery-3.6.0.js"></script>
<script>
    $(document).ready(function() {
        $('a').click(function(event) {
            event.preventDefault(); 
        });
    });
</script>