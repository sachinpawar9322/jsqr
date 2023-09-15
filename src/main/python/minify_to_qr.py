import minify_html
import qrcode
import base64
import sys

def minify(file:str)->str:
    f=open(file)
    data = f.read()
    minified = minify_html.minify(data, minify_js=True, remove_processing_instructions=True).replace(';\n',';').replace('\n','')
    outputPath='/'.join(file.split('/')[:-1])+'/index.min.html'
    o=open(outputPath,'w')
    o.write(minified)
    print(f'minified file of size {len(data)} to {len(minified)} size ')
    return outputPath


def generateQR(file:str)->str:
    f=open(file)
    data = f.read()
    ascii=data.encode('utf-8')
    encoded=f'data:text/html;base64, {base64.b64encode(ascii).decode("utf-8")}'
    print(encoded)
    img = qrcode.make(encoded)
    type(img)  
    outputPath='/'.join(file.split('/')[:-1])+'/qr.png'
    img.save(outputPath)
    outputPath


def minifyToQR(inputPath:str)->str:
    minifiedPath=minify(inputPath)
    qrPath=generateQR(minifiedPath)
    return qrPath


if __name__ == "__main__":
    path=sys.argv[1]
    qrPath=generateQR(path)
    