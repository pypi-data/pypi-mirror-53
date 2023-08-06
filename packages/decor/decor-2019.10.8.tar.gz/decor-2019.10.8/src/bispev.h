#ifndef CDECOR_BISPEV_H_   /* Include guard */
#define CDECOR_BISPEV_H_

/* This is a C library.  Allow compilation with a C++ compiler */
#ifdef __cplusplus
extern "C" {
#endif

typedef struct spline_coefs {
    int dim1;
    int dim2;
    double *tx;
    int tx_size;
    double *ty;
    int ty_size;
    double *c;
    int c_size;
} spline_coefs;

int bisplev(const spline_coefs *coefs, double *z);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // CDECOR_BISPEV_H_
