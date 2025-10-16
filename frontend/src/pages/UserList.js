import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import styled from 'styled-components';
import axios from 'axios';

const UserListContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
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

const Logo = styled.div`
  font-family: 'Nosifer', cursive;
  font-size: 1.8rem;
  color: #FF0000;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
`;

const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const UserName = styled.span`
  font-family: 'Cinzel', serif;
  color: #FFD700;
  font-weight: 600;
`;

const LogoutBtn = styled.button`
  background: transparent;
  border: 1px solid #666;
  color: #ccc;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-family: 'Cinzel', serif;
  transition: all 0.3s ease;

  &:hover {
    border-color: #FF0000;
    color: #FF0000;
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
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

const UserGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
`;

const UserCard = styled(motion.div)`
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid #333;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;

  &:hover {
    border-color: #FFD700;
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(255, 215, 0, 0.2);
  }

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #FFD700, transparent);
    transition: left 0.5s;
  }

  &:hover::before {
    left: 100%;
  }
`;

const UserCardName = styled.h3`
  font-family: 'Cinzel', serif;
  font-size: 1.3rem;
  color: #FFD700;
  margin-bottom: 1rem;
  text-align: center;
`;

const PoemPreview = styled.div`
  font-family: 'Cinzel', serif;
  font-size: 0.9rem;
  line-height: 1.6;
  color: #ccc;
  text-align: center;
  max-height: 120px;
  overflow: hidden;
  position: relative;

  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 20px;
    background: linear-gradient(transparent, rgba(0, 0, 0, 0.9));
  }
`;

const ConnectButton = styled.button`
  background: linear-gradient(45deg, #8B0000, #FF0000);
  border: 2px solid #FFD700;
  color: #fff;
  padding: 10px 20px;
  font-family: 'Cinzel', serif;
  font-weight: 600;
  font-size: 14px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  width: 100%;
  margin-top: 1rem;

  &:hover {
    background: linear-gradient(45deg, #FF0000, #8B0000);
    box-shadow: 0 0 15px rgba(255, 0, 0, 0.4);
    transform: translateY(-2px);
  }
`;

const LoadingSpinner = styled.div`
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #FF0000;
  animation: spin 1s ease-in-out infinite;
  margin: 2rem auto;
  display: block;

  @keyframes spin {
    to { transform: rotate(360deg); }
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

const UserList = ({ currentUser, onLogout, audioManager }) => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchUsers();
    if (audioManager) {
      audioManager.startMusic();
    }
  }, [audioManager]);

  const fetchUsers = async () => {
    try {
      const response = await axios.get('http://localhost:8000/users');
      // Filter out current user and ensure we have an array
      const otherUsers = (response.data || []).filter(user => user.username !== currentUser.username);
      setUsers(otherUsers);
    } catch (err) {
      console.error('Error fetching users:', err);
      setError('Failed to load users. Please make sure the backend is running.');
      setUsers([]); // Ensure users is always an array
    } finally {
      setLoading(false);
    }
  };

  const handleConnect = (username) => {
    navigate(`/connect/${username}`);
  };

  const handleLogout = () => {
    if (audioManager) {
      audioManager.stopMusic();
    }
    onLogout();
  };

  if (loading) {
    return (
      <UserListContainer>
        <Header>
          <Logo>Halloween Poe Chat</Logo>
          <UserInfo>
            <UserName>Welcome, {currentUser.username}</UserName>
            <LogoutBtn onClick={handleLogout}>Logout</LogoutBtn>
          </UserInfo>
        </Header>
        <MainContent>
          <LoadingSpinner />
        </MainContent>
      </UserListContainer>
    );
  }

  return (
    <UserListContainer>
      <Header>
        <Logo>Halloween Poe Chat</Logo>
        <UserInfo>
          <UserName>Welcome, {currentUser.username}</UserName>
          <LogoutBtn onClick={handleLogout}>Logout</LogoutBtn>
        </UserInfo>
      </Header>

      <MainContent>
        <Title>Mysterious Souls Await</Title>
        <Subtitle>Choose a soul to connect with through the shadows...</Subtitle>

        {error && <ErrorMessage>{error}</ErrorMessage>}

        <UserGrid>
          {(users || []).map((user, index) => (
            <UserCard
              key={user.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <UserCardName>{user.username}</UserCardName>
              <PoemPreview>{user.poem}</PoemPreview>
              <ConnectButton onClick={() => handleConnect(user.username)}>
                Attempt Connection
              </ConnectButton>
            </UserCard>
          ))}
        </UserGrid>

        {(users || []).length === 0 && !loading && (
          <div style={{ textAlign: 'center', margin: '2rem 0' }}>
            <p style={{ fontFamily: 'Cinzel', color: '#ccc', fontSize: '1.2rem' }}>
              No other souls found in the shadows... Check back later.
            </p>
          </div>
        )}
      </MainContent>
    </UserListContainer>
  );
};

export default UserList;
