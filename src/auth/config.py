import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_DAYS = os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS")


EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

EMAIL_SENDER = "anton234567894@gmail.com"
BODY_FOR_CONFIRM_EMAIL = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Verification</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
            }}

            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}

            .logo {{
                text-align: left;
                margin-bottom: 20px;
            }}

            .logo img {{
                max-width: 50px;
                height: auto;
            }}

            .message {{
                text-align: left;
                margin-bottom: 20px;
            }}

            .message p {{
                margin-bottom: 10px;
            }}

            .button {{
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                text-decoration: none;
                background-color: #6495ED;
                border-radius: 5px;
            }}
 
            .button-container a {{
                color: #fff;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">
                <img src="https://i.postimg.cc/zGN1NQq0/circle-9524788.png" alt="Company Logo">
            </div>
            <div class="message">
                <p>Дорогой пользователь,</p>
                <p>Благодарим вас за регистрацию в сервисе Swiper! Мы ценим ваш выбор и рады приветствовать вас в нашем сообществе.</p>
                <p>Чтобы подтвердить вашу регистрацию и активировать ваш аккаунт, пожалуйста,
                    нажмите на кнопку 'Подтвердить' или перейдите по следующей ссылке: http://127.0.0.1:8000/auth/verify_email/?user_id={}</p>
            </div>
            <div class="button-container" align="center">
                <a class="button" href="http://127.0.0.1:8000/auth/verify_email/?user_id={}">Подтвердить мой аккаунт</a>
            </div>
            <div class="message">
                <p>Спасибо, что выбрали Swiper! Мы уверены, что ваш опыт использования нашего сервиса будет приятным и полезным.</p>
                <p>С уважением,<br>Команда Swiper</p>
            </div>
        </div>
    </body>
    </html>
    """

BODY_FOR_RESET_PASSWORD = """ 
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="x-ua-compatible" content="ie=edge">
  <title>Password Reset</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style type="text/css">
    /**
   * Google webfonts. Recommended to include the .woff version for cross-client compatibility.
   */
    @media screen {{
      @font-face {{
        font-family: 'Source Sans Pro';
        font-style: normal;
        font-weight: 400;
        src: local('Source Sans Pro Regular'), local('SourceSansPro-Regular'), url(https://fonts.gstatic.com/s/sourcesanspro/v10/ODelI1aHBYDBqgeIAH2zlBM0YzuT7MdOe03otPbuUS0.woff) format('woff');
      }}

      @font-face {{
        font-family: 'Source Sans Pro';
        font-style: normal;
        font-weight: 700;
        src: local('Source Sans Pro Bold'), local('SourceSansPro-Bold'), url(https://fonts.gstatic.com/s/sourcesanspro/v10/toadOcfmlt9b38dHJxOBGFkQc6VGVFSmCnC_l7QZG60.woff) format('woff');
      }}
    }}

    body,
    table,
    td,
    a {{
      -ms-text-size-adjust: 100%;
      /* 1 */
      -webkit-text-size-adjust: 100%;
      /* 2 */
    }}


    table,
    td {{
      mso-table-rspace: 0pt;
      mso-table-lspace: 0pt;
    }}


    img {{
      -ms-interpolation-mode: bicubic;
    }}

    a[x-apple-data-detectors] {{
      font-family: inherit !important;
      font-size: inherit !important;
      font-weight: inherit !important;
      line-height: inherit !important;
      color: inherit !important;
      text-decoration: none !important;
    }}

    div[style*="margin: 16px 0;"] {{
      margin: 0 !important;
    }}

    body {{
      width: 100% !important;
      height: 100% !important;
      padding: 0 !important;
      margin: 0 !important;
    }}

    table {{
      border-collapse: collapse !important;
    }}

    .container {{
      padding-top: 10px;
      padding-right: 20px;
      padding-left: 20px;
      padding-bottom: 5px;
      color: white;
    }}

    a {{
      color: #1a82e2;
    }}

    img {{
      height: auto;
      line-height: 100%;
      text-decoration: none;
      border: 0;
      outline: none;
    }}
  </style>

</head>

<body style="background-color: #e9ecef;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="center" bgcolor="#e9ecef">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
          <tr>
            <td align="left" bgcolor="#ffffff"
              style="padding: 36px 24px 0; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; border-top: 3px solid #d4dadf;">
              <h1 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -1px; line-height: 48px;">Забыли
                пароль?</h1>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <tr>
      <td align="center" bgcolor="#e9ecef">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
          <tr>
            <td align="left" bgcolor="#ffffff"
              style="padding: 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px;">
              <p style="margin: 0;">Мы получили запрос на сброс пароля для учетной записи связанной с {}. В вашу учетную
                запись пока не внесено никаких изменений.</p>
            </td>
          </tr>

          <tr>
            <td align="left" bgcolor="#ffffff">
              <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td align="center" bgcolor="#ffffff" style="padding: 12px;">
                    <table border="0" cellpadding="0" cellspacing="0">
                      <tr>
                        <td align="center" bgcolor="#1a82e2" style="border-radius: 6px;" , color="white">
                          <div class="container">
                            <p>Ваш секретный код!</p>
                            <h2 class="SecretCode">{}</h2>
                          </div>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <td align="left" bgcolor="#ffffff"
            style="padding: 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px; border-bottom: 3px solid #d4dadf">
            <p style="margin: 0;">
            <p>С уважением, Команда <b>Swiper</b></p>
          </td>
    </tr>
  </table>
  </td>
  </tr>
</body>
</html> """