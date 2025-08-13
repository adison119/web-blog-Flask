function confirmDelete(){ return confirm('ยืนยันการลบโพสต์นี้?'); }
document.addEventListener('DOMContentLoaded', ()=>{
  const select = document.getElementById('layoutSelect');
  const color = document.getElementById('primaryColor');
  if(select || color){
    const preview = document.querySelector('.preview-box');
    const apply = ()=>{
      if(select){ preview.style.gridTemplateColumns = (select.value==='left')? '240px 1fr' : '1fr 240px'; }
      if(color){ document.documentElement.style.setProperty('--primary', color.value); }
    };
    if(select) select.addEventListener('change', apply);
    if(color) color.addEventListener('input', apply);
    apply();
  }
});
