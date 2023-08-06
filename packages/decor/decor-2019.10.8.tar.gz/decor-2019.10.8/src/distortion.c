#include "distortion.h"
#include <math.h>
#include <memory.h>
#include <stdlib.h>
#include <float.h>

struct distortion {
    int dim1;
    int dim2;
    int dim11;
    int dim22;
    int size;
    int size12;
    int lut_size_max;
    int delta0;
    int delta1;
    unsigned long buffer_size;
    int *lut_idx;
    double *buffer;
    double *lut_coef;
    double *corners;
    double *pos;
};

static int clip(int value, int min, int max) {
    if (value < min)
        return min;
    else if (value > max)
        return max;
    else
        return value;
}

static double min4(double a, double b, double c, double d) {
    a = a < b ? a : b;
    c = c < d ? c : d;
    return a < c ? a : c;
}

static double max4(double a, double b, double c, double d) {
    a = a > b ? a : b;
    c = c > d ? c : d;
    return a > c ? a : c;
}

static int calc_lut_size(distortion *d) {
    int i, j, k, l, m, min0, min1, max0, max1, dd, ii, jj, kk, *lut_size;
    double a0, a1, b0, b1, c0, c1, d0, d1;

    if (!(lut_size = calloc(d->size, sizeof(int))))
        return -1;
    dd = d->dim2 * 4 * 2;
    for (i = 0; i < d->dim1; ++i) {
        ii = i * dd;
        for (j = 0; j < d->dim2; ++j) {
            jj = ii + j * 4 * 2;
            a0 = d->pos[jj + 0];
            a1 = d->pos[jj + 1];
            b0 = d->pos[jj + 2];
            b1 = d->pos[jj + 3];
            c0 = d->pos[jj + 4];
            c1 = d->pos[jj + 5];
            d0 = d->pos[jj + 6];
            d1 = d->pos[jj + 7];
            min0 = clip((int) floor(min4(a0, b0, c0, d0)), 0, d->dim1);
            min1 = clip((int) floor(min4(a1, b1, c1, d1)), 0, d->dim2);
            max0 = clip((int) ceil(max4(a0, b0, c0, d0)) + 1, 0, d->dim1);
            max1 = clip((int) ceil(max4(a1, b1, c1, d1)) + 1, 0, d->dim2);
            for (k = min0; k < max0; ++k) {
                kk = k * d->dim2;
                for (l = min1; l < max1; ++l) {
                    m = kk + l;
                    lut_size[m]++;
                    if (lut_size[m] > d->lut_size_max)
                        d->lut_size_max = lut_size[m];
                }
            }
        }
    }
    free(lut_size);
    return 0;
}

static double calc_area(double i1, double i2, double slope, double intercept) {
    return 0.5 * (i2 - i1) * (slope * (i2 + i1) + 2.0 * intercept);
}

static void integrate(distortion *d, double start, double stop, double slope, double intercept) {
    int i, h, idx;
    double p, dp, a, aa, da, sign;

    if (start < stop) {
        p = ceil(start);
        dp = p - start;
        if (p > stop) {
            a = calc_area(start, stop, slope, intercept);
            if (a != 0) {
                aa = fabs(a);
                sign = a / aa;
                da = stop - start;
                for (h = 0; aa > 0; ++h) {
                    if (da > aa) {
                        da = aa;
                        aa = -1;
                    }
                    idx = ((int) floor(start)) * d->delta1 + h;
                    d->buffer[idx] += sign * da;
                    aa -= da;
                }
            }
        } else {
            if (dp > 0) {
                a = calc_area(start, p, slope, intercept);
                if (a != 0) {
                    aa = fabs(a);
                    sign = a / aa;
                    da = dp;
                    for (h = 0; aa > 0; ++h) {
                        if (da > aa) {
                            da = aa;
                            aa = -1;
                        }
                        idx = (((int) floor(p)) - 1) * d->delta1 + h;
                        d->buffer[idx] += sign * da;
                        aa -= da;
                    }
                }
            }
            for (i = (int) floor(p); i < (int) floor(stop); ++i) {
                a = calc_area(i, i + 1, slope, intercept);
                if (a != 0) {
                    aa = fabs(a);
                    sign = a / aa;
                    da = 1.0;
                    for (h = 0; aa > 0; ++h) {
                        if (da > aa) {
                            da = aa;
                            aa = -1;
                        }
                        idx = i * d->delta1 + h;
                        d->buffer[idx] += sign * da;
                        aa -= da;
                    }
                }
            }
            p = floor(stop);
            dp = stop - p;
            if (dp > 0) {
                a = calc_area(p, stop, slope, intercept);
                if (a != 0) {
                    aa = fabs(a);
                    sign = a / aa;
                    da = fabs(dp);
                    for (h = 0; aa > 0; ++h) {
                        if (da > aa) {
                            da = aa;
                            aa = -1;
                        }
                        idx = ((int) floor(p)) * d->delta1 + h;
                        d->buffer[idx] += sign * da;
                        aa -= da;
                    }
                }
            }
        }
    } else if (start > stop) {
        p = floor(start);
        if (stop > p) {
            a = calc_area(start, stop, slope, intercept);
            if (a != 0) {
                aa = fabs(a);
                sign = a / aa;
                da = start - stop;
                for (h = 0; aa > 0; ++h) {
                    if (da > aa) {
                        da = aa;
                        aa = -1;
                    }
                    idx = ((int) floor(start)) * d->delta1 + h;
                    d->buffer[idx] += sign * da;
                    aa -= da;
                }
            }
        } else {
            dp = p - start;
            if (dp < 0) {
                a = calc_area(start, p, slope, intercept);
                if (a != 0) {
                    aa = fabs(a);
                    sign = a / aa;
                    da = fabs(dp);
                    for (h = 0; aa > 0; ++h) {
                        if (da > aa) {
                            da = aa;
                            aa = -1;
                        }
                        idx = ((int) floor(p)) * d->delta1 + h;
                        d->buffer[idx] += sign * da;
                        aa -= da;
                    }
                }
            }
            for (i = (int) start; i > (int) ceil(stop); --i) {
                a = calc_area((double) i, (double) i - 1, slope, intercept);
                if (a != 0) {
                    aa = fabs(a);
                    sign = a / aa;
                    da = 1;
                    for (h = 0; aa > 0; ++h) {
                        if (da > aa) {
                            da = aa;
                            aa = -1;
                        }
                        idx = (i - 1) * d->delta1 + h;
                        d->buffer[idx] += sign * da;
                        aa -= da;
                    }
                }
            }
            p = ceil(stop);
            dp = stop - p;
            if (dp < 0) {
                a = calc_area(p, stop, slope, intercept);
                if (a != 0) {
                    aa = fabs(a);
                    sign = a / aa;
                    da = fabs(dp);
                    for (h = 0; aa > 0; ++h) {
                        if (da > aa) {
                            da = aa;
                            aa = -1;
                        }
                        idx = ((int) floor(stop)) * d->delta1 + h;
                        d->buffer[idx] += sign * da;
                        aa -= da;
                    }
                }
            }
        }
    }
}

static int calc_lut_table(distortion *d) {
    int ml, nl, offset0, offset1, box_size0, box_size1, ms, ns, *out_max;
    int idx, i, j, k, m, n, dd, ii, jj, mms, ddd, mml, mld;
    double a0, a1, b0, b1, c0, c1, d0, d1, pab, pbc, pcd, pda, cab, cbc, ccd, cda, area, value, o0, o1;

    if (!(d->lut_coef = calloc(d->size * d->lut_size_max, sizeof(double))))
        return -1;
    if (!(d->lut_idx = calloc(d->size * d->lut_size_max, sizeof(int))))
        return -1;
    if (!(d->buffer = malloc(d->buffer_size)))
        return -1;
    if (!(out_max = calloc(d->size, sizeof(int))))
        return -1;
    dd = d->dim2 * 4 * 2;
    ddd = d->dim2 * d->lut_size_max;
    for (idx = i = 0; i < d->dim1; ++i) {
        ii = i * dd;
        for (j = 0; j < d->dim2; ++j, ++idx) {
            jj = ii + j * 4 * 2;
            a0 = d->pos[jj + 0];
            a1 = d->pos[jj + 1];
            b0 = d->pos[jj + 2];
            b1 = d->pos[jj + 3];
            c0 = d->pos[jj + 4];
            c1 = d->pos[jj + 5];
            d0 = d->pos[jj + 6];
            d1 = d->pos[jj + 7];
            o0 = floor(min4(a0, b0, c0, d0));
            o1 = floor(min4(a1, b1, c1, d1));
            offset0 = (int) o0;
            offset1 = (int) o1;
            box_size0 = ((int) ceil(max4(a0, b0, c0, d0))) - offset0;
            box_size1 = ((int) ceil(max4(a1, b1, c1, d1))) - offset1;
            a0 -= o0;
            a1 -= o1;
            b0 -= o0;
            b1 -= o1;
            c0 -= o0;
            c1 -= o1;
            d0 -= o0;
            d1 -= o1;
            if (b0 != a0) {
                pab = (b1 - a1) / (b0 - a0);
                cab = a1 - pab * a0;
            } else {
                pab = cab = 0.0;
            }
            if (c0 != b0) {
                pbc = (c1 - b1) / (c0 - b0);
                cbc = b1 - pbc * b0;
            } else {
                pbc = cbc = 0.0;
            }
            if (d0 != c0) {
                pcd = (d1 - c1) / (d0 - c0);
                ccd = c1 - pcd * c0;
            } else {
                pcd = ccd = 0.0;
            }
            if (a0 != d0) {
                pda = (a1 - d1) / (a0 - d0);
                cda = d1 - pda * d0;
            } else {
                pda = cda = 0.0;
            }
            memset(d->buffer, 0, d->buffer_size);
            integrate(d, b0, a0, pab, cab);
            integrate(d, a0, d0, pda, cda);
            integrate(d, d0, c0, pcd, ccd);
            integrate(d, c0, b0, pbc, cbc);
            area = 0.5 * ((c0 - a0) * (d1 - b1) - (c1 - a1) * (d0 - b0));
            for (ms = 0; ms < box_size0; ++ms) {
                ml = ms + offset0;
                if (ml < 0 || ml >= (int) d->dim1)
                    continue;
                mms = ms * d->delta1;
                mml = ml * d->dim2;
                mld = ml * ddd;
                for (ns = 0; ns < box_size1; ++ns) {
                    nl = ns + offset1;
                    if (nl < 0 || nl >= (int) d->dim2)
                        continue;
                    value = d->buffer[mms + ns] / area;
                    if (value <= 0)
                        continue;
                    m = mml + nl;
                    k = out_max[m];
                    n = mld + nl * d->lut_size_max + k;
                    d->lut_idx[n] = idx;
                    d->lut_coef[n] = value;
                    out_max[m] = k + 1;
                }
            }
        }
    }
    free(out_max);
    return 0;
}

static void destroy_aux(distortion *d) {
    if (d) {
        free(d->pos);
        free(d->corners);
        free(d->buffer);
        d->buffer = NULL;
        d->corners = NULL;
        d->pos = NULL;
    }
}

void distortion_destroy(distortion *d) {
    destroy_aux(d);
    if (d) {
        free(d->lut_coef);
        free(d->lut_idx);
        free(d);
    }
}

static int calc_corners(distortion *d, const double *dx, const double *dy) {
    double delta_y, delta_x, delta0 = -DBL_MAX, delta1 = -DBL_MAX;
    int k, i, j, n, l, m;

    if (!(d->corners = malloc(2 * d->size12 * sizeof(double))))
        return -1;
    for (k = i = 0; i < d->dim11; ++i) {
        n = i * d->dim22;
        m = (i - 1) * d->dim22;
        for (j = 0; j < d->dim22; ++j) {
            l = n + j;
            d->corners[k++] = dy[l];
            d->corners[k++] = dx[l];
            if (i > 0) {
                delta_y = ceil(dy[l]) - floor(dy[m + j]);
                if (delta_y > delta0)
                    delta0 = delta_y;
            }
            if (j > 0) {
                delta_x = ceil(dx[l]) - floor(dx[l - 1]);
                if (delta_x > delta1)
                    delta1 = delta_x;
            }
        }
    }
    if (delta0 == -DBL_MAX || delta1 == -DBL_MAX)
        return -1;
    d->delta0 = (int) delta0;
    d->delta1 = (int) delta1;
    d->buffer_size = d->delta0 * d->delta1 * sizeof(double);
    return 0;
}

static int calc_pos(distortion *d) {
    int i, j, k, l, m, n, m1, m2, n1, n2, k1, k2, k3, k4;

    if (!(d->pos = malloc(d->size * 4 * 2 * sizeof(double))))
        return -1;
    for (i = 0; i < d->dim11; ++i) {
        m = i * d->dim22 * 2;
        m1 = i * d->dim2 * 4 * 2;
        m2 = (i - 1) * d->dim2 * 4 * 2;
        for (j = 0; j < d->dim22; ++j) {
            n = m + j * 2;
            n1 = j * 4 * 2;
            n2 = (j - 1) * 4 * 2;
            k1 = m1 + n1 + 0 * 4;
            k2 = m1 + n2 + 1 * 4 - 2;
            k3 = m2 + n2 + 2 * 4 - 4;
            k4 = m2 + n1 + 3 * 4 - 6;
            for (k = 0; k < 2; ++k) {
                l = n + k;
                if (i != d->dim1 && j != d->dim2)
                    d->pos[k1 + k] = d->corners[l];
                if (i != d->dim1 && j != 0)
                    d->pos[k2 + k] = d->corners[l];
                if (i != 0 && j != 0)
                    d->pos[k3 + k] = d->corners[l];
                if (i != 0 && j != d->dim2)
                    d->pos[k4 + k] = d->corners[l];
            }
        }
    }
    return 0;
}

distortion *distortion_init(int dim1, int dim2, const double *dx, const double *dy) {
    distortion *d;

    if (!(d = malloc(sizeof(distortion))))
        return NULL;
    d->lut_coef = NULL;
    d->lut_idx = NULL;
    d->buffer = NULL;
    d->corners = NULL;
    d->pos = NULL;
    d->dim1 = dim1;
    d->dim2 = dim2;
    d->size = dim1 * dim2;
    d->dim11 = dim1 + 1;
    d->dim22 = dim2 + 1;
    d->size12 = d->dim22 * d->dim11;
    d->lut_size_max = 0;
    if (calc_corners(d, dx, dy) < 0 || calc_pos(d) < 0 || calc_lut_size(d) < 0 || calc_lut_table(d) < 0) {
        distortion_destroy(d);
        return NULL;
    }
    destroy_aux(d);
    return d;
}

void distortion_correct(const distortion *d, const double *image, double *corrected) {
    int k, i, j, m, idx, ii, jj, dd;
    double sum, error, y, t, coef;

    dd = d->dim2 * d->lut_size_max;
    for (i = 0; i < d->dim1; ++i) {
        ii = i * dd;
        for (j = 0; j < d->dim2; ++j) {
            jj = ii + j * d->lut_size_max;
            error = sum = 0;
            for (k = 0; k < d->lut_size_max; ++k) {
                m = jj + k;
                idx = d->lut_idx[m];
                coef = d->lut_coef[m];
                if (coef <= 0 || idx >= d->size)
                    continue;
                y = image[idx] * coef - error;
                t = sum + y;
                error = t - sum - y;
                sum = t;
            }
            corrected[i * d->dim2 + j] += sum;
        }
    }
}
