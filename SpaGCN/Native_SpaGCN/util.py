import numpy as np
import scanpy as sc


def prefilter_genes(adata,min_counts=None,max_counts=None,min_cells=10,max_cells=None):
    if min_cells is None and min_counts is None and max_cells is None and max_counts is None:
        raise ValueError('Provide one of min_counts, min_genes, max_counts or max_genes.')
    id_tmp=np.asarray([True]*adata.shape[1],dtype=bool)
    id_tmp=np.logical_and(id_tmp,sc.pp.filter_genes(adata.X,min_cells=min_cells)[0]) if min_cells is not None  else id_tmp
    id_tmp=np.logical_and(id_tmp,sc.pp.filter_genes(adata.X,max_cells=max_cells)[0]) if max_cells is not None  else id_tmp
    id_tmp=np.logical_and(id_tmp,sc.pp.filter_genes(adata.X,min_counts=min_counts)[0]) if min_counts is not None  else id_tmp
    id_tmp=np.logical_and(id_tmp,sc.pp.filter_genes(adata.X,max_counts=max_counts)[0]) if max_counts is not None  else id_tmp
    adata._inplace_subset_var(id_tmp)

def filter_panelgenes(adata,gene_name):
    id_index = []
    for i in range(len(gene_name)):
        id_tmp = np.where(adata.var_names == gene_name[i])[0][0]
        id_index.append(id_tmp)
    del id_tmp
    adata._inplace_subset_var(id_index)  # index np.where

def del_panelgenes(adata,gene_name):
    original_list = list(range(len(adata.var_names)))
    id_index = []
    for i in range(len(gene_name)):
        id_tmp = np.where(adata.var_names == gene_name[i])[0][0]
        id_index.append(id_tmp)
    del id_tmp
    remain_index = np.delete(original_list, id_index).tolist()
    adata._inplace_subset_var(remain_index)
