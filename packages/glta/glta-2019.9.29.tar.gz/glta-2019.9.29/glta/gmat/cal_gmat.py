import numpy as np
import pandas as pd
import time
from glta.process_plink.process_plink import read_plink, impute_geno


def cal_agmat(bed_file, inv=True, small_val=0.001):
    print("{:#^80}".format("Read the SNP data"))
    snp_mat = read_plink(bed_file)
    if np.any(np.isnan(snp_mat)):
        print('Missing genotypes are imputed with random genotypes.')
        snp_mat = impute_geno(snp_mat)
    print("There are {:d} individuals and {:d} SNPs.".format(snp_mat.shape[0], snp_mat.shape[1]))
    freq = np.sum(snp_mat, axis=0) / (2 * snp_mat.shape[0])
    freq.shape = (1, snp_mat.shape[1])
    scale = 2 * freq * (1 - freq)
    scale = np.sum(scale)
    snp_mat = snp_mat - 2 * freq
    
    print("{:#^80}".format("Calculate the additive genomic relationship matrix"))
    clock_t0 = time.perf_counter()
    cpu_t0 = time.process_time()
    kin = np.dot(snp_mat, snp_mat.T) / scale
    kin_diag = np.diag(kin)
    kin_diag = kin_diag + kin_diag * small_val
    np.fill_diagonal(kin, kin_diag)
    clock_t1 = time.perf_counter()
    cpu_t1 = time.process_time()
    print("Running time: Clock time, {:.5f} sec; CPU time, {:.5f} sec.".format(clock_t1 - clock_t0, cpu_t1 - cpu_t0))
    
    print("{:#^80}".format("Output"))
    ind = np.tril_indices_from(kin)
    val = kin[ind]
    fam_info = pd.read_csv(bed_file + '.fam', sep='\s+', header=None)
    id1 = np.array(fam_info.iloc[ind[0], 1])
    id2 = np.array(fam_info.iloc[ind[1], 1])
    data_df = {'id1': id1, 'id2': id2, 'val': val}
    data_df = pd.DataFrame(data_df, columns=['id1', 'id2', 'val'])
    kin_file = bed_file + '.grm'
    print("The output file is", kin_file)
    data_df.to_csv(kin_file, sep=' ', header=False, index=False)
    
    kin_inv = None
    if inv:
        print("{:#^80}".format("Calculate the inversion of kinship"))
        clock_t0 = time.perf_counter()
        cpu_t0 = time.process_time()
        kin_inv = np.linalg.inv(kin)
        clock_t1 = time.perf_counter()
        cpu_t1 = time.process_time()
        print("Running time: Clock time, {:.5f} sec; CPU time, {:.5f} sec.".format(clock_t1 - clock_t0,
                                                                                   cpu_t1 - cpu_t0))
        
        print("{:#^80}".format("Output the inversion"))
        val = kin_inv[ind]
        data_df = {'id1': id1, 'id2': id2, 'val': val}
        data_df = pd.DataFrame(data_df, columns=['id1', 'id2', 'val'])
        kin_inv_file = bed_file + '.giv'
        print("The output file is", kin_inv_file)
        data_df.to_csv(kin_inv_file, sep=' ', header=False, index=False)
    
    return kin, kin_inv


def cal_ginbreedcoef(bed_file):
    snp_mat = read_plink(bed_file)
    if np.any(np.isnan(snp_mat)):
        print('Missing genotypes are imputed with random genotypes.')
        snp_mat = impute_geno(snp_mat)
    print("There are {:d} individuals and {:d} SNPs.".format(snp_mat.shape[0], snp_mat.shape[1]))
    homo_f = 1 - np.sum(np.abs(snp_mat - 1.0) < 0.01, axis=1) / snp_mat.shape[1]
    freq = np.sum(snp_mat, axis=0) / (2 * snp_mat.shape[0])
    freq.shape = (1, snp_mat.shape[1])
    scale_vec = 2 * freq * (1 - freq)
    scale = np.sum(scale_vec)
    snp_mat = snp_mat - 2 * freq
    grm_f1 = np.sum(np.multiply(snp_mat, snp_mat), axis=1) / scale - 1.0
    grm_f2 = np.sum(np.multiply(snp_mat, snp_mat) / scale_vec, axis=1) / snp_mat.shape[1] - 1.0
    
    fam_info = pd.read_csv(bed_file + '.fam', sep='\s+', header=None)
    id = np.array(fam_info.iloc[:, 1])
    data_df = {'id': id, 'homo_F': homo_f, 'grm_F1': grm_f1, 'grm_F2': grm_f2}
    data_df = pd.DataFrame(data_df, columns=['id', 'homo_F', 'grm_F1', 'grm_F2'])
    out_file = bed_file + '.ginbreedcoef'
    data_df.to_csv(out_file, sep=' ', header=True, index=False)
    