import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import styled from 'styled-components';
import axios from 'axios';

const ConnectionContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
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

const MainContent = styled.div`
  margin-top: 100px;
  padding: 2rem 0;
`;

const Title = styled.h1`
  font-family: 'Nosifer', cursive;
  font-size: 2.5rem;
  color: #FF0000;
  text-align: center;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
`;

const Subtitle = styled.h2`
  font-family: 'Creepster', cursive;
  font-size: 1.5rem;
  color: #FFD700;
  text-align: center;
  margin-bottom: 2rem;
`;

const PoemDisplay = styled.div`
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid #FFD700;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
  font-family: 'Cinzel', serif;
  font-size: 1.1rem;
  line-height: 1.8;
  color: #ccc;
  text-align: center;
  white-space: pre-line;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #FFD700, transparent);
    animation: shimmer 3s infinite;
  }

  @keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }
`;

const Form = styled.form`
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid #333;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
`;

const FormGroup = styled.div`
  margin-bottom: 1.5rem;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 0.5rem;
  font-family: 'Cinzel', serif;
  font-weight: 600;
  color: #FFD700;
  font-size: 1.1rem;
`;

const Input = styled.input`
  width: 100%;
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

const Button = styled.button`
  background: linear-gradient(45deg, #8B0000, #FF0000);
  border: 2px solid #FFD700;
  color: #fff;
  padding: 15px 30px;
  font-family: 'Cinzel', serif;
  font-weight: 600;
  font-size: 18px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  width: 100%;
  position: relative;
  overflow: hidden;

  &:hover {
    background: linear-gradient(45deg, #FF0000, #8B0000);
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
    transform: translateY(-2px);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const MessageDisplay = styled.div`
  background: ${props => {
    if (props.type === 'success') return 'rgba(0, 100, 0, 0.8)';
    if (props.type === 'error') return 'rgba(139, 0, 0, 0.8)';
    if (props.type === 'warning') return 'rgba(255, 165, 0, 0.8)';
    return 'rgba(0, 0, 0, 0.8)';
  }};
  border: 2px solid ${props => {
    if (props.type === 'success') return '#00FF00';
    if (props.type === 'error') return '#FF0000';
    if (props.type === 'warning') return '#FFD700';
    return '#666';
  }};
  color: #fff;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  font-family: 'Cinzel', serif;
  text-align: center;
`;

const AttemptsDisplay = styled.div`
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #666;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
  font-family: 'Cinzel', serif;
  text-align: center;
  color: #ccc;
`;

const CooldownDisplay = styled.div`
  background: rgba(255, 0, 0, 0.8);
  border: 2px solid #FF0000;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
  font-family: 'Cinzel', serif;
  text-align: center;
  color: #fff;
  animation: pulse 2s infinite;
`;

const ConnectionAttempt = ({ currentUser, audioManager }) => {
  const { username } = useParams();
  const navigate = useNavigate();
  const [targetUser, setTargetUser] = useState(null);
  const [answers, setAnswers] = useState(['', '', '']);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  const [attempts, setAttempts] = useState(0);
  const [cooldown, setCooldown] = useState(null);
  const [crypticMessage, setCrypticMessage] = useState('');

  useEffect(() => {
    fetchTargetUser();
    if (audioManager) {
      audioManager.startMusic();
    }
  }, [username, audioManager]);

  const fetchTargetUser = async () => {
    try {
      const response = await axios.get('http://localhost:8000/users');
      const user = response.data.find(u => u.username === username);
      if (user) {
        setTargetUser(user);
      } else {
        setMessage('User not found');
        setMessageType('error');
      }
    } catch (err) {
      setMessage('Failed to load user information');
      setMessageType('error');
    }
  };

  const handleInputChange = (e, index) => {
    const newAnswers = [...answers];
    newAnswers[index] = e.target.value;
    setAnswers(newAnswers);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await axios.post('http://localhost:8000/attempt-connection', {
        target_username: username,
        answers: answers
      });

      setAttempts(prev => prev + 1);
      setCrypticMessage(response.data.cryptic_message);

      if (response.data.success) {
        setMessage('Connection successful! You can now chat with this user.');
        setMessageType('success');
        if (audioManager) {
          audioManager.playSound('success');
          audioManager.setPitch(1.5); // High pitch for success
        }
        
        setTimeout(() => {
          navigate(`/chat/${username}`);
        }, 2000);
      } else {
        setMessage(`Only ${response.data.correct_answers}/3 answers correct. ${response.data.message}`);
        setMessageType('warning');
        
        // Adjust audio pitch based on accuracy
        if (audioManager) {
          if (response.data.correct_answers >= 2) {
            audioManager.setPitch(1.2); // Higher pitch for close answers
            audioManager.playSound('warning');
          } else {
            audioManager.setPitch(0.8); // Lower pitch for wrong answers
            audioManager.playSound('error');
          }
        }
      }

    } catch (err) {
      if (err.response?.status === 429) {
        setMessage(err.response.data.detail);
        setMessageType('error');
        setCooldown(120); // 2 minutes in seconds
        
        // Start cooldown timer
        const timer = setInterval(() => {
          setCooldown(prev => {
            if (prev <= 1) {
              clearInterval(timer);
              return null;
            }
            return prev - 1;
          });
        }, 1000);
        
        if (audioManager) {
          audioManager.setPitch(0.5); // Very low pitch for cooldown
          audioManager.playSound('error');
        }
      } else {
        setMessage(err.response?.data?.detail || 'Connection attempt failed');
        setMessageType('error');
        if (audioManager) {
          audioManager.playSound('error');
        }
      }
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!targetUser) {
    return (
      <ConnectionContainer>
        <div style={{ textAlign: 'center', margin: '2rem 0' }}>
          <p style={{ fontFamily: 'Cinzel', color: '#ccc', fontSize: '1.2rem' }}>
            Loading mysterious soul...
          </p>
        </div>
      </ConnectionContainer>
    );
  }

  return (
    <ConnectionContainer>
      <Header>
        <BackButton onClick={() => navigate('/')}>← Back to Souls</BackButton>
        <div style={{ fontFamily: 'Cinzel', color: '#FFD700' }}>
          Attempting Connection with {username}
        </div>
      </Header>

      <MainContent>
        <Title>Decipher the Shadows</Title>
        <Subtitle>Solve the riddle to connect with {username}</Subtitle>

        <PoemDisplay>{targetUser.poem}</PoemDisplay>

        {crypticMessage && (
          <MessageDisplay type="warning">
            <strong>Edgar Allan Poe whispers:</strong><br />
            {crypticMessage}
          </MessageDisplay>
        )}

        {cooldown && (
          <CooldownDisplay>
            <strong>Cooldown Active!</strong><br />
            Wait {formatTime(cooldown)} before your next attempt.
          </CooldownDisplay>
        )}

        {attempts > 0 && (
          <AttemptsDisplay>
            Attempts: {attempts}/5
          </AttemptsDisplay>
        )}

        {message && (
          <MessageDisplay type={messageType}>
            {message}
          </MessageDisplay>
        )}

        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Label>Your Answers (3 answers to the riddle above)</Label>
            {answers.map((answer, index) => (
              <div key={index} style={{ marginBottom: '1rem' }}>
                <Label>Answer {index + 1}</Label>
                <Input
                  type="text"
                  value={answer}
                  onChange={(e) => handleInputChange(e, index)}
                  placeholder={`Enter your answer ${index + 1}...`}
                  required
                  disabled={cooldown > 0}
                />
              </div>
            ))}
          </FormGroup>

          <Button 
            type="submit" 
            disabled={loading || cooldown > 0}
          >
            {loading ? 'Consulting the Spirits...' : 'Attempt Connection'}
          </Button>
        </Form>
      </MainContent>
    </ConnectionContainer>
  );
};

export default ConnectionAttempt;
