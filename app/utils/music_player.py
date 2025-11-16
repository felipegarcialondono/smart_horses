import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None
        self.volume = 0.3  # Volumen por defecto (0.0 a 1.0)
        
        # Rutas de música
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.music_path = os.path.join(base_path, "assets", "music")
        self.sounds_path = os.path.join(base_path, "assets", "sounds")
        
        self.music_files = {
            "menu": os.path.join(self.music_path, "menu.mp3"),
            "game": os.path.join(self.music_path, "game.mp3"),
            "victory": os.path.join(self.music_path, "victory.mp3")
        }
        
        # Cargar efectos de sonido
        self.sounds = {}
        self._load_sounds()
    
    def _load_sounds(self):
        """Carga todos los efectos de sonido"""
        sound_files = {
            "move": os.path.join(self.sounds_path, "move.wav"),
            "special": os.path.join(self.sounds_path, "special.wav"),
            "victory": os.path.join(self.sounds_path, "victory.wav"),
            "defeat": os.path.join(self.sounds_path, "defeat.wav"),
            "click": os.path.join(self.sounds_path, "click.wav")
        }
        
        # ✅ Configuración de volumen personalizado para cada sonido
        volume_settings = {
            "move": 0.4,
            "special": 0.6,
            "victory": 0.7,
            "defeat": 0.6,
            "click": 0.9  # ← MÁS ALTO PARA CLICK
        }
        
        for sound_name, sound_file in sound_files.items():
            if os.path.exists(sound_file):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(sound_file)
                    # Aplicar volumen personalizado
                    volume = volume_settings.get(sound_name, 0.5)
                    self.sounds[sound_name].set_volume(volume)
                        
                except Exception as e:
                    print(f"Error al cargar sonido '{sound_name}': {e}")
        
    def play_music(self, music_name, loop=True):
        """Reproduce música de fondo"""
        if music_name not in self.music_files:
            print(f"Música '{music_name}' no encontrada")
            return
        
        music_file = self.music_files[music_name]
        
        if not os.path.exists(music_file):
            print(f"Archivo de música no encontrado: {music_file}")
            return
        
        # Si ya está sonando esta música, no reiniciar
        if self.current_music == music_name and pygame.mixer.music.get_busy():
            return
        
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1 if loop else 0)  # -1 = loop infinito
            self.current_music = music_name
            print(f"♪ Reproduciendo música: {music_name}")
        except Exception as e:
            print(f"Error al reproducir música: {e}")
    
    def play_sound(self, sound_name):
        """Reproduce un efecto de sonido"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Sonido '{sound_name}' no encontrado")
    
    def stop_music(self):
        """Detiene la música"""
        pygame.mixer.music.stop()
        self.current_music = None
    
    def pause_music(self):
        """Pausa la música"""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Reanuda la música"""
        pygame.mixer.music.unpause()
    
    def set_volume(self, volume):
        """Ajusta el volumen de la música (0.0 a 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
    
    def set_sound_volume(self, volume):
        """Ajusta el volumen de los efectos de sonido (0.0 a 1.0)"""
        volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(volume)
    
    def fadeout(self, milliseconds=1000):
        """Hace fade out de la música"""
        pygame.mixer.music.fadeout(milliseconds)