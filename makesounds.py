import synthesizer
from synthesizer import Writer,Synthesizer,Waveform

synthesizer=Synthesizer(osc1_waveform=Waveform.sine,osc1_volume=1.0,use_osc2=False)

#from synthesizer import Writer
writer = Writer()

chord = [["C4"],["D4"],["E4"],["F4"],["G4"],["A4"],["B4"],["C5"]]
for i in range(len(chord)):
    wave = synthesizer.generate_chord(chord[i], 2.0)
    #writer.write_wave("path/to/your.wav", wave)
    writer.write_wave(file_path=r"joc project\\sounds\\short\\" + str(i) + ".wav", wave=wave)
    wave = synthesizer.generate_chord(chord[i], 4.0)
    writer.write_wave(file_path=r"joc project\\sounds\\long\\" + str(i) + ".wav", wave=wave)