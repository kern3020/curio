import os

class Snps(object):
    '''Single-Nucleotide Polymorphism(SNP) is a specific position in the
    gemone which varies. 23andMe returns SNPs data as a long string.
    Each SNP is a pair of characters. 
    
    1) A,C, T and G are well-known nucleotides. 
    2) '_' (underbar) is a location which wasn't read. 
    3) '-' (minus) could not be determined 
    4) I insertion, D is deletion

    '''

    def __init__(self, snps_file):
        # open sample data
        with open(snps_file) as fd:
            self._snps_inmemory = fd.read()
        self._snps_length = len(self._snps_inmemory)

        # create index 
        self._index_file = '/home/jkern/data/genomic/23andme/'
        self._snps_index_file = 'snps.data'

    def genotype_sym(sym):
        '''
        Lookup loci based on sym and return genotype pair
        '''
        pass

    def genotype_loci(loci):
        '''
        Return genotype pair at loci.

        Assertion: confirm you get the same results from the Rest API. 

        '''
        # since they are pairs, multiple by 2 to get the
        # right offset
        loci *= 2 
        return self._snps_inmemory[loci:loci+2]

if __name__ == '__main__':
    pass
