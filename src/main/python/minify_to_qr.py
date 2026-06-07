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


def generateQR(file: str) -> str:
    data = open(file, 'rb').read()
    compressed = gzip.compress(data, compresslevel=9)
    encoded = base64.b64encode(compressed).decode('ascii')
    print(f'gzip {len(data)} -> {len(compressed)} bytes, base64 -> {len(encoded)} chars')

    url = f'https://raw.githack.com/sachinpawar9322/jsqr/master/index.html#{encoded}'
    print(f'URL length: {len(url)} chars')

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
    qrPath = generateQR(minifiedPath)
    return qrPath


if __name__ == "__main__":
    path = sys.argv[1]
    qrPath = minifyToQR(path)
    print(f'Source: {path}\nResult: {qrPath}')
