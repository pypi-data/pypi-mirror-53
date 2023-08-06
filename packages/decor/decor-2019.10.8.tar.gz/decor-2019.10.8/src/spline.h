#ifndef DECOR_SPLINE_H
#define DECOR_SPLINE_H

#include <QString>
#include <QVector>
#include <QTextStream>

class Spline {
public:
    Spline() = default;

    virtual ~Spline();

    bool parse(const QString &filename);

    QString errorString() const;

    bool operator==(const Spline &other) const;

    QVector<double> dx(int dim1, int dim2) const;

    QVector<double> dy(int dim1, int dim2) const;

    inline double xMax() const { return m_x_max; };

    inline double xMin() const { return m_x_min; };

    inline double yMax() const { return m_y_max; };

    inline double yMin() const { return m_y_min; };

    inline double grid() const { return m_grid; };

    inline double pixel1() const { return m_pixel1; };

    inline double pixel2() const { return m_pixel2; };

    inline int xKnotsXSize() const { return m_x_knots_x_size; };

    inline int xKnotsYSize() const { return m_x_knots_y_size; };

    inline int yKnotsXSize() const { return m_y_knots_x_size; };

    inline int yKnotsYSize() const { return m_y_knots_y_size; };

    inline int xCoeffSize() const { return m_x_coeff_size; };

    inline int yCoeffSize() const { return m_y_coeff_size; };

    inline const double *xKnotsX() const { return m_x_knots_x; };

    inline const double *xKnotsY() const { return m_x_knots_y; };

    inline const double *yKnotsX() const { return m_y_knots_x; };

    inline const double *yKnotsY() const { return m_y_knots_y; };

    inline const double *xCoeff() const { return m_x_coeff; };

    inline const double *yCoeff() const { return m_y_coeff; };

private:
    static const int FloatItemSize = 14;
    static const int SplineOrder = 4;

    enum Distortion {
        X,
        Y,
    };

    double m_x_max = 0;
    double m_x_min = 0;
    double m_y_max = 0;
    double m_y_min = 0;
    double m_grid = 0;
    double m_pixel1 = 0;
    double m_pixel2 = 0;
    double *m_x_knots_x = nullptr;
    int m_x_knots_x_size = 0;
    double *m_x_knots_y = nullptr;
    int m_x_knots_y_size = 0;
    double *m_x_coeff = nullptr;
    int m_x_coeff_size = 0;
    double *m_y_knots_x = nullptr;
    int m_y_knots_x_size = 0;
    double *m_y_knots_y = nullptr;
    int m_y_knots_y_size = 0;
    double *m_y_coeff = nullptr;
    int m_y_coeff_size = 0;
    int m_i = 0;
    QString m_error;

    bool parseValidRegion(QTextStream *s);

    bool parseDistortion(QTextStream *s, Distortion type);

    bool parseFloatLine(QTextStream *s, double **pointers, int size);

    bool parseIntLine(QTextStream *s, int **pointers, int size);

    bool parsePixels(QTextStream *s);

    static QString &rStrip(QString &str);

    void setX(int x, int y, const QVarLengthArray<double> &data);

    void setY(int x, int y, const QVarLengthArray<double> &data);
};


#endif //DECOR_SPLINE_H
