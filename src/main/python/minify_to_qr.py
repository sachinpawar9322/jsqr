import minify_html
import qrcode
import gzip
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
    print(f'gzip {len(data)} -> {len(compressed)} bytes ({round(len(compressed)/len(data)*100)}%)')

    qr = qrcode.QRCode(
        version=40,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=4,
    )
    qr.add_data(compressed, optimize=0)
    qr.make(fit=False)
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
