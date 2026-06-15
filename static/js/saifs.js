/* SAIFS Main JS */
(function(){
'use strict';

// ── Theme ──────────────────────────────────────────────────
const root = document.documentElement;
const savedTheme = localStorage.getItem('saifs-theme') || 'dark';
root.setAttribute('data-theme', savedTheme);

function toggleTheme(){
  const current = root.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', next);
  localStorage.setItem('saifs-theme', next);
  const btn = document.getElementById('theme-toggle');
  if(btn) btn.innerHTML = next === 'dark' ? '☀️' : '🌙';
}
window.toggleTheme = toggleTheme;

// ── Sidebar ────────────────────────────────────────────────
const sidebar = document.getElementById('saifs-sidebar');
const overlay = document.getElementById('sidebar-overlay');

function openSidebar(){
  if(!sidebar) return;
  sidebar.classList.add('open');
  overlay && overlay.classList.add('show');
}
function closeSidebar(){
  if(!sidebar) return;
  sidebar.classList.remove('open');
  overlay && overlay.classList.remove('show');
}
window.toggleSidebar = function(){
  sidebar && sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
};
overlay && overlay.addEventListener('click', closeSidebar);

// Active link highlight
const links = document.querySelectorAll('.sidebar-link');
links.forEach(link => {
  if(link.getAttribute('href') === window.location.pathname){
    link.classList.add('active');
  }
});

// ── Dropdown ───────────────────────────────────────────────
document.addEventListener('click', function(e){
  document.querySelectorAll('.saifs-dropdown-menu.show').forEach(menu => {
    if(!menu.parentElement.contains(e.target)) menu.classList.remove('show');
  });
});

window.toggleDropdown = function(id){
  const menu = document.getElementById(id);
  if(!menu) return;
  document.querySelectorAll('.saifs-dropdown-menu.show').forEach(m => {
    if(m.id !== id) m.classList.remove('show');
  });
  menu.classList.toggle('show');
};

// ── Toast ──────────────────────────────────────────────────
window.showToast = function(message, type='info', duration=4000){
  let container = document.getElementById('toast-container');
  if(!container){
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const icons = {success:'✅', danger:'❌', info:'ℹ️', warning:'⚠️'};
  const toast = document.createElement('div');
  toast.className = `toast-saifs ${type}`;
  toast.innerHTML = `<span>${icons[type]||'ℹ️'}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(()=>{ toast.style.opacity='0'; toast.style.transform='translateY(20px)'; setTimeout(()=>toast.remove(), 300); }, duration);
};

// ── Animated Counters ──────────────────────────────────────
function animateCounter(el){
  const target = parseInt(el.getAttribute('data-target') || el.textContent, 10);
  if(isNaN(target)) return;
  const duration = 1200;
  const step = target / (duration / 16);
  let current = 0;
  const timer = setInterval(()=>{
    current = Math.min(current + step, target);
    el.textContent = Math.floor(current);
    if(current >= target) clearInterval(timer);
  }, 16);
}

const counterEls = document.querySelectorAll('.stat-value[data-target]');
if(counterEls.length){
  const obs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        animateCounter(entry.target);
        obs.unobserve(entry.target);
      }
    });
  }, {threshold: 0.5});
  counterEls.forEach(el => obs.observe(el));
}

// ── Flash message auto-dismiss ─────────────────────────────
document.querySelectorAll('.alert-dismissible').forEach(alert => {
  setTimeout(()=>{
    alert.style.opacity = '0';
    alert.style.transform = 'translateY(-10px)';
    alert.style.transition = 'all 0.3s ease';
    setTimeout(()=>alert.remove(), 300);
  }, 4000);
});

// ── Upload drag-and-drop ───────────────────────────────────
const uploadZone = document.querySelector('.upload-zone');
if(uploadZone){
  const fileInput = document.getElementById('file-input');
  uploadZone.addEventListener('click', ()=> fileInput && fileInput.click());
  uploadZone.addEventListener('dragover', e=>{e.preventDefault(); uploadZone.classList.add('dragover');});
  uploadZone.addEventListener('dragleave', ()=> uploadZone.classList.remove('dragover'));
  uploadZone.addEventListener('drop', e=>{
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    if(fileInput && e.dataTransfer.files.length){
      fileInput.files = e.dataTransfer.files;
      const nameEl = document.getElementById('file-name-display');
      if(nameEl) nameEl.textContent = e.dataTransfer.files[0].name;
    }
  });
  if(fileInput){
    fileInput.addEventListener('change', ()=>{
      const nameEl = document.getElementById('file-name-display');
      if(nameEl && fileInput.files.length) nameEl.textContent = fileInput.files[0].name;
    });
  }
}

// ── Init theme icon ────────────────────────────────────────
document.addEventListener('DOMContentLoaded', ()=>{
  const btn = document.getElementById('theme-toggle');
  if(btn) btn.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
});

})();
