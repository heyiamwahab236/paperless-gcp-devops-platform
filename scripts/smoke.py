"""Authenticate, ingest a synthetic PDF, verify search and original-file integrity.

No third-party packages. Use only on a disposable/local portfolio instance.
Credentials are read from environment or a hidden prompt; never logged.
"""
import argparse
import getpass
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid


def make_pdf(marker):
    content = f'BT /F1 12 Tf 50 740 Td (Synthetic portfolio evidence {marker}) Tj ET'.encode()
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
               b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
               b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
               b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
               b'<< /Length ' + str(len(content)).encode() + b' >>\nstream\n' + content + b'\nendstream']
    pdf = bytearray(b'%PDF-1.4\n')
    offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf.extend(f'{index} 0 obj\n'.encode() + obj + b'\nendobj\n')
    xref = len(pdf)
    pdf.extend(f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'.encode())
    for offset in offsets[1:]:
        pdf.extend(f'{offset:010d} 00000 n \n'.encode())
    pdf.extend(f'trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
    return bytes(pdf)


def request(base, path, token=None, data=None, content_type=None):
    headers = {'Accept': 'application/json'}
    if token:
        headers['Authorization'] = 'Token ' + token
    if content_type:
        headers['Content-Type'] = content_type
    req = urllib.request.Request(base + path, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://localhost:8000')
    parser.add_argument('--timeout', type=int, default=360)
    args = parser.parse_args()
    base = args.url.rstrip('/')
    parsed = urllib.parse.urlparse(base)
    if parsed.hostname not in ('localhost', '127.0.0.1') or parsed.scheme != 'http':
        raise SystemExit('This demo smoke test only accepts HTTP on localhost or 127.0.0.1.')
    username = os.environ.get('PAPERLESS_TEST_USER') or input('Admin username: ')
    password = os.environ.get('PAPERLESS_TEST_PASSWORD') or getpass.getpass('Admin password: ')
    token = json.loads(request(base, '/api/token/', data=json.dumps({'username': username, 'password': password}).encode(), content_type='application/json'))['token']
    marker = 'portfolio' + uuid.uuid4().hex
    pdf = make_pdf(marker)
    boundary = '----portfolio' + uuid.uuid4().hex
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="title"\r\n\r\n{marker}\r\n'
            f'--{boundary}\r\nContent-Disposition: form-data; name="document"; filename="{marker}.pdf"\r\n'
            'Content-Type: application/pdf\r\n\r\n').encode() + pdf + f'\r\n--{boundary}--\r\n'.encode()
    request(base, '/api/documents/post_document/', token, body, 'multipart/form-data; boundary=' + boundary)
    deadline = time.monotonic() + args.timeout
    while time.monotonic() < deadline:
        result = json.loads(request(base, '/api/documents/?query=' + marker, token))
        docs = [doc for doc in result.get('results', []) if doc['title'] == marker]
        if docs:
            doc = docs[0]
            if marker not in doc.get('content', ''):
                raise RuntimeError('Search found the title but extracted document text did not match')
            original = request(base, f'/api/documents/{doc["id"]}/download/?original=true', token)
            if hashlib.sha256(original).digest() != hashlib.sha256(pdf).digest():
                raise RuntimeError('Downloaded original differs from the uploaded PDF')
            print(json.dumps({'result': 'PASS', 'document_id': doc['id'], 'marker': marker,
                              'checks': ['authentication', 'upload', 'text extraction', 'search', 'original SHA-256'],
                              'note': 'Synthetic document retained for persistence and restore drills; not an OCR benchmark.'}, indent=2))
            return
        time.sleep(5)
    raise TimeoutError('Document did not become searchable within the timeout')


if __name__ == '__main__':
    main()
