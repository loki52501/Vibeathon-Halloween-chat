import React, { useState } from 'react';
import { motion } from 'framer-motion';
import styled from 'styled-components';
import axios from 'axios';

const RegistrationContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
`;

const Title = styled.h1`
  font-family: 'Nosifer', cursive;
  font-size: 3.5rem;
  color: #FF0000;
  text-align: center;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  animation: flicker 3s infinite;
`;

const Subtitle = styled.h2`
  font-family: 'Creepster', cursive;
  font-size: 1.8rem;
  color: #FFD700;
  text-align: center;
  margin-bottom: 2rem;
`;

const Form = styled.form`
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid #333;
  border-radius: 12px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
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

const TextArea = styled.textarea`
  width: 100%;
  padding: 12px 16px;
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #666;
  border-radius: 8px;
  color: #fff;
  font-family: 'Cinzel', serif;
  font-size: 16px;
  min-height: 80px;
  resize: vertical;
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

const ErrorMessage = styled.div`
  background: rgba(139, 0, 0, 0.8);
  border: 2px solid #FF0000;
  color: #fff;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  font-family: 'Cinzel', serif;
  text-align: center;
`;

const SuccessMessage = styled.div`
  background: rgba(0, 100, 0, 0.8);
  border: 2px solid #00FF00;
  color: #fff;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  font-family: 'Cinzel', serif;
  text-align: center;
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
`;

const Registration = ({ onRegistration }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    questions: ['', '', ''],
    answers: ['', '', '']
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [generatedPoem, setGeneratedPoem] = useState('');

  const handleInputChange = (e, index = null) => {
    const { name, value } = e.target;
    
    if (index !== null) {
      setFormData(prev => ({
        ...prev,
        [name]: (prev[name] || []).map((item, i) => i === index ? value : item)
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await axios.post('http://localhost:8000/register', formData);
      
      setSuccess('Registration successful! Your Poe-style poem has been generated.');
      setGeneratedPoem(response.data.poem);
      
      // Auto-register the user after successful registration
      setTimeout(() => {
        onRegistration({
          id: response.data.user_id,
          username: formData.username,
          poem: response.data.poem
        });
      }, 2000);

    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <RegistrationContainer>
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <Title>Halloween Poe Chat</Title>
        <Subtitle>Enter the realm of mysterious connections...</Subtitle>

        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Label>Username</Label>
            <Input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              placeholder="Enter your mysterious username..."
              required
            />
          </FormGroup>

          <FormGroup>
            <Label>Password</Label>
            <Input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Choose a secret password..."
              required
            />
          </FormGroup>

          <FormGroup>
            <Label>Personal Questions (3 questions that someone should know about you)</Label>
            {(formData.questions || []).map((question, index) => (
              <div key={index} style={{ marginBottom: '1rem' }}>
                <Label>Question {index + 1}</Label>
                <Input
                  type="text"
                  name="questions"
                  value={question}
                  onChange={(e) => handleInputChange(e, index)}
                  placeholder={`Enter question ${index + 1}...`}
                  required
                />
              </div>
            ))}
          </FormGroup>

          <FormGroup>
            <Label>Answers (3 answers to your questions)</Label>
            {(formData.answers || []).map((answer, index) => (
              <div key={index} style={{ marginBottom: '1rem' }}>
                <Label>Answer {index + 1}</Label>
                <Input
                  type="text"
                  name="answers"
                  value={answer}
                  onChange={(e) => handleInputChange(e, index)}
                  placeholder={`Enter answer ${index + 1}...`}
                  required
                />
              </div>
            ))}
          </FormGroup>

          {error && <ErrorMessage>{error}</ErrorMessage>}
          {success && <SuccessMessage>{success}</SuccessMessage>}

          <Button type="submit" disabled={loading}>
            {loading ? 'Creating Your Mysterious Profile...' : 'Enter the Shadows'}
          </Button>
        </Form>

        {generatedPoem && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <PoemDisplay>{generatedPoem}</PoemDisplay>
          </motion.div>
        )}
      </motion.div>
    </RegistrationContainer>
  );
};

export default Registration;
