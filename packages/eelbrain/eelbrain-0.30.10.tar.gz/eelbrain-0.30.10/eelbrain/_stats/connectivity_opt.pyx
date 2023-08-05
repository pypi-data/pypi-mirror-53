# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
#cython: boundscheck=False, wraparound=False

from libc.stdlib cimport malloc, free
import numpy as np
cimport numpy as np


ctypedef np.uint32_t UINT32
ctypedef np.int64_t INT64
ctypedef np.float64_t FLOAT64

def merge_labels(np.ndarray[UINT32, ndim=2] cmap,
                 long n_labels_in,
                 np.ndarray[UINT32, ndim=2] edges,
                 np.ndarray[INT64, ndim=1] edge_start,
                 np.ndarray[INT64, ndim=1] edge_stop):
    """Merge adjacent labels with non-standard connectivity

    Parameters
    ----------
    cmap : array of int, ndim=2
        Array with labels, labels are merged along the second axis; cmap is
        modified in-place.
    n_labels_in : int
        Number of labels in cmap.
    edges : array of int (n_edges, 2)
        Edges of the connectivity graph.
    """
    n_labels_in += 1

    cdef unsigned int slice_i, i, dst_i, edge_i
    cdef unsigned int n_vert = cmap.shape[0]
    cdef unsigned int n_slices = cmap.shape[1]
    cdef unsigned int label, connected_label, src, dst
    cdef unsigned int relabel_src, relabel_dst

    cdef unsigned int* relabel = <unsigned int*> malloc(sizeof(unsigned int) * n_labels_in)
    for i in range(n_labels_in):
        relabel[i] = i

    # find targets for relabeling
    for slice_i in range(n_slices):
        for src in range(n_vert):
            label = cmap[src, slice_i]
            if label == 0:
                continue

            for edge_i in range(edge_start[src], edge_stop[src]):
                dst = edges[edge_i, 1]
                connected_label = cmap[dst, slice_i]
                if connected_label == 0:
                    continue

                while relabel[label] < label:
                    label = relabel[label]

                while relabel[connected_label] < connected_label:
                    connected_label = relabel[connected_label]

                if label > connected_label:
                    relabel_src = label
                    relabel_dst = connected_label
                else:
                    relabel_src = connected_label
                    relabel_dst = label

                relabel[relabel_src] = relabel_dst

    # find lowest labels
    cdef int n_labels_out = -1
    for i in range(n_labels_in):
        relabel_dst = relabel[i]
        if relabel_dst == i:
            n_labels_out += 1
        else:
            while relabel[relabel_dst] < relabel_dst:
                relabel_dst = relabel[relabel_dst]
            relabel[i] = relabel_dst

    # relabel cmap
    for i in range(n_vert):
        for slice_i in range(n_slices):
            label = cmap[i, slice_i]
            if label != 0:
                relabel_dst = relabel[label]
                if relabel_dst != label:
                    cmap[i, slice_i] = relabel_dst

    # find all label ids in cmap
    cdef np.ndarray[UINT32, ndim=1] out = np.empty(n_labels_out, dtype=np.uint32)
    dst_i = 0
    for i in range(1, n_labels_in):
        if i == relabel[i]:
            out[dst_i] = i
            dst_i += 1

    free(relabel)
    return out


def tfce_increment(np.ndarray[UINT32, ndim=1] labels,
                   np.ndarray[UINT32, ndim=1] label_image,
                   np.ndarray[FLOAT64, ndim=1] image,
                   double e, double h_factor):
    cdef unsigned int i, cid
    cdef unsigned int n = image.shape[0]
    cdef unsigned int n_labels = labels.max() + 1

    cdef double* area = <double*> malloc(sizeof(double) * n_labels)

    # initialize area
    for i in range(n_labels):
        area[i] = 0.

    # determine area
    for i in range(n):
        cid = label_image[i]
        if cid > 0:
            area[cid] += 1.

    # determine TFCE value
    for cid in labels:
        area[cid] = area[cid] ** e * h_factor

    # update TFCE image
    for i in range(n):
        cid = label_image[i]
        if cid > 0:
            image[i] += area[cid]

    free(area)
