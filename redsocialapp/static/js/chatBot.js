import { createChat } from 'https://cdn.jsdelivr.net/npm/@n8n/chat/dist/chat.bundle.es.js';

createChat({
  webhookUrl: window.N8N_CHAT_WEBHOOK, 
  webhookConfig: {
    method: 'POST',
    headers: {}
  },
  target: '#n8n-chat',
  mode: 'window',
  chatInputKey: 'chatInput',
  chatSessionKey: 'sessionId',
  metadata: {},
  showWelcomeScreen: false,
  defaultLanguage: 'es',
  initialMessages: [
    'Hola! 👋',
    'Mi nombre es Raulito, ¿en qué te puedo ayudar hoy?'
  ],
  i18n: {
    en: {
      title: 'Hi there! 👋',
      subtitle: "Start a chat. We're here to help you 24/7.",
      footer: '',
      getStarted: 'New Conversation',
      inputPlaceholder: 'Type your question..',
    },
  },
});