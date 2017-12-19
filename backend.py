# TODO: keep in mind that this class uses PyQt and it extends QObject
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')

from gi.repository import GObject, Gst, GstBase, GObject
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot

class MusicPlayer(QObject):
   # declare a new signal
   eosReached = pyqtSignal()

   def __init__(self):
      QObject.__init__(self)
      # Initialize the GStreamer framework
      Gst.init(None)
      # initialize playbin element to reproduce different audio encoding
      self.player = Gst.ElementFactory.make("playbin", "player")

      # set the initial default value to 0.5
      self.player.set_property('volume', 0.5)

      # flag used to switch between play and pause
      self.playing = False
      # the current (or last) song being played
      self.current_song = None

      # connect the signal with the slot
      self.eosReached.connect(self.next_song)

      if (not self.player):
         print 'Not all elements could be created. Cannot create a Gstreamer pipeline to stream songs...'
         exit(-1)

      #self.pipeline.add(self.player)
      print "Created GStreamer playbin backend, default volume set to 0.5..."

      bus = self.player.get_bus()
      #bus.enable_sync_message_emission()
      bus.add_signal_watch()
      # message::tag should give us only the tags
      bus.connect("message", self.on_message)


   def load_audio(self, audio_uri):
      # audioResource is the full path of the song in the file system
      self.current_song = audio_uri
      #print self.current_song
      self.stop_audio()
      #self.audio_source.set_property('location', audioResource)
      self.player.set_property('uri', "file://" + self.current_song)
      self.play_audio()


   def play_audio(self):
      # Play the song
      #self.pipeline.set_state(gst.STATE_PLAYING)
      self.player.set_state(Gst.State.PLAYING)
      self.playing = True
      print "Playing audio.."


      '''self.bus = self.pipeline.get_bus()

      self.msg = self.bus.timed_pop_filtered(gst.CLOCK_TIME_NONE,
                  gst.MESSAGE_ERROR | gst.MESSAGE_EOS)'''


   def pause_audio(self):
      #self.pipeline.set_state(gst.STATE_PAUSED)
      self.player.set_state(Gst.State.PAUSED)
      self.playing = False
      print "Pausing audio.."


   def stop_audio(self):
      self.player.set_state(Gst.State.READY)
      self.playing = False
      print "Stopping audio.."


   def play_pause_audio(self):
      if self.current_song is not None:
         if self.playing:
            self.pause_audio()
         else:
            self.play_audio()
      else:
         print "A song must be selected.."

   def reload_audio(self):
       if self.current_song is not None:
           self.load_audio(self.current_song)

   def next_song(self):
       print "Next song must be played.."

   def set_volume(self, volume):
       self.player.set_property('volume', volume)


   def on_message(self, bus, message):
      #print message.type
      if message.type == Gst.MessageType.ERROR:
         error_msg = message.parse_error()
         print error_msg
      if message.type == Gst.MessageType.EOS:
         # here the pipeline has reached the EOS, i.e. a song has been played
         self.eosReached.emit()
