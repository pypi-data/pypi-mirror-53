#ifndef DECOR_GEODISTORTION_H
#define DECOR_GEODISTORTION_H

#include "spline.h"
#include "distortion.h"

class Distortion {
public:
    Distortion() = default;

    virtual ~Distortion();

    QVector<double> correct(int dim1, int dim2, const QVector<double> &image);

    bool openSpline(const QString &filename);

    inline QString errorString() const { return m_error; };

protected:
    int m_dim1 = 0;
    int m_dim2 = 0;
    Spline *m_spline = nullptr;
    distortion *m_d = nullptr;
    QString m_error;
};


#endif //DECOR_GEODISTORTION_H
