from pathlib import Path
import re

p = Path('friends/direct.html')
s = p.read_text(encoding='utf-8')

# Use a normal PNG file instead of the corrupted embedded logo data URI.
s = re.sub(r'(<img[^>]*class="brand"[^>]*src=")[^"]+("[^>]*>)', lambda m: m.group(1)+'./logo.png?v=20260916'+m.group(2), s, count=1)

# Remove stale PWA references for this public preview.
s = re.sub(r'<link[^>]+rel="manifest"[^>]*>', '', s, flags=re.I)
s = re.sub(r'<link[^>]+rel="apple-touch-icon"[^>]*>', '', s, flags=re.I)
s = re.sub(r'<script id="friends-navigation-safety-net">[\s\S]*?</script>', '', s)
s = re.sub(r'<script id="friends-preview-cache-reset">[\s\S]*?</script>', '', s)

# Final capture-phase navigation handler: the approved v0.19 motion-wash stays intact.
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
