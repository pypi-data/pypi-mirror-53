#include "geodistortion.h"

Distortion::~Distortion() {
    distortion_destroy(m_d);
    delete m_spline;
}

QVector<double> Distortion::correct(int dim1, int dim2, const QVector<double> &image) {
    if (!m_spline)
        qFatal("Spline is not initialized");
    if (m_dim1 != dim1 || m_dim2 != dim2) {
        QVector<double> dx = m_spline->dx(dim1, dim2);
        QVector<double> dy = m_spline->dy(dim1, dim2);
        distortion_destroy(m_d);
        m_d = distortion_init(dim1, dim2, dx.constData(), dy.constData());
        if (!m_d)
            return QVector<double>();
        m_dim1 = dim1;
        m_dim2 = dim2;
    }
    QVector<double> corrected(dim1 * dim2);
    distortion_correct(m_d, image.constData(), corrected.data());
    return corrected;
}

bool Distortion::openSpline(const QString &filename) {
    Spline *s = new Spline;
    if (!s->parse(filename)) {
        m_error = s->errorString();
        delete s;
        return false;
    }
    if (m_spline && *m_spline == *s) {
        delete s;
        return true;
    }
    delete m_spline;
    m_spline = s;
    m_dim1 = 0;
    return true;
}
