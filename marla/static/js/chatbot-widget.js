(function() {
    const apiKey = window.chatbotSettings.apiKey;

    const container = document.getElementById('chatbot-widget');
    container.innerHTML = `
        <div class="chatbot-widget">
            <div class="chatbot-widget__icon">
                <button id="chatbot-widget-toggle" class="btn btn-primary">
                    <img src="https://img.icons8.com/cotton/64/null/talk.png"/>
                </button>
            </div>
           
            <div class="chatbot-widget__content">
                <div class="chatbot-widget__input">
                    <input type="text" id="chatbot-widget-question" class="form-control" placeholder="Ask a question...">
                    <button id="chatbot-widget-submit" class="btn btn-success">Submit</button>
                </div>
                <div class="chatbot-widget__response" id="chatbot-widget-response"></div>
            </div>
        </div>
    `;

    const questionInput = document.getElementById('chatbot-widget-question');
    const submitButton = document.getElementById('chatbot-widget-submit');
    const responseContainer = document.getElementById('chatbot-widget-response');
    const toggleButton = document.getElementById('chatbot-widget-toggle');
    const contentContainer = container.querySelector('.chatbot-widget__content');

    toggleButton.addEventListener('click', () => {
        contentContainer.classList.toggle('open');
    });

    submitButton.addEventListener('click', async () => {
        const question = questionInput.value;
        if (question) {
            const response = await fetch('http://localhost:8000/api/ask/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question, api_key: apiKey })
            });

            if (response.ok) {
                const data = await response.json();
                responseContainer.innerHTML = data.answer;
            } else {
                responseContainer.innerHTML = 'Error: Unable to get a response.';
            }
        }
    });
})();
