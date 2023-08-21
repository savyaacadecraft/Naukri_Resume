from twocaptcha import TwoCaptcha
import requests

# Instance of TwoCaptcha
captcha_solver = TwoCaptcha('7eb7fd266b08d9115af5570bccca656c')

# Target website URL
site_url = "https://resdex.naukri.com/v3/preview?uniqId=6d1b85b660ffa593348c49678a356c1e5f540f55431b0c165010405e590c514d1b0e1157114758085b5819405f19051752595b00504811011403106&sid=6218990959&paramString=8b485a994a0b1f7d419bf11cc53a6d4b13106&hfFlowName=search&commentSearchType=comment-my,comment-others&totalResumes=12985&hiringForFlowId=7ff24aa64423ca3e6c292a28c804acf3&pFlow=SEARCH_ID&pFlowId=7ff24aa64423ca3e6c292a28c804acf3&tupleIndex=12&storageKey=6218990959-108&parentHighLightingKey=6218990959-108&activeIn=39&parentSid=6218990959&sidGroupId=7ff24aa64423ca3e6c292a28c804acf3&tabKey=profile"

# Getting the token
try:
    # For solving reCAPTCHA
    token = captcha_solver.recaptcha(
        sitekey="",
        url=site_url
    )

# Handling the exceptions
except Exception as e:
    raise SystemExit('Error: CAPTCHA token not recieved.')

# Sending the token to the website
print("Token: ", str(token))