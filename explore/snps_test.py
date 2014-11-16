import unittest

from . import snps

class Snps(unittest):

    def setUp(self):
        # Using demo data for "Lily Mendel"
        self._exp_len = 2266424
        self._snps_lily = Snps('/home/jkern/data/genomic/23andme/lily_mendel.txt')
    
    def test_check_loci(self):
        # last genotype
        loc = self._exp_len - 2
        self.assertEqual(self._snps_lily.genotype_loci(loc), "__") 

        # Mucolipidosis type IV, an autosomal recessive neurodegenerative lysosomal storage disorder
        # 1065758	rs104886461	19	7591645
        self.assertEqual(self._snps_lily.genotype_loci(1065758), "__") 

