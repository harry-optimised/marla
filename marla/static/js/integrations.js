document.addEventListener('DOMContentLoaded', () => {
    const integrationCode = document.getElementById('integrationCode');
    const apiKeyElement = document.getElementById('apiKey');
    const apiKey = apiKeyElement.dataset.apiKey;
    const snippet = `
<!-- Chatbot Widget Start -->
<link rel="stylesheet" href="http://localhost:8000/static/css/chatbot-widget.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">

<script>
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = 'http://localhost:8000/static/js/chatbot-widget.js';
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'chatbot-widget-jssdk'));

  window.chatbotSettings = {
    apiKey: '${apiKey}'
  };
</script>
<div id="chatbot-widget"></div>
<!-- Chatbot Widget End -->
    `.trim();
    integrationCode.value = snippet;

    const copyButton = document.getElementById('copyButton');
    copyButton.addEventListener('click', () => {
        integrationCode.select();
        document.execCommand('copy');
        alert('Code copied to clipboard!');
    });
});
