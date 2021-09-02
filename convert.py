import sequence_pb2
import os
from termcolor import colored as col
from time import process_time
currentfile = 0
sequencedir = os.listdir(os.getcwd())
while currentfile < (len(sequencedir)):
    if sequencedir[currentfile].endswith('.sequence'):
        currentname = os.path.basename(sequencedir[currentfile])
        print(col('Found Sequence:', 'cyan'), col(currentname, 'magenta'))
        currentout = open(currentname + '.txt', 'w+')
        f = open(sequencedir[currentfile], 'rb')
        starttime = process_time()
        sequence = sequence_pb2.Sequence()
        sequence.ParseFromString(f.read())
        currentout.write(str(sequence))
        f.close()
        currentout.close()
        stoptime = process_time()
        print(col('Processed', 'cyan'), col(currentname, 'magenta') + col('!', 'cyan'), col('(Time Elapsed:', 'cyan'), col(stoptime, 'magenta'), col('seconds)', 'cyan'))
        print(col('Output:', 'cyan'), col(currentname + '.txt', 'magenta'))
    currentfile = currentfile + 1
