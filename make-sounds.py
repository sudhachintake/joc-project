import synthesizer
from synthesizer import Writer,Synthesizer,Waveform

synthesizer=Synthesizer(osc1_waveform=Waveform.sine,osc1_volume=1.0,use_osc2=False)

#from synthesizer import Writer
writer = Writer()

#sargam notes
chord = [["C4"],["D4"],["E4"],["F4"],["G4"],["A4"],["B4"],["C5"]]

#generating notes
for i in range(len(chord)):
    #writing each note
    wave = synthesizer.generate_chord(chord[i], 0.5)
    writer.write_wave(file_path=r"JOCProject\spacegem-python\sounds\short\\" + str(i) + ".wav", wave=wave)
    wave = synthesizer.generate_chord(chord[i], 1.0)
    writer.write_wave(file_path=r"JOCProject\spacegem-python\sounds\\long\\" + str(i) + ".wav", wave=wave)
