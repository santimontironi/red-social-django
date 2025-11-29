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
    'Bienvenido, mi nombre es Raulito, ¿en qué te puedo ayudar hoy?'
  ],
  i18n: {
    es: {
      title: 'Hola! 👋',
      subtitle: "Empieza el chat conmigo. Estoy para ayudarte 24/7.",
      footer: '',
      getStarted: 'Nueva conversación',
      inputPlaceholder: 'Ingresa tu mensaje..',
    },
  },
});