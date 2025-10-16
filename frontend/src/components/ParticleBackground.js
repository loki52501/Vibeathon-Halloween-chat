import React, { useEffect, useRef } from 'react';
import styled from 'styled-components';

const ParticleContainer = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
  overflow: hidden;
`;

const Particle = styled.div`
  position: absolute;
  background: ${props => props.color || 'rgba(255, 255, 255, 0.1)'};
  border-radius: 50%;
  animation: float ${props => props.duration || 20}s infinite linear;
  width: ${props => props.size || 4}px;
  height: ${props => props.size || 4}px;
  
  @keyframes float {
    0% {
      transform: translateY(100vh) rotate(0deg);
      opacity: 0;
    }
    10% {
      opacity: 1;
    }
    90% {
      opacity: 1;
    }
    100% {
      transform: translateY(-100vh) rotate(360deg);
      opacity: 0;
    }
  }
`;

const ParticleBackground = () => {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const createParticle = () => {
      const particle = document.createElement('div');
      const size = Math.random() * 6 + 2;
      const duration = Math.random() * 20 + 15;
      const left = Math.random() * 100;
      const colors = [
        'rgba(255, 0, 0, 0.1)',
        'rgba(255, 215, 0, 0.1)',
        'rgba(255, 255, 255, 0.1)',
        'rgba(128, 0, 128, 0.1)',
        'rgba(0, 255, 0, 0.1)'
      ];
      const color = colors[Math.floor(Math.random() * colors.length)];

      particle.style.position = 'absolute';
      particle.style.background = color;
      particle.style.borderRadius = '50%';
      particle.style.width = `${size}px`;
      particle.style.height = `${size}px`;
      particle.style.left = `${left}%`;
      particle.style.animation = `float ${duration}s infinite linear`;
      particle.style.animationDelay = `${Math.random() * 5}s`;

      container.appendChild(particle);

      // Remove particle after animation
      setTimeout(() => {
        if (particle.parentNode) {
          particle.parentNode.removeChild(particle);
        }
      }, duration * 1000);
    };

    // Create initial particles
    for (let i = 0; i < 20; i++) {
      setTimeout(createParticle, i * 1000);
    }

    // Create new particles periodically
    const interval = setInterval(createParticle, 2000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  return <ParticleContainer ref={containerRef} />;
};

export default ParticleBackground;
