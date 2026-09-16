from pathlib import Path
import re, base64

p = Path('friends/direct.html')
s = p.read_text(encoding='utf-8')

# Keep the exact existing FRIENDS logo bytes, but serve them as a normal file.
m = re.search(r'<img([^>]*class="brand"[^>]*)src="data:image/([^;]+);base64,([^"]+)"([^>]*)>', s)
if m:
    ext = 'webp' if 'webp' in m.group(2).lower() else 'png'
    Path(f'friends/logo.{ext}').write_bytes(base64.b64decode(m.group(3)))
    logo_url = f'./logo.{ext}?v=20260916'
    s = re.sub(r'(<img[^>]*class="brand"[^>]*src=")[^"]+("[^>]*>)', lambda x: x.group(1)+logo_url+x.group(2), s, count=1)

# Remove stale PWA references for this public preview.
s = re.sub(r'<link[^>]+rel="manifest"[^>]*>', '', s, flags=re.I)
s = re.sub(r'<link[^>]+rel="apple-touch-icon"[^>]*>', '', s, flags=re.I)
s = re.sub(r'<script id="friends-navigation-safety-net">[\s\S]*?</script>', '', s)
s = re.sub(r'<script id="friends-preview-cache-reset">[\s\S]*?</script>', '', s)

# Final capture-phase nav handler: tabs work even if another app script errors.
safety = r'''<script id="friends-navigation-safety-net">
(function(){
  function syncNav(id){document.querySelectorAll('[data-view]').forEach(function(b){var on=b.getAttribute('data-view')===id;b.classList.toggle('on',on);if(b.closest('.nav'))b.classList.toggle('active',on);});}
  function go(id){var to=document.getElementById(id),from=document.querySelector('.view.active'),wash=document.querySelector('.motion-wash');if(!to)return;if(from===to){syncNav(id);return;}if(from)from.classList.add('leaving');if(wash)wash.classList.add('show');syncNav(id);setTimeout(function(){if(from)from.classList.remove('active','leaving');to.classList.add('active');to.style.animation='none';void to.offsetHeight;to.style.animation='';window.scrollTo(0,0);},150);setTimeout(function(){if(wash)wash.classList.remove('show');},270);}
  document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-view]');if(!b)return;e.preventDefault();e.stopImmediatePropagation();go(b.getAttribute('data-view'));},true);
  window.FRIENDS_GO=go;window.__FRIENDS_NAV_READY__=true;
})();
</script>
<script id="friends-preview-cache-reset">if('serviceWorker' in navigator){navigator.serviceWorker.getRegistrations().then(function(rs){rs.forEach(function(r){r.unregister();});}).catch(function(){});}</script>'''

s = s.replace('</body>', safety + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
