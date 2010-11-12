/*
 * Copyright (c) 2001-2006 MUSIC TECHNOLOGY GROUP (MTG)
 *                         UNIVERSITAT POMPEU FABRA
 *
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 */

/* 
David Garcia Garzon
Universitat Pompeu Fabra

Katy Noland
Queen Mary, University of London

Adapted from MATLAB code by Chris Harte at Queen Mary
*/

#define USE_SNDFILE 1

#include <list>
#include <iostream>
#include <fstream>
#include <cmath>
#include "ChordExtractor.hxx"
#include "MonoAudioFileReader.hxx"
#include "AudioInPort.hxx"
#include "AudioOutPort.hxx"
#include "Pool.hxx"
#include "Array.hxx"
#include "enumerated.h"
#include "frame_division.h"
#include "CLAM/DiscontinuousSegmentation.hxx"
#include <CLAM/Assert.hxx>

const char * copyright =
	"Chord extraction v1.0.\n"
	"Copyright 2006 Queen Mary University of London\n"
	"Copyright 2006 Universitat Pompeu Fabra\n"
	"Original algorithm by Chris Harte.\n"
	"Ported to C++ by David Garcia Garzon and Katy Noland.\n"
	"\n"
	;
const char * usage =
	"Usage: ChordExtractor [-s out.sc] [-f <suffix>] [-m <method>] <wavefile1> <wavefile2> ...\n"
	"\nOptions:\n"
	" -h            shows this help\n"
	" -s            dump the schema to the standard output\n"
	" -f <suffix>   append <suffix> to the generated descriptors file (default: '.pool')\n"
	" -m <method>   use the <method> segmentation algorithm\n"
	"\nUsage examples:\n"
	" ChordExtractor -s schema.sc\n"
	" ChordExtractor -f .beats song1.wav song2.mp3 song3.ogg\n"
	;

const char * schemaContent = 
"<?xml version='1.0' encoding='UTF-8' standalone='no' ?>\n"
"<DescriptionScheme>\n"
"\n"
" <Uri>descriptionScheme:www.iua.upf.edu:clam:ChordExtraction</Uri>\n"
"\n"
" <Attributes>\n"
"   <Attribute name='Chords_Harte' scope='Song' type='Segmentation'>\n"
"     <ChildScope>ExtractedChord</ChildScope>\n"
"     <SegmentationPolicy>Discontinuous</SegmentationPolicy>\n"
"   </Attribute>\n"
#if 0
"    <Attribute name='DebugFrameSegments' scope='Song' type='Segmentation'>\n"
"	  <Documentation>\n"
"	  	This segmentation is just to check that the segments and the frames are properly aligned.\n"
"	  </Documentation>\n"
"      <ChildScope></ChildScope>\n"
"      <SegmentationPolicy>Continuous</SegmentationPolicy>\n"
"    </Attribute>\n"
#endif
"    <Attribute name='Frames' scope='Song' type='FrameDivision'>\n"
"      <ChildScope>Frame</ChildScope>\n"
"    </Attribute>\n"
"    <Attribute name='TunningPosition' scope='Frame' type='Float'/>\n"
"    <Attribute name='TunningStrength' scope='Frame' type='Float'/>\n"
"    <Attribute name='FirstChordCandidateRelevance' scope='Frame' type='Float'/>\n"
"    <Attribute name='SecondChordCandidateRelevance' scope='Frame' type='Float'/>\n"
"    <Attribute name='FirstChordIndex' scope='Frame' type='Float'/>\n"
"    <Attribute name='SecondChordIndex' scope='Frame' type='Float'/>\n"
"    <Attribute name='Energy' scope='Frame' type='Float'/>\n"
"	<!--\n"
"    <Attribute name='PrimaryRoot' scope='Frame'type='Enumerated'>\n"
"      <EnumerationValues>A A# B B# C C# D D# E F F# G G#</EnumerationValues>\n"
"    </Attribute>\n"
"    <Attribute name='PrimaryMode' scope='Frame' type='Enumerated'\n"
"      <EnumerationValues>Major Minor Major7 Minor7 Dominant7 MajorMinor7 Diminished Augmented Fifth</EnumerationValues>\n"
"    </Attribute>\n"
"    <Attribute name='SecondaryRoot' scope='Frame' type='Enumerated'>\n"
"      <EnumerationValues>A A# B B# C C# D D# E F F# G G#</EnumerationValues>\n"
"    </Attribute>\n"
"    <Attribute name='SecondaryMode'scope='Frame' type='Enumerated'>\n"
"      <EnumerationValues>Major Minor Major7 Minor7 Dominant7 MajorMinor7 Diminished Augmented Fifth</EnumerationValues>\n"
"    </Attribute>\n"
"	-->\n"
"    <Attribute name='HartePcp' scope='Frame' type='FloatArray'>\n"
"      <BinLabels>G G# A Bb B C C# D Eb E F F#</BinLabels>\n"
"    </Attribute>\n"
"    <Attribute name='HarteChordCorrelation' scope='Frame' type='FloatArray'>\n"
"      <BinLabels>"
"G G#/Ab A A#/Bb B C C#/Db D D#/Eb E F F#/Gb "
"g g#/ab a a#/bb b c c#/db d d#/eb e f f#/gb "
		"</BinLabels>\n"
"    </Attribute>\n"
"    <Attribute name='Root' scope='ExtractedChord' type='Enumerated'>\n"
"      <EnumerationValues>G G# A A# B C C# D D# E F F#</EnumerationValues>\n"
"    </Attribute>\n"
"    <Attribute name='Mode' scope='ExtractedChord' type='Enumerated'>\n"
"      <EnumerationValues>\n"
"         Major Minor Major7 Minor7 Dominant7 MinorMajor7\n"
//"		 Suspended2 Suspended4 Major6 Minor6 6/9\n"
"		 Diminished Diminished7 Augmented Fifth\n"
"      </EnumerationValues>\n"
"    </Attribute>\n"
"  </Attributes>\n"
"\n"
"</DescriptionScheme>\n"
;

int processFile(const std::string & waveFile, const std::string & suffix, unsigned segmentationMethod)
{
	CLAM::MonoAudioFileReaderConfig cfg;
	cfg.SetSourceFile( waveFile );
	CLAM::MonoAudioFileReader reader;
	if (!reader.Configure(cfg))
	{
		std::cerr << "Error reading file '" << waveFile << "'" << std::endl;
		std::cerr << reader.GetConfigErrorMessage() << std::endl;
		return -1;
	}
	CLAM::TData samplingRate = reader.GetHeader().GetSampleRate();
	unsigned long nsamples = reader.GetHeader().GetLength()*samplingRate/1000.0;

	int factor=1;							// downsampling factor
	float minf = 98;						// (MIDI note G1)
	unsigned bpo = 36;			// bins per octave

	Simac::ChordExtractor chordExtractor(samplingRate/factor,minf,bpo);
	chordExtractor.segmentationMethod(segmentationMethod);
	unsigned framesize = chordExtractor.frameSize();
	unsigned hop = chordExtractor.hop();
	unsigned long nFrames = floor((float)(nsamples-framesize+hop)/(float)hop);	// no. of time windows

	std::cout << "Frame size: " << framesize << std::endl;
	std::cout << "Hop size: " << hop << std::endl;

	CLAM::AudioInPort inport;
	reader.GetOutPort(0).ConnectToIn(inport);
	inport.SetSize( framesize );
	inport.SetHop( hop );

	reader.Start();
	CLAM::TData currentFrame = 0;
	unsigned firstFrameOffset = 0;
//	clock_t start = clock();
	std::vector<float> floatBuffer(framesize);
	while (reader.Do())
	{
		if (!inport.CanConsume()) continue; // Not enough audio, try again
		std::cout << "." << std::flush;
		CLAM::TData * segpointer = &(inport.GetAudio().GetBuffer()[0]);
		for (unsigned i = 0; i < framesize; i++)
			floatBuffer[i] = segpointer[i];
		CLAM::TData currentTime = (currentFrame*hop+firstFrameOffset)/samplingRate;
		chordExtractor.doIt(&floatBuffer[0], currentTime);
		inport.Consume();
		currentFrame++;
	}
//	clock_t end = clock();
	reader.Stop();

	std::ofstream outputPool((waveFile+suffix).c_str());

	return 0;
}

int main(int argc, char* argv[])			// access command line arguments
{
	std::cout << copyright << std::endl;
	std::list<std::string> songs;
	std::string suffix = ".pool";
	std::string schemaLocation = "";
	unsigned segmentationMethod = 0;
	if (argc==1) 
	{
		std::cerr << usage << std::endl;
		return 0;
	}

	bool isSchema = false;
	bool isSuffix = false;
	bool isConfiguration = false;
	bool isSegmentationMethod = false;
	for (unsigned i = 1; i<argc; i++)
	{
		std::string parameter = argv[i];
		if (parameter=="-h")
		{
			std::cerr << usage << std::endl;
			return 0;
		}
		else if (isSchema)
		{
			schemaLocation = parameter;
			isSchema=false;
		}
		else if (isSuffix)
		{
			suffix = parameter;
			isSuffix=false;
		}
		else if (isSegmentationMethod)
		{
			segmentationMethod = atoi( argv[i] );
			isSegmentationMethod=false;
		}
		else if (isConfiguration)
		{
			// TODO: Take the configuration file
			isConfiguration=false;
		}
		else if (parameter=="-f") isSuffix = true;
		else if (parameter=="-s") isSchema = true;
		else if (parameter=="-m") isSegmentationMethod = true;
		else if (parameter=="-c") isConfiguration = true;
		else if (parameter=="-w") return 0; // No write back
		else songs.push_back(parameter);
	}

	if (schemaLocation!="")
	{
		std::ofstream schemaFile(schemaLocation.c_str());
		schemaFile << schemaContent;
	}

	for (std::list<std::string>::iterator it = songs.begin();
			it!= songs.end();
			it++)
	{
		int error = processFile(*it, suffix, segmentationMethod);
		if (error) return error;
	}

//	std::cout << "\nProcessing time: " << (end-start)/CLOCKS_PER_SEC << " seconds\n";

	return 0;
}


