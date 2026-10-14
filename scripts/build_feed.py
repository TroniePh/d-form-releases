"""Build Pages download/update feeds from published GitHub release assets only."""
import argparse
import json
import os
import re
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO='TroniePh/d-form-releases'
BASE='https://github.com/'+REPO+'/releases'
TAG=re.compile(r'^v(\d+\.\d+\.\d+)$')

def manifest(release):
    match=TAG.fullmatch(release.get('tag_name',''))
    if not match or release.get('draft') or not release.get('published_at'):return None
    version=match[1]
    assets=[]
    for scope in ('Free','AllUsers'):
        name=f'D-form-Setup-v{version}-{scope}.exe'
        found=[a for a in release.get('assets',[]) if a['name']==name and a.get('state')=='uploaded']
        if len(found)!=1: return None
        asset=found[0];digest=asset.get('digest') or ''
        expected=BASE+f'/download/v{version}/{name}'
        if not re.fullmatch(r'sha256:[a-fA-F0-9]{64}',digest) or asset['browser_download_url']!=expected or not 0<asset['size']<=256*1024*1024:
            raise ValueError('Release asset is invalid: '+name)
        assets.append(dict(scope=scope,name=name,url=expected,size=asset['size'],sha256=digest[7:].lower()))
    return dict(available=True,version=version,channel='preview' if release.get('prerelease') else 'stable',
                published_at=release['published_at'],release_url=release['html_url'],notes=release.get('body') or '',
                word_architectures=['x64'],assets=assets)

def build(releases,target,upload_tag=None):
    candidates=[result for release in releases if (result:=manifest(release))]
    candidates.sort(key=lambda r:tuple(map(int,r['version'].split('.'))),reverse=True)
    stable=next((r for r in candidates if r['channel']=='stable'),None)
    none=dict(available=False,channel='stable',version='0.0.0',assets=[])
    selected=candidates[0] if candidates else none
    target.mkdir(parents=True,exist_ok=True)
    for name,value in [('update.json',selected),('stable.json',stable or none),('releases.json',dict(updated_at=datetime.now(timezone.utc).isoformat(),releases=candidates))]:
        (target/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n','utf-8')
    if upload_tag:
        item=next((r for r in candidates if 'v'+r['version']==upload_tag),None)
        if item is None:raise ValueError('Published release needs both correctly named installer assets with GitHub SHA256 digests')
        original=next(r for r in releases if r['tag_name']==upload_tag)
        names={a['name'] for a in original['assets']}
        generated=[]
        if 'update.json' not in names:
            path=target/'release-manifest'/'update.json';path.parent.mkdir(exist_ok=True)
            path.write_text(json.dumps(item,ensure_ascii=False,indent=2)+'\n','utf-8');generated.append(path)
        if 'SHA256SUMS.txt' not in names:
            path=target/'release-manifest'/'SHA256SUMS.txt';path.parent.mkdir(exist_ok=True)
            path.write_text('\n'.join(a['sha256']+'  '+a['name'] for a in item['assets'])+'\n','utf-8');generated.append(path)
        if generated:subprocess.run(['gh','release','upload',upload_tag,*map(str,generated),'--repo',REPO],check=True)
    return selected

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fixture');parser.add_argument('--output',default='docs');parser.add_argument('--upload-tag');args=parser.parse_args()
    if args.fixture:releases=json.loads(Path(args.fixture).read_text('utf-8-sig'))
    else:
        request=urllib.request.Request('https://api.github.com/repos/'+REPO+'/releases?per_page=100',headers={'Accept':'application/vnd.github+json','User-Agent':'D-form-Pages'})
        token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
        if token:request.add_header('Authorization','Bearer '+token)
        with urllib.request.urlopen(request,timeout=30) as response:releases=json.load(response)
    selected=build(releases,Path(args.output),args.upload_tag)
    print('Built verified download feeds:',selected['version'],selected['channel'],selected['available'])

if __name__=='__main__':main()
