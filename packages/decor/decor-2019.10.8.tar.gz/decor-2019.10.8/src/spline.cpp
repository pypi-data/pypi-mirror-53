#include "spline.h"
#include "bispev.h"
#include <QFile>
#include <QDebug>

Spline::~Spline() {
    delete[] m_x_knots_x;
    delete[] m_x_knots_y;
    delete[] m_y_knots_x;
    delete[] m_y_knots_y;
    delete[] m_x_coeff;
    delete[] m_y_coeff;
}

bool Spline::parse(const QString &filename) {
    QFile file(filename);
    if (!file.open(QIODevice::ReadOnly)) {
        m_error = file.errorString();
        return false;
    }
    QTextStream s(&file);
    for (m_i = 1; !s.atEnd(); ++m_i) {
        const QString &line = s.readLine().trimmed();
        if (line == QStringLiteral("VALID REGION") && !parseValidRegion(&s))
            return false;
        else if (line == QStringLiteral("GRID SPACING, X-PIXEL SIZE, Y-PIXEL SIZE") && !parsePixels(&s))
            return false;
        else if (line == QStringLiteral("X-DISTORTION") && !parseDistortion(&s, X))
            return false;
        else if (line == QStringLiteral("Y-DISTORTION") && !parseDistortion(&s, Y))
            return false;
    }
    if (m_x_max == 0 || m_y_max == 0 || !m_x_knots_y_size) {
        m_error = QStringLiteral("not a spline file");
        return false;
    }
    return true;
}

QString Spline::errorString() const {
    return m_error;
}

bool Spline::parseValidRegion(QTextStream *s) {
    double *pointers[4] = {&m_x_min, &m_y_min, &m_x_max, &m_y_max};
    return parseFloatLine(s, pointers, 4);
}

bool Spline::parsePixels(QTextStream *s) {
    double *pointers[3] = {&m_grid, &m_pixel1, &m_pixel2};
    return parseFloatLine(s, pointers, 3);
}

bool Spline::parseFloatLine(QTextStream *s, double **pointers, int size) {
    ++m_i;
    QString str = s->readLine();
    const QString &line = rStrip(str);
    if (line.size() != size * FloatItemSize) {
        qDebug() << line.size() << size * FloatItemSize;
        m_error = QStringLiteral("spline corrupted at line %1: %2").arg(QString::number(m_i), line);
        return false;
    }
    for (int i = 0; i < size; ++i) {
        bool ok;
        QStringRef part(&line, i * FloatItemSize, FloatItemSize);
        *pointers[i] = part.trimmed().toDouble(&ok);
        if (!ok) {
            m_error = QStringLiteral("spline corrupted at line %1: failed not convert to float number").arg(m_i);
            return false;
        }
    }
    return true;
}

QString &Spline::rStrip(QString &str) {
    for (int n = str.size() - 1; n >= 0; --n)
        if (!str.at(n).isSpace()) {
            str.truncate(n + 1);
            break;
        }
    return str;
}

bool Spline::operator==(const Spline &other) const {
    if (!(m_x_min == other.m_x_min &&
          m_x_max == other.m_x_max &&
          m_y_min == other.m_y_min &&
          m_y_max == other.m_y_max &&
          m_grid == other.m_grid &&
          m_pixel1 == other.m_pixel1 &&
          m_pixel2 == other.m_pixel2))
        return false;
    if (m_x_coeff_size != other.m_x_coeff_size ||
        m_x_knots_x_size != other.m_x_knots_x_size ||
        m_x_knots_y_size != other.m_x_knots_y_size)
        return false;
    if (m_y_coeff_size != other.m_y_coeff_size ||
        m_y_knots_x_size != other.m_y_knots_x_size ||
        m_y_knots_y_size != other.m_y_knots_y_size)
        return false;
    for (int i = 0; i < m_x_knots_x_size; ++i)
        if (m_x_knots_x[i] != other.m_x_knots_x[i])
            return false;
    for (int i = 0; i < m_x_knots_y_size; ++i)
        if (m_x_knots_y[i] != other.m_x_knots_y[i])
            return false;
    for (int i = 0; i < m_x_coeff_size; ++i)
        if (m_x_coeff[i] != other.m_x_coeff[i])
            return false;
    for (int i = 0; i < m_y_knots_x_size; ++i)
        if (m_y_knots_x[i] != other.m_y_knots_x[i])
            return false;
    for (int i = 0; i < m_y_knots_y_size; ++i)
        if (m_y_knots_y[i] != other.m_y_knots_y[i])
            return false;
    for (int i = 0; i < m_y_coeff_size; ++i)
        if (m_y_coeff[i] != other.m_y_coeff[i])
            return false;
    return true;
}

bool Spline::parseIntLine(QTextStream *s, int **pointers, int size) {
    ++m_i;
    const QString &line = s->readLine();
    const QStringList &sline = line.split(' ', QString::SkipEmptyParts);
    if (sline.size() != size) {
        m_error = QStringLiteral("corrupted line %1: %2").arg(QString::number(m_i), line);
        return false;
    }
    for (int i = 0; i < size; ++i) {
        bool ok;
        *pointers[i] = sline[i].toInt(&ok);
        if (!ok) {
            m_error = QStringLiteral("failed to convert to int in line %1: %2").arg(QString::number(m_i), line);
            return false;
        }
    }
    return true;
}

bool Spline::parseDistortion(QTextStream *s, Spline::Distortion type) {
    int x, y;
    int *pointers[2] = {&x, &y};
    if (!parseIntLine(s, pointers, 2))
        return false;
    QVarLengthArray<double> data;
    for (; !s->atEnd(); ++m_i) {
        QString str = s->readLine();
        const QString &line = rStrip(str);
        if (line.isEmpty())
            break;
        if (line.size() % FloatItemSize != 0) {
            m_error = QStringLiteral("corrupted spline at line %1: %2").arg(QString::number(m_i), line);
            return false;
        }
        for (int i = 0; i < line.size(); i += FloatItemSize) {
            QStringRef part(&line, i, FloatItemSize);
            bool ok;
            data.append(part.toDouble(&ok));
            if (!ok) {
                m_error = QStringLiteral("spline corrupted at line %1: failed not convert to float number").arg(m_i);
                return false;
            }
        }
    }
    if (x < SplineOrder || y < SplineOrder || data.size() < x + y) {
        m_error = QStringLiteral("failed to parse spline: not enough coefficients");
        return false;
    }
    switch (type) {
        case X:
            setX(x, y, data);
            break;
        case Y:
            setY(x, y, data);
            break;
    }
    return true;
}

void Spline::setX(int x, int y, const QVarLengthArray<double> &data) {
    m_x_knots_x_size = x;
    m_x_knots_y_size = y;
    m_x_coeff_size = data.size() - x - y;
    delete[] m_x_knots_x;
    m_x_knots_x = new double[m_x_knots_x_size];
    memcpy(m_x_knots_x, data.constData(), m_x_knots_x_size * sizeof(double));
    delete[] m_x_knots_y;
    m_x_knots_y = new double[m_x_knots_y_size];
    memcpy(m_x_knots_y, data.constData() + x, m_x_knots_y_size * sizeof(double));
    delete[] m_x_coeff;
    m_x_coeff = new double[m_x_coeff_size];
    memcpy(m_x_coeff, data.constData() + x + y, m_x_coeff_size * sizeof(double));
}

void Spline::setY(int x, int y, const QVarLengthArray<double> &data) {
    m_y_knots_x_size = x;
    m_y_knots_y_size = y;
    m_y_coeff_size = data.size() - x - y;
    delete[] m_y_knots_x;
    m_y_knots_x = new double[m_y_knots_x_size];
    memcpy(m_y_knots_x, data.constData(), m_y_knots_x_size * sizeof(double));
    delete[] m_y_knots_y;
    m_y_knots_y = new double[m_y_knots_y_size];
    memcpy(m_y_knots_y, data.constData() + x, m_y_knots_y_size * sizeof(double));
    delete[] m_y_coeff;
    m_y_coeff = new double[m_y_coeff_size];
    memcpy(m_y_coeff, data.constData() + x + y, m_y_coeff_size * sizeof(double));
}

QVector<double> Spline::dx(int dim1, int dim2) const {
    ++dim1;
    ++dim2;
    QVector<double> res(dim1 * dim2);
    spline_coefs s;
    s.dim1 = dim2,
    s.dim2 = dim1,
    s.tx = m_x_knots_x,
    s.tx_size = m_x_knots_x_size,
    s.ty = m_x_knots_y,
    s.ty_size = m_x_knots_y_size,
    s.c = m_x_coeff,
    s.c_size = m_x_coeff_size;
    if (bisplev(&s, res.data()) < 0)
        return QVector<double>();
    for (int i = 0; i < dim1; ++i) {
        const int n = i * dim2;
        for (int j = 0; j < dim2; ++j)
            res[n + j] += j;
    }
    return res;
}

QVector<double> Spline::dy(int dim1, int dim2) const {
    ++dim1;
    ++dim2;
    QVector<double> res(dim1 * dim2);
    spline_coefs s;
    s.dim1 = dim2,
    s.dim2 = dim1,
    s.tx = m_y_knots_x,
    s.tx_size = m_y_knots_x_size,
    s.ty = m_y_knots_y,
    s.ty_size = m_y_knots_y_size,
    s.c = m_y_coeff,
    s.c_size = m_y_coeff_size;
    if (bisplev(&s, res.data()) < 0)
        return QVector<double>();
    for (int i = 0; i < dim1; ++i) {
        const int n = i * dim2;
        for (int j = 0; j < dim2; ++j)
            res[n + j] += i;
    }
    return res;
}
