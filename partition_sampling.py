import os
import sys
from Bio import SeqIO

def seqlen(file):
    FastaFile = open(file, 'rU')
    seqLen=0
    for rec in SeqIO.parse(FastaFile, 'fasta'):
        name = rec.id
        seq = rec.seq
        seqLen = len(rec)
        break
    return seqLen

def check_empty(file):
    if(os.stat(file).st_size == 0):
        return True
    return False    


def check_sample(sample):
    FastaFile = open(sample, 'rU')
    for rec in SeqIO.parse(FastaFile, 'fasta'):
        seq = rec.seq 
        if(seq.find('a')==-1 or seq.find('t')==-1 or seq.find('g')==-1 or seq.find('c')==-1):
            FastaFile.close()
            return False
        FastaFile.close()
        return True    
    

def marge_samples(prev_folder,temp_folder,concat_folder,partition_file):
    with open(partition_file,'a') as ptf:
        for i in range(1,101):
            sample_name='sample'+str(i)+'.aln.fasta'
            file1=prev_folder+'/'+sample_name
            file2=temp_folder+'/'+sample_name
            newfile=concat_folder+'/'+sample_name
            if(check_sample(file2)):
                command='seqkit concat '+file1+' '+file2+' > '+newfile
                os.system(command)
                len_f=seqlen(file2)
                ptf.write('sample%s %s'%(i,str(len_f)))
                ptf.write("\n")
            else:
                command='cp '+file1+' '+newfile
                os.system(command)    

start_fileindex=int(sys.argv[1])
end_fileindex=int(sys.argv[2])

partition_file='partition_'+str(start_fileindex)+'.txt'

files=[]
with open("filteredAlns.file.txt",'r') as f:
    for line in f:
        fname=line.split("\n")[0]
        files.append(fname)
files.pop(0)
length=len(files)

alignment=files[start_fileindex]
temp_folder=str(start_fileindex)+'_tmp'
command1='mkdir '+temp_folder
os.system(command1)

path1='/mnt/scratch/alaminmd/finch/rawr-study-datasets-and-scripts-master/data/empirical/Lamichhaney-2015/'

rawr_command='python '+path1+'software/sampleSeq/sampleSeq.py -a '+path1+ str(alignment)+' -m RAWR -o sample -n 100 --RAWR 0.1'
cd_command='cd '+temp_folder
os.chdir(temp_folder)
os.system(rawr_command)
for i in range(1,101):
    command='mafft sample'+str(i)+'.seq.fasta > sample'+str(i)+'.aln.fasta'
    os.system(command)

os.chdir('../')

prev_folder=temp_folder

with open(partition_file,'a') as ptf:
    for i in range(1,101):
        sample_name='sample'+str(i)+'.aln.fasta'
        file1=prev_folder+'/'+sample_name
        len_f=seqlen(file1)
        ptf.write('sample%s %s'%(i,str(len_f)))
        ptf.write("\n")

for f_num in range(start_fileindex+1,end_fileindex+1):
    alignment=files[f_num]
    if(check_empty(alignment)==False):
        temp_folder=str(f_num)+'_tmp'
        command1='mkdir '+temp_folder
        os.system(command1)
        rawr_command='python '+path1+'software/sampleSeq/sampleSeq.py -a '+path1+ str(alignment)+' -m RAWR -o sample -n 100 --RAWR 0.1'
        cd_command='cd '+temp_folder
        os.chdir(temp_folder)
        os.system(rawr_command)
        for i in range(1,101):
            command='mafft sample'+str(i)+'.seq.fasta > sample'+str(i)+'.aln.fasta'
            os.system(command)        
        os.chdir('../')
        concat_folder=str(f_num)+'_concat'
        concat_folder_command='mkdir '+concat_folder
        os.system(concat_folder_command)
        marge_samples(prev_folder,temp_folder,concat_folder,partition_file)

        delcommand='rm -r '+prev_folder+' '+temp_folder
        os.system(delcommand)
        prev_folder=concat_folder    
            
