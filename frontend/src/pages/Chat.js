import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import styled from 'styled-components';
import io from 'socket.io-client';

const ChatContainer = styled.div`
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
`;

const Header = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(10px);
  border-bottom: 2px solid #333;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const BackButton = styled.button`
  background: transparent;
  border: 1px solid #666;
  color: #ccc;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-family: 'Cinzel', serif;
  transition: all 0.3s ease;

  &:hover {
    border-color: #FFD700;
    color: #FFD700;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
  }
`;

const ChatTitle = styled.div`
  font-family: 'Cinzel', serif;
  color: #FFD700;
  font-size: 1.2rem;
  font-weight: 600;
`;

const MainContent = styled.div`
  margin-top: 100px;
  flex: 1;
  display: flex;
  flex-direction: column;
`;

const MessagesContainer = styled.div`
  flex: 1;
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #333;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1rem;
  overflow-y: auto;
  max-height: 60vh;
  min-height: 400px;
`;

const Message = styled(motion.div)`
  margin-bottom: 1rem;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  max-width: 70%;
  word-wrap: break-word;
  position: relative;
  
  ${props => props.isOwn ? `
    background: linear-gradient(45deg, #8B0000, #FF0000);
    margin-left: auto;
    border: 1px solid #FFD700;
  ` : `
    background: rgba(0, 0, 0, 0.6);
    border: 1px solid #666;
  `}
`;

const MessageText = styled.div`
  font-family: 'Cinzel', serif;
  color: #fff;
  line-height: 1.4;
`;

const MessageTime = styled.div`
  font-size: 0.8rem;
  color: #888;
  margin-top: 0.5rem;
  text-align: right;
`;

const MessageSender = styled.div`
  font-size: 0.9rem;
  color: #FFD700;
  margin-bottom: 0.3rem;
  font-weight: 600;
`;

const InputContainer = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
`;

const MessageInput = styled.input`
  flex: 1;
  padding: 12px 16px;
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #666;
  border-radius: 8px;
  color: #fff;
  font-family: 'Cinzel', serif;
  font-size: 16px;
  transition: all 0.3s ease;

  &:focus {
    outline: none;
    border-color: #FFD700;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
  }

  &::placeholder {
    color: #888;
  }
`;

const SendButton = styled.button`
  background: linear-gradient(45deg, #8B0000, #FF0000);
  border: 2px solid #FFD700;
  color: #fff;
  padding: 12px 24px;
  font-family: 'Cinzel', serif;
  font-weight: 600;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;

  &:hover {
    background: linear-gradient(45deg, #FF0000, #8B0000);
    box-shadow: 0 0 15px rgba(255, 0, 0, 0.4);
    transform: translateY(-2px);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const ConnectionStatus = styled.div`
  background: ${props => props.connected ? 'rgba(0, 100, 0, 0.8)' : 'rgba(139, 0, 0, 0.8)'};
  border: 2px solid ${props => props.connected ? '#00FF00' : '#FF0000'};
  color: #fff;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-family: 'Cinzel', serif;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  text-align: center;
`;

const WelcomeMessage = styled.div`
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid #FFD700;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
  text-align: center;
  font-family: 'Cinzel', serif;
  color: #ccc;
  line-height: 1.6;
`;

const Chat = ({ currentUser, audioManager }) => {
  const { username } = useParams();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [connected, setConnected] = useState(false);
  const [socket, setSocket] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Initialize socket connection
    const newSocket = io('http://localhost:8000', {
      transports: ['websocket']
    });

    newSocket.on('connect', () => {
      setConnected(true);
      newSocket.emit('join_chat', {
        username: currentUser.username,
        targetUsername: username
      });
    });

    newSocket.on('disconnect', () => {
      setConnected(false);
    });

    newSocket.on('message', (message) => {
      setMessages(prev => [...prev, message]);
      if (audioManager) {
        audioManager.playSound('success');
      }
    });

    newSocket.on('user_joined', (data) => {
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: `${data.username} has entered the shadows...`,
        sender: 'system',
        timestamp: new Date().toISOString(),
        isSystem: true
      }]);
    });

    newSocket.on('user_left', (data) => {
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: `${data.username} has faded into the darkness...`,
        sender: 'system',
        timestamp: new Date().toISOString(),
        isSystem: true
      }]);
    });

    setSocket(newSocket);

    // Load message history
    loadMessageHistory();

    return () => {
      newSocket.close();
    };
  }, [currentUser.username, username, audioManager]);

  const loadMessageHistory = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/messages/${currentUser.id}/${username}`);
      setMessages(response.data);
    } catch (error) {
      console.error('Failed to load message history:', error);
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (newMessage.trim() && socket && connected) {
      const message = {
        id: Date.now(),
        text: newMessage.trim(),
        sender: currentUser.username,
        timestamp: new Date().toISOString()
      };

      socket.emit('message', {
        ...message,
        targetUsername: username
      });

      setMessages(prev => [...prev, message]);
      setNewMessage('');
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <ChatContainer>
      <Header>
        <BackButton onClick={() => navigate('/')}>← Back to Souls</BackButton>
        <ChatTitle>Chatting with {username}</ChatTitle>
        <div></div>
      </Header>

      <MainContent>
        <ConnectionStatus connected={connected}>
          {connected ? 'Connected to the shadows' : 'Disconnected from the shadows'}
        </ConnectionStatus>

        {messages.length === 0 && (
          <WelcomeMessage>
            <h3 style={{ color: '#FFD700', marginBottom: '1rem' }}>
              Welcome to the Shadow Realm
            </h3>
            <p>
              You have successfully connected with {username} through the mysterious poetry.
              Begin your conversation in the shadows...
            </p>
          </WelcomeMessage>
        )}

        <MessagesContainer>
          {messages.map((message) => (
            <Message
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              isOwn={message.sender === currentUser.username}
              isSystem={message.isSystem}
            >
              {!message.isSystem && message.sender !== currentUser.username && (
                <MessageSender>{message.sender}</MessageSender>
              )}
              <MessageText>{message.text}</MessageText>
              <MessageTime>{formatTime(message.timestamp)}</MessageTime>
            </Message>
          ))}
          <div ref={messagesEndRef} />
        </MessagesContainer>

        <InputContainer>
          <MessageInput
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Type your message in the shadows..."
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage(e)}
            disabled={!connected}
          />
          <SendButton
            onClick={handleSendMessage}
            disabled={!connected || !newMessage.trim()}
          >
            Send
          </SendButton>
        </InputContainer>
      </MainContent>
    </ChatContainer>
  );
};

export default Chat;
