import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import axios from 'axios';

const ChatContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  color: #fff;
  padding: 2rem;
  position: relative;
  overflow: hidden;
`;

const ChatHeader = styled.div`
  text-align: center;
  margin-bottom: 2rem;
  position: relative;
  z-index: 2;
`;

const Title = styled.h1`
  font-family: 'Cinzel', serif;
  font-size: 2.5rem;
  color: #FFD700;
  text-shadow: 0 0 20px #FFD700;
  margin-bottom: 1rem;
  animation: glow 2s ease-in-out infinite alternate;
  
  @keyframes glow {
    from { text-shadow: 0 0 20px #FFD700; }
    to { text-shadow: 0 0 30px #FFD700, 0 0 40px #FFD700; }
  }
`;

const Subtitle = styled.p`
  font-family: 'Crimson Text', serif;
  font-size: 1.2rem;
  color: #ccc;
  margin-bottom: 2rem;
`;

const ChatArea = styled.div`
  max-width: 800px;
  margin: 0 auto;
  background: rgba(0, 0, 0, 0.7);
  border: 2px solid #FFD700;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
  position: relative;
  z-index: 2;
`;

const MessagesContainer = styled.div`
  height: 400px;
  overflow-y: auto;
  border: 1px solid #333;
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
  background: rgba(0, 0, 0, 0.5);
  
  &::-webkit-scrollbar {
    width: 8px;
  }
  
  &::-webkit-scrollbar-track {
    background: #333;
    border-radius: 4px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #FFD700;
    border-radius: 4px;
  }
`;

const Message = styled.div`
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 8px;
  background: ${props => props.isOwn ? 'rgba(255, 215, 0, 0.2)' : 'rgba(255, 255, 255, 0.1)'};
  border-left: 3px solid ${props => props.isOwn ? '#FFD700' : '#666'};
`;

const MessageHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
`;

const Sender = styled.span`
  font-weight: bold;
  color: ${props => props.isOwn ? '#FFD700' : '#fff'};
  font-family: 'Cinzel', serif;
`;

const Timestamp = styled.span`
  font-size: 0.8rem;
  color: #999;
`;

const MessageText = styled.div`
  color: #fff;
  line-height: 1.4;
`;

const InputArea = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
`;

const MessageInput = styled.input`
  flex: 1;
  padding: 0.8rem;
  border: 2px solid #333;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  font-size: 1rem;
  
  &:focus {
    outline: none;
    border-color: #FFD700;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
  }
  
  &::placeholder {
    color: #666;
  }
`;

const SendButton = styled.button`
  padding: 0.8rem 1.5rem;
  background: linear-gradient(45deg, #FFD700, #FFA500);
  color: #000;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: linear-gradient(45deg, #FFA500, #FFD700);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
  }
  
  &:disabled {
    background: #666;
    cursor: not-allowed;
    transform: none;
  }
`;

const BackButton = styled.button`
  position: absolute;
  top: 1rem;
  left: 1rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 0, 0, 0.7);
  color: #FFD700;
  border: 1px solid #FFD700;
  border-radius: 5px;
  cursor: pointer;
  font-family: 'Cinzel', serif;
  
  &:hover {
    background: rgba(255, 215, 0, 0.1);
  }
`;

const ChatSimple = ({ currentUser, onBack }) => {
  const { username } = useParams();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [targetUser, setTargetUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef(null);
  const pollingInterval = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Fetch target user data
    const fetchTargetUser = async () => {
      try {
        const response = await axios.get('http://localhost:8000/users');
        const user = response.data.find(u => u.username === username);
        if (user) {
          setTargetUser(user);
        } else {
          console.error('Target user not found:', username);
          navigate('/');
        }
      } catch (error) {
        console.error('Error fetching target user:', error);
        navigate('/');
      }
    };

    if (username) {
      fetchTargetUser();
    }
  }, [username, navigate]);

  useEffect(() => {
    if (!currentUser || !targetUser) return;

    // Load message history
    loadMessageHistory();

    // Start polling for new messages
    pollingInterval.current = setInterval(() => {
      loadMessageHistory();
    }, 2000); // Poll every 2 seconds

    return () => {
      if (pollingInterval.current) {
        clearInterval(pollingInterval.current);
      }
    };
  }, [currentUser, targetUser]);

  const loadMessageHistory = async () => {
    if (!currentUser || !targetUser) return;
    
    try {
      const response = await axios.get(
        `http://localhost:8000/messages/${currentUser.id}/${targetUser.username}`
      );
      const history = response.data.map(msg => ({
        ...msg,
        isOwn: msg.sender === currentUser.username
      }));
      setMessages(history);
    } catch (error) {
      console.error('Error loading message history:', error);
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    console.log('sendMessage called:', { newMessage, currentUser, targetUser });
    
    if (!newMessage.trim() || !currentUser || !targetUser) {
      console.log('sendMessage blocked:', { 
        hasMessage: !!newMessage.trim(), 
        hasCurrentUser: !!currentUser, 
        hasTargetUser: !!targetUser 
      });
      return;
    }

    try {
      console.log('Sending message to backend...');
      const response = await axios.post('http://localhost:8000/send-message', {
        content: newMessage,
        target_username: targetUser.username,
        current_username: currentUser.username
      });

      console.log('Message sent successfully:', response.data);

      // Add message to local state
      setMessages(prev => [...prev, {
        ...response.data,
        isOwn: true
      }]);

      setNewMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Failed to send message. Please check if the backend is running.');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleBack = () => {
    if (onBack) {
      onBack();
    } else {
      navigate('/');
    }
  };

  if (loading || !currentUser || !currentUser.username || !targetUser) {
    return (
      <ChatContainer>
        <ChatHeader>
          <Title>Loading Messages...</Title>
          <Subtitle>
            {!currentUser ? 'Loading user data...' : 
             !currentUser.username ? 'Invalid user data...' : 
             !targetUser ? 'Loading target user...' : 'Loading messages...'}
          </Subtitle>
        </ChatHeader>
      </ChatContainer>
    );
  }

  return (
    <ChatContainer>
      <BackButton onClick={handleBack}>← Back to Connections</BackButton>
      
      <ChatHeader>
        <Title>Mysterious Chat</Title>
        <Subtitle>
          Chatting with {targetUser.username} • Simple Mode
        </Subtitle>
      </ChatHeader>

      <ChatArea>
        <MessagesContainer>
          {messages.map((message) => (
            <Message key={message.id} isOwn={message.isOwn}>
              <MessageHeader>
                <Sender isOwn={message.isOwn}>
                  {message.sender}
                </Sender>
                <Timestamp>
                  {new Date(message.timestamp).toLocaleTimeString()}
                </Timestamp>
              </MessageHeader>
              <MessageText>{message.content}</MessageText>
            </Message>
          ))}
          <div ref={messagesEndRef} />
        </MessagesContainer>

        <InputArea>
          <MessageInput
            type="text"
            value={newMessage}
            onChange={(e) => {
              console.log('Input changed:', e.target.value);
              setNewMessage(e.target.value);
            }}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            autoFocus
          />
          <SendButton 
            onClick={sendMessage} 
            disabled={!newMessage.trim()}
          >
            Send
          </SendButton>
        </InputArea>
      </ChatArea>
    </ChatContainer>
  );
};

export default ChatSimple;
