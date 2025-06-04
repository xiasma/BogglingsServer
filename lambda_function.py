from app import app
from werkzeug.middleware.proxy_fix import ProxyFix
from mangum import Mangum
from app import *

# Helps with AWS API Gateway quirks
app.wsgi_app = ProxyFix(app.wsgi_app)

# Wrap Flask in Mangum for AWS Lambda compatibility
handler = Mangum(app)

def lambda_handler(event, context):
    return handler(event, context)