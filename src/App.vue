<script setup>
import { ref } from 'vue';

const logemail = ref('');
const logpass = ref('');
const regname = ref('');
const regemail = ref('');
const regpass = ref('');
const errorMessageLogIn = ref('');
const errorMessage = ref('');
const infoMessage = ref('');
const infoMessageLogIn = ref('');

const APIurl = 'https://jsonplaceholder.typicode.com/users'
const ServerUrl = 'http://127.0.0.1:5000'

const collectDataLogIn = () => {
  // Собираем данные из полей
  if (!logemail.value || !logpass.value) {
    errorMessageLogIn.value = "Укажите логин и пароль";
    return NaN
  }
  const formData = new FormData();
  formData.set('email', logemail.value);
  formData.set('password', logpass.value);
  errorMessageLogIn.value = '';
  infoMessage.value = '';
  formData.forEach((value, key) => {
    console.log(`${key}: ${value}`);
  });
  return formData
}

const collectDataRegister = () => {
  // Проверяем, что все поля заполнены
  if (!regemail.value || !regname.value || !regpass.value) {
    errorMessage.value = 'Все поля должны быть заполнены';
    return null;
  }

  // Собираем данные из полей
  const formData = new FormData();
  formData.set('email', regemail.value);
  formData.set('password', regpass.value);
  formData.set('name', regname.value);
  errorMessage.value = '';
  infoMessage.value = '';
  formData.forEach((value, key) => {
    console.log(`${key}: ${value}`);
  });
  return formData;
}

async function sendPOSTRequestLogIn() {
  const formData = collectDataLogIn();
  if (formData) {
    const page = '/login';
    const url = `${ServerUrl}${page}`;
    console.log(url);
    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        if (response.status === 404) {
          errorMessageLogIn.value = 'User not found';
        } else if (response.status === 401) {
          errorMessageLogIn.value = 'Invalid credentials';
        } else {
          throw new Error('Ошибка при загрузке данных сервера');
        }
        return; // Добавлено, чтобы выйти из функции после обработки ошибки
      }

      const data = await response.json();

      if (!data.success) {
        console.log(data.message);
        errorMessageLogIn.value = data.message;
        return; // Добавлено, чтобы выйти из функции после обработки ошибки
      }
      console.log(data.user)
      console.log(`Данные с сервера:\n`, data.message, ' - ', data.success);
      console.log('id пользователя', data.user.id);
      console.log('name', data.user.name);
      console.log('email', data.user.email);
      // console.log('phone', data.user[0].phone);

      const textInfo = `User name: ${data.user.name}<br>Email: ${data.user.email}`;
      infoMessageLogIn.value = textInfo;

    } catch (error) {
      if (error.message === 'Failed to fetch') {
        errorMessageLogIn.value = 'Ошибка сети: не удается подключиться к серверу';
      } else {
        errorMessageLogIn.value = 'Ошибка при получении данных: ' + error.message;
      }
      console.error('Ошибка при получении данных:', error);
    }
  }
}


async function sendPOSTRequestRegister() {
  const formData = collectDataRegister()
  if (formData) {
    const page = '/register';
    const url = `${ServerUrl}${page}`;
    console.log(url);
    try {
      const response = await fetch(url, {
        method: 'POST',

        body: formData
      });
      console.log(response.body)
      if (!response.ok) {
        if (response.status === 409) {
          errorMessage.value = 'Пользователь с указанным email существует\nПерейдите в форму LogIn';
        } if (response.status === 400) {
          errorMessage.value = response.message
        }
        throw new Error(`Ошибка при сохранении данных на сервер ${response.status}`);
      }
      const data = await response.json(); // Преобразование ответа в JSON формат
      console.log(`Данные сервера:\n${JSON.stringify(data, null, 2)}`);
      infoMessage.value = data.message

    } catch (error) {
      console.error('Ошибка при получении данных:', error);
    }
  }
}

async function getDataAllUser() {
  // Выполняет запрос GET на
  const name = 'Ervin Howell'
  const response = await fetch(`${APIurl}`);
  const data = await response.json()

  if (!response.ok) {
    console.log("Ошибка получения данных", response.json())
  }

  console.log("Data the all users", data);
}

async function getDataUser() {
  const email = logemail.value;
  const password = logpass.value;
  const response = await fetch(`${APIurl}/?email=${email}&zipcode=${password}`);
  const data = await response.json();
  if (!response.ok) {
    console.log("Ошибка получения данных", response.json())
  }

  data.length ? console.log(`Data the current user\n${JSON.stringify(data, null, 2)}`) : console.info('No data!!!');
}

</script>

<template>
  <a href="https://front.codes/" class="logo" target="_blank">
    <img src="https://assets.codepen.io/1462889/fcy.png" alt="">
  </a>

  <div class="section">
    <div class="container">
      <div class="row full-height justify-content-center">
        <div class="col-12 text-center align-self-center py-5">
          <div class="section pb-5 pt-5 pt-sm-2 text-center">
            <h6 class="mb-0 pb-3"><span>Log In </span><span>Sign Up</span></h6>
            <input class="checkbox" type="checkbox" id="reg-log" name="reg-log" />
            <label for="reg-log"></label>
            <div class="card-3d-wrap mx-auto">
              <div class="card-3d-wrapper">
                <div class="card-front">
                  <div class="center-wrap">
                    <div class="section text-center">
                      <h4 class="mb-4 pb-3">Log In</h4>
                      <div class="form-group">
                        <input type="email" v-model="logemail" class="form-style" placeholder="Your Email" id="logemail"
                          autocomplete="off">
                        <i class="input-icon uil uil-at"></i>
                      </div>
                      <div class="form-group mt-2">
                        <input type="password" v-model="logpass" class="form-style" placeholder="Your Password"
                          id="logpass" autocomplete="off">
                        <i class="input-icon uil uil-lock-alt"></i>
                      </div>
                      <a href="#" class="btn mt-4" @click="sendPOSTRequestLogIn">submit</a>
                      <p class="error-message" v-if="errorMessageLogIn">{{ errorMessageLogIn }}</p>
                      <!-- Добавлено для отображения сообщения об ошибке -->
                      <p class="info-message" v-if="infoMessageLogIn">{{ infoMessageLogIn }}</p>
                      <!-- Добавлено для отображения сообщения о пользователе -->
                      <p class="mb-0 mt-4 text-center"><a href="#0" class="link">Forgot your password?</a></p>
                    </div>
                  </div>
                </div>
                <div class="card-back">
                  <div class="center-wrap">
                    <div class="section text-center">
                      <h4 class="mb-4 pb-3">Sign Up</h4>
                      <div class="form-group">
                        <input type="text" v-model="regname" class="form-style" placeholder="Your Full Name"
                          id="regname" autocomplete="off">
                        <i class="input-icon uil uil-user"></i>
                      </div>
                      <div class="form-group mt-2">
                        <input type="email" v-model="regemail" class="form-style" placeholder="Your Email" id="regemail"
                          autocomplete="off">
                        <i class="input-icon uil uil-at"></i>
                      </div>
                      <div class="form-group mt-2">
                        <input type="password" v-model="regpass" class="form-style" placeholder="Your Password"
                          id="regpass" autocomplete="off">
                        <i class="input-icon uil uil-lock-alt"></i>
                      </div>
                      <a href="#" class="btn mt-4" @click="sendPOSTRequestRegister">submit</a>
                      <p class="error-message" v-if="errorMessage">{{ errorMessage }}</p>
                      <!-- Добавлено для отображения сообщения об ошибке -->
                      <p class="info-message" v-if="infoMessage" v-html="infoMessage"></p>
                      <!-- Добавлено для отображения сообщения о пользователе -->
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
/* Please ❤ this if you like it! */

@import url("https://fonts.googleapis.com/css?family=Poppins:400,500,600,700,800,900");

body {
  font-family: "Poppins", sans-serif;
  font-weight: 300;
  font-size: 15px;
  line-height: 1.7;
  color: #c4c3ca;
  background-color: #1f2029;
  overflow-x: hidden;
}

a {
  cursor: pointer;
  transition: all 200ms linear;
}

a:hover {
  text-decoration: none;
}

.link {
  color: #c4c3ca;
}

.link:hover {
  color: #ffeba7;
}

p {
  font-weight: 500;
  font-size: 14px;
  line-height: 1.7;
}

h4 {
  font-weight: 600;
}

h6 span {
  padding: 0 20px;
  text-transform: uppercase;
  font-weight: 700;
}

.section {
  position: relative;
  width: 100%;
  display: block;
}

.full-height {
  min-height: 100vh;
}

[type="checkbox"]:checked,
[type="checkbox"]:not(:checked) {
  position: absolute;
  left: -9999px;
}

.checkbox:checked+label,
.checkbox:not(:checked)+label {
  position: relative;
  display: block;
  text-align: center;
  width: 60px;
  height: 16px;
  border-radius: 8px;
  padding: 0;
  margin: 10px auto;
  cursor: pointer;
  background-color: #ffeba7;
}

.checkbox:checked+label:before,
.checkbox:not(:checked)+label:before {
  position: absolute;
  display: block;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  color: #ffeba7;
  background-color: #102770;
  font-family: "unicons";
  content: "\eb4f";
  z-index: 20;
  top: -10px;
  left: -10px;
  line-height: 36px;
  text-align: center;
  font-size: 24px;
  transition: all 0.5s ease;
}

.checkbox:checked+label:before {
  transform: translateX(44px) rotate(-270deg);
}

.card-3d-wrap {
  position: relative;
  width: 440px;
  max-width: 100%;
  height: 400px;
  -webkit-transform-style: preserve-3d;
  transform-style: preserve-3d;
  perspective: 800px;
  margin-top: 60px;
}

.card-3d-wrapper {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  -webkit-transform-style: preserve-3d;
  transform-style: preserve-3d;
  transition: all 600ms ease-out;
}

.card-front,
.card-back {
  width: 100%;
  height: 100%;
  background-color: #2a2b38;
  background-image: url("https://s3-us-west-2.amazonaws.com/s.cdpn.io/1462889/pat.svg");
  background-position: bottom center;
  background-repeat: no-repeat;
  background-size: 300%;
  position: absolute;
  border-radius: 6px;
  left: 0;
  top: 0;
  -webkit-transform-style: preserve-3d;
  transform-style: preserve-3d;
  -webkit-backface-visibility: hidden;
  -moz-backface-visibility: hidden;
  -o-backface-visibility: hidden;
  backface-visibility: hidden;
}

.card-back {
  transform: rotateY(180deg);
}

.checkbox:checked~.card-3d-wrap .card-3d-wrapper {
  transform: rotateY(180deg);
}

.center-wrap {
  position: absolute;
  width: 100%;
  padding: 0 35px;
  top: 50%;
  left: 0;
  transform: translate3d(0, -50%, 35px) perspective(100px);
  z-index: 20;
  display: block;
}

.form-group {
  position: relative;
  display: block;
  margin: 0;
  padding: 0;
}

.form-style {
  padding: 13px 20px;
  padding-left: 55px;
  height: 48px;
  width: 100%;
  font-weight: 500;
  border-radius: 4px;
  font-size: 14px;
  line-height: 22px;
  letter-spacing: 0.5px;
  outline: none;
  color: #c4c3ca;
  background-color: #1f2029;
  border: none;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
  box-shadow: 0 4px 8px 0 rgba(21, 21, 21, 0.2);
}

.form-style:focus,
.form-style:active {
  border: none;
  outline: none;
  box-shadow: 0 4px 8px 0 rgba(21, 21, 21, 0.2);
}

.input-icon {
  position: absolute;
  top: 0;
  left: 18px;
  height: 48px;
  font-size: 24px;
  line-height: 48px;
  text-align: left;
  color: #ffeba7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:-ms-input-placeholder {
  color: #c4c3ca;
  opacity: 0.7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input::-moz-placeholder {
  color: #c4c3ca;
  opacity: 0.7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:-moz-placeholder {
  color: #c4c3ca;
  opacity: 0.7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input::-webkit-input-placeholder {
  color: #c4c3ca;
  opacity: 0.7;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:focus:-ms-input-placeholder {
  opacity: 0;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:focus::-moz-placeholder {
  opacity: 0;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:focus:-moz-placeholder {
  opacity: 0;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.form-group input:focus::-webkit-input-placeholder {
  opacity: 0;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
}

.btn {
  border-radius: 4px;
  height: 44px;
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  -webkit-transition: all 200ms linear;
  transition: all 200ms linear;
  padding: 0 30px;
  letter-spacing: 1px;
  display: -webkit-inline-flex;
  display: -ms-inline-flexbox;
  display: inline-flex;
  -webkit-align-items: center;
  -moz-align-items: center;
  -ms-align-items: center;
  align-items: center;
  -webkit-justify-content: center;
  -moz-justify-content: center;
  -ms-justify-content: center;
  justify-content: center;
  -ms-flex-pack: center;
  text-align: center;
  border: none;
  background-color: #ffeba7;
  color: #102770;
  box-shadow: 0 8px 24px 0 rgba(255, 235, 167, 0.2);
}

.btn:active,
.btn:focus {
  background-color: #102770;
  color: #ffeba7;
  box-shadow: 0 8px 24px 0 rgba(16, 39, 112, 0.2);
}

.btn:hover {
  background-color: #102770;
  color: #ffeba7;
  box-shadow: 0 8px 24px 0 rgba(16, 39, 112, 0.2);
}

.logo {
  position: absolute;
  top: 30px;
  right: 30px;
  display: block;
  z-index: 100;
  transition: all 250ms linear;
}

.logo img {
  height: 26px;
  width: auto;
  display: block;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}

.info-message {
  color: rgb(64, 174, 224);
  font-size: 14px;
  margin-top: 10px;
}
</style>
