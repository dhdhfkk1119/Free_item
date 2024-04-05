<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <style>
        .content {
            width: 100%;
            position: relative;
            margin: 60px 0 60px 0;
        }
        .content-op{
            height: 600px;
            width: 100%;
            background-image: url("../static/image/background.jpg");
            background-size: 500px 500px;
            background-repeat: no-repeat;
            opacity: 0.3;
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
            color:white;
            font-weight: bolder;
        }
        .content-button button {
            
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
        <div class="content-op">
        </div>
        <div class="content-in">
            <!-- font -->
            <div class="content-wrap">
                <div class="content-text">
                    <p>무료로 물건을 이용할 수 있는 정보를 담은 페이지. </p>
                    <p>a page containing free access and reservation information.</p>
                </div>
                <!-- button -->
                <div class="content-button">
                    <a href="info.jsp"><button>장난감</button></a>
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
