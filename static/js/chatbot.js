/* SAIFS Chatbot Widget JS */
(function(){
  const toggle = document.getElementById('chatbot-toggle');
  const box    = document.getElementById('chatbot-box');
  const input  = document.getElementById('chatbot-input');
  const sendBtn= document.getElementById('chatbot-send');
  const msgs   = document.getElementById('chatbot-messages');

  if(!toggle || !box) return;

  toggle.addEventListener('click', ()=> box.classList.toggle('open'));

  function appendMsg(text, type){
    const div = document.createElement('div');
    div.className = type === 'user' ? 'msg-user' : 'msg-bot';
    div.textContent = text;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function sendMessage(){
    const text = input.value.trim();
    if(!text) return;
    appendMsg(text, 'user');
    input.value = '';

    fetch('/chatbot/message', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({message: text})
    })
    .then(r => r.json())
    .then(data => appendMsg(data.response || 'Sorry, something went wrong.', 'bot'))
    .catch(()=> appendMsg('Connection error. Please try again.', 'bot'));
  }

  sendBtn && sendBtn.addEventListener('click', sendMessage);
  input && input.addEventListener('keydown', e => { if(e.key === 'Enter') sendMessage(); });

  // Welcome message
  setTimeout(()=> appendMsg('👋 Hi! I\'m your Invertis SAIFS assistant. How can I help you today?', 'bot'), 500);
})();
