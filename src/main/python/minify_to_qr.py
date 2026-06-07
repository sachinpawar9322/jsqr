import minify_html
import qrcode
import gzip
import base64
import sys


def minify(file: str) -> str:
    data = open(file).read()
    minified = minify_html.minify(data, minify_js=True, remove_processing_instructions=True).replace(';\n', ';').replace('\n', '')
    outputPath = '/'.join(file.split('/')[:-1]) + '/index.min.html'
    open(outputPath, 'w').write(minified)
    print(f'minified {len(data)} -> {len(minified)} bytes')
    return outputPath


REPO_BASE = 'https://raw.githack.com/sachinpawar9322/jsqr/master'
QR_MAX = 2953  # version 40, error_correction=L, byte mode capacity


def generateQR(file: str, source_file: str = None) -> str:
    data = open(file, 'rb').read()
    compressed = gzip.compress(data, compresslevel=9)
    encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
    embed_url = f'{REPO_BASE}/index.html#{encoded}'

    if len(embed_url) <= QR_MAX:
        url = embed_url
        print(f'mode: embed  gzip {len(data)} -> {len(compressed)} -> base64 {len(encoded)} chars  url {len(url)} chars')
    else:
        # File too large to embed — link directly to the source file on GitHub
        ref = source_file or file
        url = f'{REPO_BASE}/{ref}'
        print(f'mode: direct  embed would be {len(embed_url)} chars (>{QR_MAX})  using url {len(url)} chars: {url}')

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()

    outputPath = '/'.join(file.split('/')[:-1]) + '/qr.png'
    img.save(outputPath)
    print(f'QR saved to {outputPath}')
    return outputPath


def minifyToQR(inputPath: str) -> str:
    minifiedPath = minify(inputPath)
    qrPath = generateQR(minifiedPath, source_file=inputPath)
    return qrPath


if __name__ == "__main__":
    path = sys.argv[1]
    qrPath = minifyToQR(path)
    print(f'Source: {path}\nResult: {qrPath}')
