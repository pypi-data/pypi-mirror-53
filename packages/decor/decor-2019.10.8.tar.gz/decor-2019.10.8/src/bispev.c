#include "bispev.h"
#include <stdlib.h>

#ifndef SPLINE_ORDER
#define SPLINE_ORDER 3
#endif

static void fpbspl(const double *t, double x, int l, double *h, double *hh) {
    int i, j;
    double f;

    h[0] = 1;
    for (j = 1; j <= SPLINE_ORDER; ++j) {
        for (i = 0; i < j; ++i)
            hh[i] = h[i];
        h[0] = 0;
        for (i = 0; i < j; ++i) {
            f = hh[i] / (t[l + i] - t[l + i - j]);
            h[i] = h[i] + f * (t[l + i] - x);
            h[i + 1] = f * (x - t[l + i - j]);
        }
    }
}

static void init_aux(const double *t, int size, int dim, int **al, double **aw) {
    int i, j, l, l1, *ll;
    double arg, tb, te, h[6], hh[5], *ww;

    if (size < SPLINE_ORDER + 1)
        return;
    if (!(ll = malloc(dim * sizeof(int))))
        return;
    if (!(ww = malloc(dim * (SPLINE_ORDER + 1) * sizeof(double))))
        return;
    tb = t[SPLINE_ORDER];
    te = t[size - SPLINE_ORDER - 1];
    l = SPLINE_ORDER + 1;
    l1 = l + 1;
    for (i = 0; i < dim; ++i) {
        arg = i;
        if (arg < tb)
            arg = tb;
        if (arg > te)
            arg = te;
        while (!(arg < t[l] || l == (size - SPLINE_ORDER - 1))) {
            l = l1;
            l1 = l + 1;
        }
        fpbspl(t, arg, l, h, hh);
        ll[i] = l - SPLINE_ORDER - 1;
        for (j = 0; j <= SPLINE_ORDER; ++j)
            ww[i * (SPLINE_ORDER + 1) + j] = h[j];
    }
    *al = ll;
    *aw = ww;
}

int bisplev(const spline_coefs *c, double *z) {
    int nky1, i, j, i1, l2, j1;
    double *wx = NULL, *wy = NULL, sp, err, tmp, a;
    int *lx = NULL, *ly = NULL, res = -1;

    nky1 = c->ty_size - SPLINE_ORDER - 1;
    if (nky1 < 0)
        goto cleanup;
    init_aux(c->tx, c->tx_size, c->dim1, &lx, &wx);
    init_aux(c->ty, c->ty_size, c->dim2, &ly, &wy);
    if (!lx || !ly || !wx || !wy || !z)
        goto cleanup;
    for (j = 0; j < c->dim2; ++j) {
        for (i = 0; i < c->dim1; ++i) {
            err = sp = 0;
            for (i1 = 0; i1 < SPLINE_ORDER + 1; ++i1) {
                for (j1 = 0; j1 < SPLINE_ORDER + 1; ++j1) {
                    l2 = lx[i] * nky1 + ly[j] + i1 * nky1 + j1;
                    if (l2 >= c->c_size)
                        continue;
                    a = c->c[l2] * wx[i * (SPLINE_ORDER + 1) + i1] * wy[j * (SPLINE_ORDER + 1) + j1] - err;
                    tmp = sp + a;
                    err = tmp - sp - a;
                    sp = tmp;
                }
            }
            z[j * c->dim1 + i] = sp;
        }
    }
    res = 0;
    cleanup:
    free(wx);
    free(wy);
    free(lx);
    free(ly);
    return res;
}
