
//=========================================
//HTML + CSS + JavaScript codes for webpage
//=========================================
const char webpageCode[] =
R"=====(
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
<title>TRANG ĐĂNG NHẬP</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'poppins',sans-serif;
}

body {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-image: url(https://user-images.githubusercontent.com/13468728/233847739-219cb494-c265-4554-820a-bd3424c59065.jpg);
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
}

section {
    position: relative;
    max-width: 400px;
    background-color: transparent;
    border: 2px solid rgba(255, 255, 255, 0.5);
    border-radius: 20px;
    backdrop-filter: blur(55px);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem 3rem;
}

h1 {
    font-size: 2rem;
    color: #fff;
    text-align: center;
}

.inputbox {
    position: relative;
    margin: 30px 0;
    max-width: 310px;
    border-bottom: 2px solid #fff;
}

.inputbox label {
    position: absolute;
    top: 50%;
    left: 5px;
    transform: translateY(-50%);
    color: #fff;
    font-size: 1rem;
    pointer-events: none;
    transition: all 0.5s ease-in-out;
}

input:focus ~ label,
input:valid ~ label {
    top: -5px;
}

.inputbox input {
    width: 100%;
    height: 60px;
    background: transparent;
    border: none;
    outline: none;
    font-size: 1rem;
    padding: 0 35px 0 5px;
    color: #fff;
}

.inputbox ion-icon {
    position: absolute;
    right: 8px;
    color: #fff;
    font-size: 1.2rem;
    top: 20px;
}

.forget {
    margin: 35px 0;
    font-size: 0.85rem;
    color: #fff;
    display: flex;
    justify-content: space-between;

}

.forget label {
    display: flex;
    align-items: center;
}

.forget label input {
    margin-right: 3px;
}

.forget a {
    color: #fff;
    text-decoration: none;
    font-weight: 600;
}

.forget a:hover {
    text-decoration: underline;
}

button {
    width: 100%;
    height: 40px;
    border-radius: 40px;
    background-color: rgb(255, 255,255, 1);
    border: none;
    outline: none;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    transition: all 0.4s ease;
}

button:hover {
  background-color: rgb(255, 255,255, 0.5);
}

.register {
    font-size: 0.9rem;
    color: #fff;
    text-align: center;
    margin: 25px 0 10px;
}

.register p a {
    text-decoration: none;
    color: #fff;
    font-weight: 600;
}

.register p a:hover {
    text-decoration: underline;
}
</style>
<body>
    <section>
        <form action="/login_page" method="GET" onsubmit="submitForm(event)">
            <h1>Login</h1>
            <div class= "inputbox">
                <ion-icon name="mail-outline"></ion-icon>
                <input type="text" name="username" id="username"  required>
                <label >ROOM-ID</label>
            </div>
            <div class="inputbox">
                <ion-icon name="lock-closed-outline"></ion-icon>
                <input type="password" name="password" id="password"  required>
                <label >Password</label>
            </div>
            <button id="login-btn">Log in</button>
        </form>
    </section>
</body>
</html>
)=====";


const char admin[] =
R"=====(
  <!DOCTYPE html>
<html>
<head>
  <script src="https://kit.fontawesome.com/a7e9f794eb.js" crossorigin="anonymous"></script>
<style>

.container {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: linear-gradient(to right, #e9e4f0, #d3cce3);
}


.item1 { grid-area: header;
  width:100%;
      background-color: #524a4a;
      padding: 10px;
      text-align: center;
      font-size: 20px;
      color:#ffffff
 }
.item3 { grid-area: main; padding: 20px;}
.item4 { grid-area: right; }
.item5 { grid-area: footer; text-align: center;}

.grid-container {
  display: grid;
  grid-template-areas:
    'header header header header'
    'main main right right'
    'footer footer footer footer';
  gap: 20px;
}

.btn2_container {
  border-color: #fff;
  background-color: #fff;
  box-shadow: -1px 3px 22px 0px rgba(255, 255, 255, 0.75);
  height: 66px;
  width: 200px;
  position: relative;
  padding: 10px;
  border-radius: 5px;
}
.two {
  height: 40px;
  width: 40px;
  background-color: rgba(255, 0, 0, 1);
  position: absolute;
  left: 10px;
  transition: all 300ms cubic-bezier(0, 1.2, 0.79, 1.06);
  border: 1px solid red;
  border-radius: 5px;
  z-index: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 3px;
}

.icon {
  font-size: 30px;
  padding: 5px;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: rgba(255, 255, 255, 1);
  transition: all 300ms cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.chgColor {
  color: #fff;
  padding-left: 0px;
}

.move {
  background-color: green;
  left: 140px;
  border: 1px solid green;
}
.containerColumn
{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.text_box
{
  border-color: #fff;
  background-color: #fff;
  box-shadow: -1px 3px 22px 0px rgba(255, 255, 255, 0.75);
  height: 30px;
  width: 200px;
  position: relative;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  font-size: 20px;
  font-weight: bold;
  display: flex; /* Sử dụng mô hình bố cục Flexbox cho phần tử. */
  flex-direction: column; /* Sắp xếp các phần tử con theo cột dọc (từ trên xuống dưới). */
  justify-content: center; /* Canh giữa các phần tử con theo chiều dọc. */
  align-items: center;
  border: 2px solid #000000;
}

.button {
  background-color: #04AA6D; /* Green */
  border: none;
  color: white;
  padding: 16px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  transition-duration: 0.4s;
  cursor: pointer;
}

.button2 {
  background-color: white; 
  color: black; 
  border: 2px solid #008CBA;
  font-weight: bold;
  border-radius: 10px;
}

.button2:hover {
  background-color: #008CBA;
  color: white;
  border-radius: 10px;
}

/* .grid-container > div {
  background-color: rgba(255, 255, 255, 0.8);
  text-align: center;
  padding: 20px 0;
  font-size: 30px;
} */
</style>
</head>
<body>
<div class="container">
  <div class="grid-container">
    <div class="item1"><h1>WELCOME  BOSS</h1></div>
    <div class="item3">
      <div class="containerColumn">
        <div class="text_box">
          <p>OPEN/CLOSE DOOR</p>
        </div>
        <div class="btn2_container">
          <span class="two">
            <i class="fas fa-times icon"></i>
          </span>
        </div>  
      </div>
    </div>
    <div class="item4">
      <button class="button button2" style="margin-top:100px;" onclick="setPer()">SET PERMISSION</button>
    </div>
    <div class="item5">
      <div class="video-block">
        <h2>Camera An Ninh</h2>
        <img alt="Video stream" src='http://192.168.1.26/mjpeg/1'>
      </div>
    </div>  
  </div>
</div>
<script>
  const btn2_ctn = document.querySelector(".btn2_container");
  const two = document.querySelector(".two");
  const check = document.querySelector(".icon");
  btn2_ctn.addEventListener("click", () => {
    check.classList.toggle("chgColor");
    two.classList.toggle("move");
    check.classList.toggle("fa-check");
    check.classList.toggle("fa-times");
  });

  function setPer()
  {
    location.href = '/setPermission';
  }
  </script>
</body>
</html>
)=====";

const char setPer[] =
R"=====(
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
<title>THÊM QUYỀN TRUY CẬP</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'poppins',sans-serif;
}

body {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-image: url('./lockBackground.jpg');
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
}

section {
    position: relative;
    max-width: 400px;
    background-color: transparent;
    border: 2px solid rgba(255, 255, 255, 0.5);
    border-radius: 20px;
    backdrop-filter: blur(55px);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem 3rem;
}

h1 {
    font-size: 2rem;
    color: #fff;
    text-align: center;
}

.inputbox {
    position: relative;
    margin: 30px 0;
    max-width: 310px;
    border-bottom: 2px solid #fff;
}

.inputbox label {
    position: absolute;
    top: 50%;
    left: 5px;
    transform: translateY(-50%);
    color: #fff;
    font-size: 1rem;
    pointer-events: none;
    transition: all 0.5s ease-in-out;
}

input:focus ~ label,
input:valid ~ label {
    top: -5px;
}

.inputbox input {
    width: 100%;
    height: 60px;
    background: transparent;
    border: none;
    outline: none;
    font-size: 1rem;
    padding: 0 35px 0 5px;
    color: #fff;
}

.inputbox ion-icon {
    position: absolute;
    right: 8px;
    color: #fff;
    font-size: 1.2rem;
    top: 20px;
}

.forget {
    margin: 35px 0;
    font-size: 0.85rem;
    color: #fff;
    display: flex;
    justify-content: space-between;

}

.forget label {
    display: flex;
    align-items: center;
}

.forget label input {
    margin-right: 3px;
}

.forget a {
    color: #fff;
    text-decoration: none;
    font-weight: 600;
}

.forget a:hover {
    text-decoration: underline;
}

button {
    width: 100%;
    height: 40px;
    border-radius: 40px;
    background-color: rgb(255, 255,255, 1);
    border: none;
    outline: none;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    transition: all 0.4s ease;
}

button:hover {
  background-color: rgb(255, 255,255, 0.5);
}

.register {
    font-size: 0.9rem;
    color: #fff;
    text-align: center;
    margin: 25px 0 10px;
}

.register p a {
    text-decoration: none;
    color: #fff;
    font-weight: 600;
}

.register p a:hover {
    text-decoration: underline;
}

</style>
<body>
    <section>
        <form action="/handleSign" method="GET" onsubmit="submitForm(event)">
            <h1>SET PERMISSION</h1>
            <div class= "inputbox">
                <ion-icon name="mail-outline"></ion-icon>
                <input type="text" name="username" id="username" required>
                <label>USERNAME</label>
            </div>

            <div class="inputbox">
                <ion-icon name="lock-closed-outline"></ion-icon>
                <input type="password" name="password" id="password" required>
                <label >Password</label>
            </div>
            <button id="login-btn">Log in</button>
        </form>
    </section>
</body>
</html>
)=====";
