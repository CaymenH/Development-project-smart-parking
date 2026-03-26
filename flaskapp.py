from flask import Flask


app = Flask(__name__)

@app.route('/parkingapp', methods=['GET'])
def iotcentral_app():
    return '''
<html>
<body>
<button style="
   background-color: #00BA2B;
    padding: 30px 64px;
    "
 onclick ="window.open ('https://smartparking2025778.azureiotcentral.com/dashboards/dtmi%3Akkfvwa2xi%3Ap7pyt5x3o')">
    go to parking sensor dashboard 
</button>

<button style="
    background-color: #0023BA;
    color: FAFAFA;
    padding: 30px 64px;
    "
 onclick ="window.open ('https://smartparking2025778.azureiotcentral.com/dashboards/dtmi%3Akkfvwa2xi%3Ap7pyt5x3o')">
    go to parking disabled dashboard
</button>
</body>
</html>
'''
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5009)
