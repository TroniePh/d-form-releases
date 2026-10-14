'use strict';
const releaseBase='https://github.com/TroniePh/d-form-releases/releases';
async function loadRelease(){
  const status=document.getElementById('release-status');
  try{
    const stableResponse=await fetch('stable.json',{cache:'no-store'});
    const stable=stableResponse.ok?await stableResponse.json():null;
    if(stable&&stable.available&&stable.channel!=='stable')throw new Error('Invalid stable channel');
    const response=stable&&stable.available?null:await fetch('update.json',{cache:'no-store'});
    if(response&&!response.ok)throw new Error('Feed unavailable');
    const release=response?await response.json():stable;
    if(!release.available){status.textContent='Bộ cài đang được chuẩn bị. Bạn có thể liên hệ để nhận hỗ trợ.';return;}
    if(!/^\d+\.\d+\.\d+$/.test(release.version)||!['stable','preview'].includes(release.channel)||!Array.isArray(release.assets)||release.assets.length!==2)throw new Error('Invalid release');
    const assets=['Free','AllUsers'].map(scope=>{
      const found=release.assets.filter(a=>a.scope===scope);
      const name=`D-form-Setup-v${release.version}-${scope}.exe`;
      if(found.length!==1||found[0].name!==name||found[0].url!==`${releaseBase}/download/v${release.version}/${name}`||!Number.isSafeInteger(found[0].size)||found[0].size<1||found[0].size>268435456||!/^\w{64}$/.test(found[0].sha256)||!/^[a-f0-9]{64}$/i.test(found[0].sha256))throw new Error('Invalid download');
      return found[0];
    });
    status.textContent=`D-form ${release.version}${release.channel==='preview'?' preview':' '} · Word desktop 64-bit trên Windows`;
    document.getElementById('release-badge').textContent=`${release.version} ${release.channel==='preview'?'PREVIEW':'STABLE'}`;
    document.getElementById('preview-note').hidden=release.channel!=='preview';
    for(const asset of assets){
      const button=document.getElementById(`download-${asset.scope}`);
      button.href=asset.url;button.textContent='Tải bộ cài '+(asset.scope==='Free'?'cho tôi':'toàn máy')+' ↓';button.classList.remove('disabled');button.removeAttribute('aria-disabled');
      document.getElementById(`size-${asset.scope}`).textContent=`${(asset.size/1048576).toFixed(1)} MB · .exe · v${release.version}`;
    }
    document.getElementById('release-link').href=`${releaseBase}/tag/v${release.version}`;
    document.getElementById('checksums-link').href=`${releaseBase}/download/v${release.version}/SHA256SUMS.txt`;
  }catch(error){status.textContent='Chưa lấy được thông tin bộ cài. Mở các bản phát hành trên GitHub hoặc liên hệ hỗ trợ.';}
}
const tabs=[...document.querySelectorAll('[role=tab]')];
function selectTab(tab){
  for(const other of tabs){const selected=other===tab;other.setAttribute('aria-selected',String(selected));other.tabIndex=selected?0:-1;}
  const image=document.getElementById('demo-image');image.src='assets/'+tab.dataset.image;image.alt=tab.dataset.alt;
  document.getElementById('demo-panel').setAttribute('aria-labelledby',tab.id);
}
for(const tab of tabs){tab.addEventListener('click',()=>selectTab(tab));tab.addEventListener('keydown',event=>{let index=tabs.indexOf(tab);if(event.key==='ArrowRight')index=(index+1)%tabs.length;else if(event.key==='ArrowLeft')index=(index+tabs.length-1)%tabs.length;else if(event.key==='Home')index=0;else if(event.key==='End')index=tabs.length-1;else return;event.preventDefault();selectTab(tabs[index]);tabs[index].focus();});}
loadRelease();
