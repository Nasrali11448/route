from flask import Flask, request
import requests
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

app = Flask(__name__)

# Target server URL
target_server = 'http://route.sandboxol.com'

# Create a ThreadPoolExecutor with max_workers=10
executor = ThreadPoolExecutor(max_workers=10000000000)

def send_http_request(method, url, headers=None, data=None, params=None):
    if headers and 'Host' in headers:
        headers['Host'] = 'route.sandboxol.com'
    if headers and 'Bmg-Device-Id' in headers:
        headers['Bmg-Device-Id'] = 'e6433c4092731c17'
    if headers and 'Bmg-Sign' in headers:
        headers['Bmg-Sign'] = 'ra5mZ7jmTxHovoJcMfnqmfqPAphh6PzNba+Z6GrYGw3C+Q='
    response = requests.request(
        method,
        url,
        headers=headers,
        data=data,
        params=params
    )
    return response.content, response.status_code, {'Content-Type': response.headers.get('Content-Type')}

def process_request(path, method, headers, body, params):
    target_url = f"{target_server}/{path}"
    return send_http_request(method, target_url, headers=headers, data=body, params=params)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    method = request.method.upper() if request.method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'] else 'GET'
    headers = dict(request.headers) if method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'] else {}
    body = request.get_data() if method in ['POST', 'PUT', 'PATCH'] else None

    print(f"Method: {method}")
    print(f"Headers: {headers}")
    print(f"Body: {body}")

    # Use "/test" path for a simple check
    if path == 'test':
        return 'Proxy is OK.', 200, {'Content-Type': 'text/plain'}

     # Otherwise, process the request as usual
    future = executor.submit(process_request, path, method, headers, body, request.args)
    content, status_code, content_type = future.result()

    return content, status_code, {'Content-Type': content_type}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    t = Thread()
    t.start()
