#ifndef CDECOR_DISTORTION_H_   /* Include guard */
#define CDECOR_DISTORTION_H_

/* This is a C library.  Allow compilation with a C++ compiler */
#ifdef __cplusplus
extern "C" {
#endif

struct distortion;

typedef struct distortion distortion;

distortion *distortion_init(int dim1, int dim2, const double *dx, const double *dy);

void distortion_destroy(distortion *d);

void distortion_correct(const distortion *d, const double *image, double *corrected);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // CDECOR_DISTORTION_H_
