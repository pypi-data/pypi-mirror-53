# $BEGIN_AUDIOMATH_LICENSE$
# 
# This file is part of the audiomath project, a Python package for
# recording, manipulating and playing sound files.
# 
# Copyright (c) 2008-2019 Jeremy Hill
# 
# audiomath is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/ .
# 
# The audiomath distribution includes binaries from the third-party
# AVbin and PortAudio projects, released under their own licenses.
# See the respective copyright, licensing and disclaimer information
# for these projects in the subdirectories `audiomath/_wrap_avbin`
# and `audiomath/_wrap_portaudio` . It also includes a fork of the
# third-party Python package `pycaw`, released under its original
# license (see `audiomath/pycaw_fork.py`).
# 
# $END_AUDIOMATH_LICENSE$

__all__ = [
	'ffmpeg',
]

import os
import re
import sys
import time
import wave
import shlex
import struct
import shutil
import threading
import subprocess

from . import Base;  from .Base import Sound, Silence, ACROSS_SAMPLES
from . import Meta; from .Meta import FindFile, PackagePath
from . import Dependencies; from .Dependencies import numpy

def EndianSwap( s, nbytes ):
	if   nbytes == 1 or sys.byteorder == 'little': return s
	elif nbytes == 2: fmt = 'H'
	elif nbytes == 4: fmt = 'L'
	else: raise ValueError( "failed to swap endianness for %d-byte values" % nbytes )
	fmt = str( int( len(s) / nbytes ) ) + fmt
	return struct.pack( '<' + fmt, *struct.unpack( '>' + fmt, s ) )

def ReadWav(self, filename):
	wf = wave.open( filename, 'rb' )
	nbytes = wf.getsampwidth()
	nchan = wf.getnchannels()
	nsamp = wf.getnframes()
	fs = wf.getframerate()
	comptype = ( wf.getcomptype(), wf.getcompname() )
	strdat = wf.readframes( nsamp )
	wf.close()
	strdat = EndianSwap( strdat, nbytes )
	self.bits = nbytes * 8
	self.fs = fs
	self.filename = os.path.realpath( filename )
	self.compression = comptype
	self.y = self.str2dat( strdat, nsamp, nchan )
	if strdat != self.dat2str():
		print( "warning: data mismatch in %r" % self )
	return self

def WriteWav( self, filename=None, headerOnly=False ):
	"""
	Write the sound waveform in uncompressed `'.wav'`
	format, to the specified `filename`.  If `filename`
	is unspecified, `self.filename` is used, if present.
	"""
	if filename is None: filename = self.filename
	if filename is None: raise TypeError( 'no filename supplied' )
	wf = wave.open( filename, 'wb' )
	wf.setsampwidth( self.nbytes )
	wf.setnchannels( self.NumberOfChannels() )
	#wf.setnframes( self.NumberOfSamples() )
	wf.setframerate( self.fs )
	wf.setcomptype( *self.compression )
	if headerOnly:
		self._wavFileHandleOpenForWriting = wf
	else:
		s = self.dat2str()
		s = EndianSwap( s, self.nbytes )
		wf.writeframes( s )
		wf.close()
	if not isinstance( filename, str ):
		try: filename = filename.name
		except: pass
	self.filename = os.path.realpath( filename ) if isinstance( filename, str ) else None
	return self

def AppendWavFrames( self, data ):
	# h = am.Recorder(10, start=0)
	# def hook( data, *blx ): href().Set( head=0 ).sound.Append( data ) 
	# import weakref; href = weakref.ref( h ); h.sound.Write('blah.wav', headerOnly=1); h.hook = hook; h.Record() 
	# h.Stop(); h.hook = None; h.sound._wavFileHandleOpenForWriting.close()
	wf = self._wavFileHandleOpenForWriting
	if not wf: raise ValueError( 'no wav file open for appending' )
	wf.writeframes( EndianSwap( self.dat2str( data ), self.nbytes ) )

def AppendRaw( self, data, fileHandle, translateNumericType=False, ensureLittleEndian=False ):
	nbytes = None
	if translateNumericType:
		data = self.dat2str( data )
		nbytes = self.nbytes
	elif hasattr( data, 'tostring' ):
		data = data.tostring()
		nbytes = data.dtype.itemsize
	if ensureLittleEndian and nbytes:
		data = EndianSwap( data, nbytes )
	fileHandle.write( data )

avbin = None
def Load_AVBin( tolerateFailure=False ):
	global avbin
	if avbin: return avbin
		
	from . import _wrap_avbin as avbin # nowadays, this will simply throw an exception if it fails
	if avbin: return avbin
	
	# ...but here's the old logic, just in case we every want to reinstate the pyglet-based fallback
	if 'pyglet' not in sys.modules: os.environ[ 'PYGLET_SHADOW_WINDOW' ] = '0'
	try: import pyglet.media.sources.avbin as avbin
	except: pass
	if avbin: return avbin
	try: import pyglet.media.avbin as avbin
	except: pass
	if avbin: return avbin
		
	if avbin: print( 'failed to import _wrap_avbin submodule - falling back on pyglet' )
	elif not tolerateFailure: raise ImportError( 'failed to import avbin either from _wrap_avbin or pyglet (is pyglet installed?)' )
	return avbin
	
def Read_AVBin( self, filename, duration=None, verbose=False ):
	if not avbin: Load_AVBin()
	sourceHandle = avbin.AVbinSource( filename )
	self.bits = sourceHandle.audio_format.sample_size
	self.fs = int( sourceHandle.audio_format.sample_rate )
	numberOfChannels = int( sourceHandle.audio_format.channels )
	bytesPerSample = int( sourceHandle.audio_format.bytes_per_sample )
	if duration is None: duration = sourceHandle.duration
	else: duration = min( duration, sourceHandle.duration )
	totalNumberOfSamples = int( round( duration * self.fs ) )
	cumulativeNumberOfSamples = 0
	self.filename = os.path.realpath( filename )
	subsDst = [ slice( None ), slice( None ) ]
	subsSrc = [ slice( None ), slice( None ) ]
	if verbose: print( 'reserving space for %g sec: %d channels, %d samples @ %g Hz = %g MB' % ( duration, numberOfChannels, totalNumberOfSamples, self.fs, totalNumberOfSamples * numberOfChannels * 4 / 1024 ** 2.0 ) )
	y = Silence( totalNumberOfSamples, numberOfChannels, 'float32' )
	t0 = 0.0
	while cumulativeNumberOfSamples < totalNumberOfSamples:
		if verbose:
			t = time.time()
			if not t0 or t > t0 + 0.5: t0 = t; print( '    read %.1f%%' % ( 100.0 * cumulativeNumberOfSamples / float( totalNumberOfSamples ) ) )
		dataPacket = sourceHandle.get_audio_data( 4096 )
		if dataPacket is None: break
		numberOfSamplesThisPacket = int( dataPacket.length / bytesPerSample )
		subsDst[ ACROSS_SAMPLES ] = slice( cumulativeNumberOfSamples, cumulativeNumberOfSamples + numberOfSamplesThisPacket )
		subsSrc[ ACROSS_SAMPLES ] = slice( 0, min( numberOfSamplesThisPacket,  totalNumberOfSamples - cumulativeNumberOfSamples ) )
		cumulativeNumberOfSamples += numberOfSamplesThisPacket
		data = self.str2dat( dataPacket.data, numberOfSamplesThisPacket, numberOfChannels )
		y[ tuple( subsDst ) ] = data[ tuple( subsSrc ) ]
	self.y = y
	return self
		
def Read( self, source, raw_dtype=None ):
	"""
	Args:
		source:
			A filename, or a byte string containing raw audio data.
			With filenames, files are decoded according to their file extension,
			unless the `raw_dtype` argument is explicitly specified, in which case files
			are assumed to contain raw data without header, regardless of extension.
			
		raw_dtype (str):
			If supplied, `source` is interpreted either as raw audio data, or
			as the name of a file *containing* raw audio data without a header.
			If `source` is a byte string containing raw audio data, and `raw_dtype` is
			unspecified, `raw_dtype` will default to `self.dtype_encoded`.
			Examples might be `float32` or even `float32*2`---the latter explicitly
			overrides the current value of `self.NumberOfChannels()` and interprets the
			raw data as 2-channel.
			
	"""
	isFileName = False
	for i in range( 32 ):
		try: nonprint = chr( i ) in source
		except: break
		if nonprint: break
	else:
		isFileName = True
	if isFileName:
		resolvedFileName = FindFile( source )
		source = resolvedFileName if resolvedFileName else os.path.realpath( source )
	isExistingFile = isFileName and os.path.isfile( source )
	if isFileName and not isExistingFile: raise IOError( 'could not find file %s' % source )
	
	if not isExistingFile or raw_dtype:
		if isExistingFile:
			self.filename = os.path.realpath( source )
			source = open( source, 'rb' )
		else:
			self.filename = ''
		if hasattr( source, 'read' ): source = source.read()
		nchan = None # default is self.NumberOfChannels()
		if not isinstance( raw_dtype, str ):
			raw_dtype = None  # default will be self.dtype_encoded
		elif '*' in raw_dtype:
			raw_dtype, count = raw_dtype.split( '*', 1 )
			if count: nchan = int( count )
		self.y = self.str2dat( source, nsamp=None, nchan=nchan, dtype=raw_dtype )
		return self
	
	if source.lower().endswith( '.wav' ): return ReadWav( self, source )
	
	return Read_AVBin( self, source )

def Write( self, filename=None ):
	if filename is None: filename = self.filename
	if filename is None: raise TypeError( 'no filename supplied' )
	extension = os.path.splitext( filename )[ -1 ].lower()
	if extension in [ '', '.wav' ]:
		WriteWav( self, filename )
	else:
		if not ffmpeg.IsInstalled(): raise ffmpeg.NotInstalled( 'cannot save in formats other than uncompressed .wav' )
		ffmpeg( filename, source=self )( self )
	return self
	
Sound.Read  = Read
Sound.Write = Write
Sound.Append = AppendWavFrames

class ffmpeg( object ):
	"""
	An instance that connects to the standalone `ffmpeg` executable
	assuming that it `.IsInstalled()`. The instance can be used to
	encode audio data to disk in a variety of formats. There are
	two main applications, illustrated in the following examples.
	Both of them implicitly use `ffmpeg` instances under the hood::
	
	    # saving a Sound in a format other than uncompressed .wav:
	    import audiomath as am
	    s = am.TestSound( '12' )
	    s.Write( 'example_sound.ogg' )
	    
	    # recording direct to disk:
	    import audiomath as am
	    s = am.Record(5, loop=True, filename='example_recording.mp3')
	    
	The latter example uses an `ffmpeg` instance as a callable
	`.hook` of a `Recorder` instance.  For more control (asynchronous
	functionality) you can do it more explicitly as follows::
	
		import audiomath as am
		h = am.Recorder(5, loop=True, start=False)
		h.Record(hook=am.ffmpeg('example_recording.mp3', source=h, verbose=True))
		
		h.Wait() # wait for ctrl-C (replace this line with whatever)
		# ...
		
		h.Stop(hook=None) # garbage-collection of the `ffmpeg` instance is one way to `.Close()` it
		s = h.Cut()
	
	The ffmpeg binary is large, so it is not included in the Python
	package by default. Installation is up to you.  You can install
	it like any other application, somewhere on the system path.
	Alternatively, if you want to, you can put it directly inside
	the `audiomath` package directory, or inside a subdirectory
	called `ffmpeg`---the class method `ffmpeg.Install()` can help
	you do this.  If you install it inside the `audiomath` package,
	then this has two advantages: (a) audiomath will find it there
	when it attempts to launch it, and (b) it will be included in
	the output of `Manifest('pyinstaller')` which you can use to
	help you freeze your application.
	
	See also:
	
		`ffmpeg.Install()`,
		`ffmpeg.IsInstalled()`
	
	"""
	# needs threading, subprocess, shutil, and also re and numpy for GrokFormat
	# TODO: seems to tack 45ms of silence onto the beginning of mp3 files for some reason
	# TODO: output of the example_sound.ogg example can be re-read into memory, but output of second
	#       example (mic-to-disk recording) cannot be re-read if the format is changed to .ogg: avbin.AVbinSource() returns None
	
	executable = 'ffmpeg'
	
	class NotInstalled( RuntimeError ):
		def __init__( self, message='' ):
			if message: message = message.strip() + '\n'
			message += 'You need to install the `ffmpeg` binary manually for this functionality.\nSee `ffmpeg.Install` for more help.'
			super( self.__class__, self ).__init__( message )
	
	@classmethod
	def GetExecutablePath( cls ):
		if os.path.isabs( cls.executable ): return cls.executable
		basename = cls.executable + ( '.exe' if sys.platform.lower().startswith( 'win' ) else '' )
		for candidate in [ PackagePath( basename ), PackagePath( 'ffmpeg', basename ) ]:
			if os.path.isfile( candidate ): return candidate
		return cls.executable
	
	@classmethod
	def Install( cls, pathToDownloadedExecutable, deleteOriginal=False ):
		"""
		The `ffmpeg` binary can be large relative to the rest of
		`audiomath`. Therefore, it is not included by default. You
		should download it from https://ffmpeg.org
		
		If an `ffmpeg` binary is already installed somewhere on
		the operating-system's search path, `audiomath` will find it,
		so you probably will not need this helper function. However,
		if you have just downloaded a statically-linked build of
		ffmpeg, are looking for somewhere to put it, and want to put
		it inside the `audiomath` package directory itself, this
		function will do it for you (it will actually put it inside
		an automatically-created subdirectory called `ffmpeg`).
		audiomath will find it there, and it will also be included
		in the output of `Manifest('pyinstaller')` which helps if
		you want to use `pyinstaller` to freeze your application.
		"""
		pathToDownloadedExecutable = os.path.realpath( pathToDownloadedExecutable )
		old = cls.GetExecutablePath()
		if not os.path.isabs( old ): old = ''
		dst = PackagePath( 'ffmpeg' )
		if not os.path.isdir( dst ): os.makedirs( dst )
		basename = cls.executable + ( '.exe' if sys.platform.lower().startswith( 'win' ) else '' )
		dst = os.path.join( dst, basename )
		if old:
			print( 'removing old file ' + old )
			os.remove( old )
		print( """copying\n    from: %s\n      to: %s""" % ( pathToDownloadedExecutable, dst ) )
		shutil.copy2( pathToDownloadedExecutable, dst )
		if deleteOriginal:
			print( 'removing original ' + pathToDownloadedExecutable )
			os.remove( pathToDownloadedExecutable )
		print( '' )
		
	@classmethod
	def IsInstalled( cls ):
		"""
		Return `True` or `False` depending on whether the `ffmpeg`
		binary executable is installed and accessible, either inside
		the `audiomath` package (see `Install()`) or on the operating
		system's search path.
		
		See also:  `Install()`
		"""
		try: process = subprocess.Popen( [ cls.GetExecutablePath(), '-version' ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
		except OSError: return False
		process.communicate()
		return True

	@classmethod
	def Run( cls, args='', stdin=None ):
		try: process = subprocess.Popen( [ cls.GetExecutablePath() ] + shlex.split( args ), stdin=subprocess.PIPE )
		except OSError: return -1
		process.communicate( stdin )
		return process.returncode

	@staticmethod
	def GrokFormat( format ):
		if not isinstance( format, str ) or not re.match( r'^[fsu](8|(16|24|32|48|64)(le|be))$', format, re.I ):
			dtype = numpy.dtype( format )
			format = '%s%d%s' % (
				's' if dtype.kind == 'i' else dtype.kind,
				dtype.itemsize * 8,
				'' if dtype.itemsize == 1 else 'be' if dtype.byteorder in '>!' or ( dtype.byteorder in '@=' and sys.byteorder != 'little' ) else 'le',
			)
		return format.lower()
		
	def __init__( self, filename, source=None, format=None, nChannels=None, fs=None, kbps=192, transform=None, verbose=False ):
		"""
		Args:
			filename (str):
				output filename---be sure to include the file
				extension so that ffmpeg can infer the desired
				output format;
			
			source (Recorder, Player or Stream):
				optional instance that can intelligently specify
				`format`, `nChannels` and `fs` all in one go;
			
			format (str):
				format of the raw data---should be either a valid
				ffmpeg PCM format string (e.g. `'f32le'`) or a
				construction argument for `numpy.dtype()` (e.g.
				`'float32'`, `'<f4'`);
			
			nChannels (int):
				number of channels to expect in each raw data
				packet.
				
			fs (int, float):
				sampling frequency, in Hz.
			
			kbps (int):
				kilobit rate for encoding.
			
			transform (None, function):
				an optional callable that can receives each data
				packet, along with the sample number and sampling
				frequency, and return a transformed version of the
				data packet to be send to `ffmpeg` in place of the
				original.
			
			verbose (bool):
				whether or not to print the standard output and
				standard error content produced by `ffmpeg`.
		"""
		self.kbps = kbps
		self.filename = filename
		self.verbose = verbose
		self.transform = transform
		
		# NB: interpretation of Stream object attributes is specific to _wrap_portaudio
		
		if not format: # see if source is a Player or Recorder instance, with a Stream instance in source.stream
			try: format = source.stream.sampleFormat[ 'numpy' ]
			except: pass
		if not format: # see if source is itself a Stream instance
			try: format = source.sampleFormat[ 'numpy' ]
			except: pass
		if not format: # see if source is a Sound instance
			try: format = source.dtype_encoded
			except: pass
		if not format:
			format = 'float32'
			
		if not nChannels: # see if source is a Player instance, with a Sound instance in source.sound
			try: nChannels = source.sound.nChannels
			except: pass
		if not nChannels: # see if source is itself a Sound instance
			try: nChannels = source.nChannels
			except: pass
		if not nChannels: # see if source is a Player or Recorder instance, with a Stream instance in source.stream
			try: nChannels = nChannels = source.stream.nInputChannels if source.stream.nInputChannels else source.stream.nOutputChannels
			except: pass
		if not nChannels: # see if source is itself a Stream instance
			try: nChannels = nChannels = source.nInputChannels if source.nInputChannels else source.nOutputChannels
			except: pass
		if not nChannels:
			nChannels = 2
		
		if not fs: # see if source is a Player or Recorder instance, with a Stream instance in source.stream
			try: fs = source.stream.fs
			except: pass
		if not fs: # see if source is a Player instance, with a Sound instance in source.sound
			try: fs = source.sound.fs
			except: pass
		if not fs: # see if source is itself a Sound or Stream instance
			try: fs = source.fs
			except: pass
		if not fs:
			fs = 44100
		
		self.format = self.GrokFormat( format )
		self.nChannels = nChannels
		self.fs = fs
		
		executable = self.GetExecutablePath()
		cmd = [
			executable,
			'-f',   self.format,
			'-ac',  '%d'  % self.nChannels,
			'-ar',  '%g'  % self.fs,
			'-i',   'pipe:',
			'-b:a', '%dk' % kbps,
			'-vn',
			'-y',
			filename,
		]
		if self.verbose: print( ' '.join( cmd ) )
		try: self.process = subprocess.Popen( cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
		except OSError as error: raise OSError( 'failed to launch %s - %s' % ( executable, error ) )
		self.output = []
		threadParams = self.threadParams = dict( processStdout=self.process.stdout, outputList=self.output, keepGoing=True, verbose=self.verbose )
		def Communicate():
			while threadParams[ 'keepGoing' ]:
				try:
					line = threadParams[ 'processStdout' ].readline()
					if not line: break
					if not isinstance( line, str ): line = line.decode( 'utf-8', errors='ignore' ) # NB: encoding could be anything in principle...
					if threadParams[ 'verbose' ]: print( line.rstrip() )
					threadParams[ 'outputList' ].append( line )
				except:
					break
		threading.Thread( target=Communicate ).start()
	def __call__( self, data, sampleNumber=None, fs=None ):
		if not self.process.stdin.closed:
			transform = self.transform
			if transform: data = transform( data, sampleNumber, fs )
			if hasattr( data, 'dat2str' ): data = data.dat2str()
			else: data = data[ :, :self.nChannels ].tostring()
			self.process.stdin.write( data )
	def Close( self ):
		#if self.verbose: print( 'closing %r' % self )
		self.process.stdin.close()
		self.threadParams[ 'keepGoing' ] = False
	def __del__( self ):
		self.Close()

