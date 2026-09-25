#!/usr/bin/env python3
"""Build a fresh annotated image viewer; SVG retains source/code controls."""
import argparse,base64,html,io,json,mimetypes,subprocess,tempfile,uuid
from pathlib import Path
import xml.etree.ElementTree as ET


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('image',type=Path)
    ap.add_argument('output',type=Path)
    ap.add_argument('--label',default='Image preview')
    ap.add_argument('--preview-output',type=Path,help='Required when a raster conversion or size reduction is needed; never overwrites the source.')
    args=ap.parse_args()
    raster=args.image.suffix.lower()!='.svg'
    download=args.image.name
    if not raster:
        source=args.image.read_text(encoding='utf-8')
        if ET.fromstring(source).tag.split('}')[-1]!='svg':ap.error('Input is not SVG.')
    else:
        from PIL import Image,ImageOps
        raw=args.image.read_bytes(); suffix=args.image.suffix.lower()
        try: im=Image.open(io.BytesIO(raw))
        except Exception:
            if suffix not in ('.heic','.heif'):ap.error('Unsupported image decoder. Convert this format to PNG or JPEG first.')
            with tempfile.TemporaryDirectory() as d:
                tmp=Path(d)/'preview.png'
                subprocess.run(['sips','-s','format','png',str(args.image),'--out',str(tmp)],check=True,capture_output=True)
                im=Image.open(tmp);im.load()
        animated=getattr(im,'n_frames',1)>1
        mime=mimetypes.guess_type(args.image.name)[0]
        native=suffix in ('.png','.jpg','.jpeg','.webp','.gif','.avif')
        needs=not native or len(raw)>550000 or bool(im.getexif().get(274,1)!=1)
        if animated and needs:ap.error('Multi-frame image needs an animation-preserving conversion; do not flatten it silently.')
        if needs:
            if not args.preview_output:ap.error('Conversion needed. Supply --preview-output in the task output directory; keep original separately.')
            if args.preview_output.resolve()==args.image.resolve():ap.error('Preview output must not overwrite original.')
            im=ImageOps.exif_transpose(im);im.thumbnail((1800,1800))
            alpha='A' in im.getbands();fmt='PNG' if alpha else 'JPEG';mime='image/png' if alpha else 'image/jpeg'
            for step in range(10):
                b=io.BytesIO();im.save(b,format=fmt,optimize=True,**({'quality':85} if fmt=='JPEG' else {}));raw=b.getvalue()
                if len(raw)<550000:break
                im=im.resize((max(1,int(im.width*.82)),max(1,int(im.height*.82))))
            expected=('.png',) if alpha else ('.jpg','.jpeg')
            if args.preview_output.suffix.lower() not in expected:ap.error('Use '+expected[0]+' for --preview-output for this image.')
            args.preview_output.parent.mkdir(parents=True,exist_ok=True);args.preview_output.write_bytes(raw);download=args.preview_output.name
            print('Display copy created; link original separately. Preview coordinates refer to display pixels.')
        w,h=im.size
        data='data:'+str(mime)+';base64,'+base64.b64encode(raw).decode()
        source=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><image width="{w}" height="{h}" href="{data}"/></svg>'
    template=(Path(__file__).resolve().parent.parent/'assets/viewer.html').read_text()
    if raster:
        import re
        template=re.sub(r'<button[^>]*id="svg-INSTANCE-code-tab"[^>]*>.*?</button>','',template)
        template=re.sub(r'<button[^>]*id="svg-INSTANCE-copy"[^>]*>.*?</button>','',template)
        template=template.replace('>Download SVG</a>','>Download image</a>')
        template=template.replace("root.querySelector('#svg-INSTANCE-download').href=uri;","root.querySelector('#svg-INSTANCE-download').href=new DOMParser().parseFromString(source,'image/svg+xml').querySelector('image').getAttribute('href');")
        template=template.replace("root.querySelector('#svg-INSTANCE-copy').onclick=async function(){","if(root.querySelector('#svg-INSTANCE-copy'))root.querySelector('#svg-INSTANCE-copy').onclick=async function(){")
        template=template.replace('SVG viewBox coordinates','image pixel coordinates').replace('SVG viewBox:','Image bounds:').replace("' on SVG'","' on image'")
    fragment=template.replace('INSTANCE',uuid.uuid4().hex[:12]).replace('DOWNLOAD_PLACEHOLDER',html.escape(download,quote=True)).replace('LABEL_PLACEHOLDER',html.escape(args.label,quote=True)).replace('SOURCE_PLACEHOLDER',json.dumps(source).replace('<','\\u003c'))
    if len(fragment.encode())>=1000000:ap.error('Viewer exceeds 1 MB. Reduce the display copy or subset SVG fonts, preserving the original.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(fragment,encoding='utf-8');print(args.output.resolve())

if __name__=='__main__': main()
