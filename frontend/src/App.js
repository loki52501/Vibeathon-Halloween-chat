import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import ParticleBackground from './components/ParticleBackground';
import AudioManager from './components/AudioManager';
import Registration from './pages/Registration';
import UserList from './pages/UserList';
import ConnectionAttempt from './pages/ConnectionAttempt';
import ChatSimple from './pages/ChatSimple';
import './App.css';

const AppContainer = styled.div`
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
`;

const App = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [audioManager, setAudioManager] = useState(null);

  useEffect(() => {
    // Initialize audio manager
    const audio = new AudioManager();
    setAudioManager(audio);
    
    // Check for existing user session
    const savedUser = localStorage.getItem('poeChatUser');
    if (savedUser) {
      setCurrentUser(JSON.parse(savedUser));
    }

    return () => {
      if (audio) {
        audio.cleanup();
      }
    };
  }, []);

  const handleUserRegistration = (userData) => {
    setCurrentUser(userData);
    localStorage.setItem('poeChatUser', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem('poeChatUser');
    if (audioManager) {
      audioManager.stopMusic();
    }
  };

  return (
    <Router>
      <AppContainer>
        <ParticleBackground />
        <AnimatePresence mode="wait">
          <Routes>
            <Route 
              path="/" 
              element={
                currentUser ? (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.5 }}
                  >
                    <UserList 
                      currentUser={currentUser} 
                      onLogout={handleLogout}
                      audioManager={audioManager}
                    />
                  </motion.div>
                ) : (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    transition={{ duration: 0.5 }}
                  >
                    <Registration onRegistration={handleUserRegistration} />
                  </motion.div>
                )
              } 
            />
            <Route 
              path="/connect/:username" 
              element={
                <motion.div
                  initial={{ opacity: 0, x: 100 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -100 }}
                  transition={{ duration: 0.5 }}
                >
                  <ConnectionAttempt 
                    currentUser={currentUser}
                    audioManager={audioManager}
                  />
                </motion.div>
              } 
            />
            <Route 
              path="/chat/:username" 
              element={
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.5 }}
                >
                  <ChatSimple 
                    currentUser={currentUser}
                    audioManager={audioManager}
                    onBack={() => window.history.back()}
                  />
                </motion.div>
              } 
            />
          </Routes>
        </AnimatePresence>
      </AppContainer>
    </Router>
  );
};

export default App;
