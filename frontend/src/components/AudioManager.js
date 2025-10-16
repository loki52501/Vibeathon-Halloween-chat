class AudioManager {
  constructor() {
    this.audioContext = null;
    this.backgroundMusic = null;
    this.isPlaying = false;
    this.currentPitch = 1.0;
    this.volume = 0.3;
    this.init();
  }

  async init() {
    try {
      // Create audio context
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
      
      // Create background music using Web Audio API
      this.createBackgroundMusic();
    } catch (error) {
      console.error('Failed to initialize audio:', error);
    }
  }

  createBackgroundMusic() {
    if (!this.audioContext) return;

    // Create a spooky ambient sound using oscillators
    const createSpookyTone = (frequency, type = 'sine', delay = 0) => {
      const oscillator = this.audioContext.createOscillator();
      const gainNode = this.audioContext.createGain();
      const filter = this.audioContext.createBiquadFilter();
      const reverb = this.audioContext.createConvolver();

      oscillator.type = type;
      oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);

      // Add some spooky filtering
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(800, this.audioContext.currentTime);
      filter.Q.setValueAtTime(1, this.audioContext.currentTime);

      // Create volume envelope for spooky effect
      const startTime = this.audioContext.currentTime + delay;
      gainNode.gain.setValueAtTime(0, startTime);
      gainNode.gain.linearRampToValueAtTime(0.1 * this.volume, startTime + 2);
      gainNode.gain.linearRampToValueAtTime(0.05 * this.volume, startTime + 4);
      gainNode.gain.linearRampToValueAtTime(0, startTime + 6);

      oscillator.connect(filter);
      filter.connect(gainNode);
      gainNode.connect(this.audioContext.destination);

      return { oscillator, gainNode, startTime };
    };

    // Create multiple spooky tones with more variety
    this.backgroundMusic = {
      tones: [],
      intervals: [],
      start: () => {
        if (this.isPlaying) return;
        
        this.isPlaying = true;
        
        // Create a more complex spooky ambient sequence
        const createAmbientSequence = () => {
          const frequencies = [55, 110, 220, 330, 440]; // More frequencies
          const types = ['sine', 'triangle', 'sawtooth', 'square'];
          
          frequencies.forEach((freq, index) => {
            const tone = createSpookyTone(
              freq * this.currentPitch, 
              types[index % types.length],
              index * 0.3
            );
            this.backgroundMusic.tones.push(tone);
            tone.oscillator.start(tone.startTime);
          });

          // Add some random spooky effects
          if (Math.random() > 0.7) {
            const randomFreq = 50 + Math.random() * 200;
            const randomTone = createSpookyTone(randomFreq * this.currentPitch, 'sawtooth', 2);
            this.backgroundMusic.tones.push(randomTone);
            randomTone.oscillator.start(randomTone.startTime);
          }
        };

        createAmbientSequence();

        // Schedule next sequence with random timing
        const nextDelay = 6000 + Math.random() * 4000; // 6-10 seconds
        const interval = setTimeout(() => {
          if (this.isPlaying) {
            this.backgroundMusic.stop();
            this.backgroundMusic.start();
          }
        }, nextDelay);
        
        this.backgroundMusic.intervals.push(interval);
      },
      
      stop: () => {
        if (!this.isPlaying) return;
        
        this.isPlaying = false;
        
        // Stop all oscillators
        this.backgroundMusic.tones.forEach(tone => {
          try {
            tone.oscillator.stop();
          } catch (e) {
            // Oscillator might already be stopped
          }
        });
        this.backgroundMusic.tones = [];
        
        // Clear all intervals
        this.backgroundMusic.intervals.forEach(interval => {
          clearTimeout(interval);
        });
        this.backgroundMusic.intervals = [];
      },
      
      setPitch: (pitch) => {
        this.currentPitch = Math.max(0.3, Math.min(3.0, pitch));
        if (this.isPlaying) {
          this.backgroundMusic.stop();
          this.backgroundMusic.start();
        }
      }
    };
  }

  startMusic() {
    if (this.backgroundMusic && !this.isPlaying) {
      this.backgroundMusic.start();
    }
  }

  stopMusic() {
    if (this.backgroundMusic && this.isPlaying) {
      this.backgroundMusic.stop();
    }
  }

  setPitch(pitch) {
    this.currentPitch = Math.max(0.5, Math.min(2.0, pitch));
    if (this.backgroundMusic) {
      this.backgroundMusic.setPitch(this.currentPitch);
    }
  }

  setVolume(volume) {
    this.volume = Math.max(0, Math.min(1, volume));
  }

  // Play sound effects
  playSound(type) {
    if (!this.audioContext) return;

    const oscillator = this.audioContext.createOscillator();
    const gainNode = this.audioContext.createGain();

    switch (type) {
      case 'success':
        oscillator.frequency.setValueAtTime(523, this.audioContext.currentTime); // C5
        oscillator.frequency.setValueAtTime(659, this.audioContext.currentTime + 0.1); // E5
        oscillator.frequency.setValueAtTime(784, this.audioContext.currentTime + 0.2); // G5
        break;
      case 'error':
        oscillator.frequency.setValueAtTime(200, this.audioContext.currentTime);
        oscillator.frequency.setValueAtTime(150, this.audioContext.currentTime + 0.1);
        oscillator.frequency.setValueAtTime(100, this.audioContext.currentTime + 0.2);
        break;
      case 'warning':
        oscillator.frequency.setValueAtTime(400, this.audioContext.currentTime);
        oscillator.frequency.setValueAtTime(300, this.audioContext.currentTime + 0.1);
        break;
      default:
        oscillator.frequency.setValueAtTime(440, this.audioContext.currentTime); // A4
    }

    oscillator.type = 'sine';
    gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.5);

    oscillator.connect(gainNode);
    gainNode.connect(this.audioContext.destination);

    oscillator.start(this.audioContext.currentTime);
    oscillator.stop(this.audioContext.currentTime + 0.5);
  }

  cleanup() {
    this.stopMusic();
    if (this.audioContext) {
      this.audioContext.close();
    }
  }
}

export default AudioManager;
