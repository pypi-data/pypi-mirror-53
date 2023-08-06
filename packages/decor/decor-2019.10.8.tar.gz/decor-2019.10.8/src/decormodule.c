#include "distortion.h"
#include "bispev.h"
#include "bitmask.h"
#include <Python.h>


typedef struct {
    PyObject_HEAD
    bitmask *mask;
} _bitmask;


static int
_bitmask_init(_bitmask *self, PyObject *args) {
    int size;
    PyObject *array;
    Py_buffer buf;
    bitmask *mask;

    if (!PyArg_ParseTuple(args, "O", &array))
        return -1;
    destroy_bitmask(self->mask);
    if (PyObject_GetBuffer(array, &buf, PyBUF_C_CONTIGUOUS) < 0) {
        PyErr_SetString(PyExc_ValueError, "could not get a buffer from the numpy array");
        return -1;
    }
    if (buf.itemsize != sizeof(int8_t)) {
        PyBuffer_Release(&buf);
        PyErr_SetString(PyExc_ValueError, "numpy array type must be int8");
        return -1;
    }
    size = (int) (buf.len / buf.itemsize);
    Py_BEGIN_ALLOW_THREADS
        mask = alloc_bitmask(size, buf.buf);
    Py_END_ALLOW_THREADS
    PyBuffer_Release(&buf);
    if (!mask) {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate memory for bitmask");
        return -1;
    }
    self->mask = mask;
    return 0;
}


static void
_bitmask_dealloc(_bitmask *self) {
    destroy_bitmask(self->mask);
    Py_TYPE(self)->tp_free((PyObject *) self);
}


static int
_bitmask_getbuffer(PyObject *obj, Py_buffer *view, int flags) {
    (void) flags;
    if (view == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer");
        return -1;
    }
    _bitmask *self = (_bitmask *) obj;
    view->obj = (PyObject *) self;
    view->buf = (void *) self->mask->array;
    view->len = (Py_ssize_t) self->mask->len;
    view->readonly = 1;
    view->itemsize = sizeof(char);
    view->format = "c";
    view->ndim = 0;
    view->shape = NULL;
    view->strides = NULL;
    view->suboffsets = NULL;
    view->internal = NULL;
    Py_INCREF(self);
    return 0;
}


static PyBufferProcs _bitmask_as_buffer = {
        (getbufferproc) _bitmask_getbuffer,
        (releasebufferproc) 0,
};

static PyTypeObject _bitmask_type = {
        PyVarObject_HEAD_INIT(NULL, 0)
        "_decor._bitmask",                          /* tp_name */
        sizeof(_bitmask),                           /* tp_basicsize */
        0,                                          /* tp_itemsize */
        (destructor) _bitmask_dealloc,              /* tp_dealloc */
        0,                                          /* tp_print */
        0,                                          /* tp_getattr */
        0,                                          /* tp_setattr */
        0,                                          /* tp_reserved */
        0,                                          /* tp_repr */
        0,                                          /* tp_as_number */
        0,                                          /* tp_as_sequence */
        0,                                          /* tp_as_mapping */
        0,                                          /* tp_hash  */
        0,                                          /* tp_call */
        0,                                          /* tp_str */
        0,                                          /* tp_getattro */
        0,                                          /* tp_setattro */
        &_bitmask_as_buffer,                        /* tp_as_buffer */
        Py_TPFLAGS_DEFAULT,                         /* tp_flags */
        "_bitmask object",                          /* tp_doc */
        0,                                          /* tp_traverse */
        0,                                          /* tp_clear */
        0,                                          /* tp_richcompare */
        0,                                          /* tp_weaklistoffset */
        0,                                          /* tp_iter */
        0,                                          /* tp_iternext */
        0,                                          /* tp_methods */
        0,                                          /* tp_members */
        0,                                          /* tp_getset */
        0,                                          /* tp_base */
        0,                                          /* tp_dict */
        0,                                          /* tp_descr_get */
        0,                                          /* tp_descr_set */
        0,                                          /* tp_dictoffset */
        (initproc) _bitmask_init,                   /* tp_init */
        0,                                          /* tp_alloc */
        PyType_GenericNew,                          /* tp_new */
};


typedef struct {
    PyObject_HEAD
    distortion *dist;
} _distortion;


static int
_distortion_init(_distortion *self, PyObject *args) {
    int dim1, dim2;
    PyObject *dx;
    PyObject *dy;
    Py_buffer bdx, bdy;
    distortion *dist;

    if (!PyArg_ParseTuple(args, "iiOO", &dim1, &dim2, &dx, &dy))
        return -1;

    if (PyObject_GetBuffer(dx, &bdx, PyBUF_C_CONTIGUOUS) < 0) {
        PyErr_SetString(PyExc_RuntimeError, "could not get dx buffer");
        return -1;
    }
    if (PyObject_GetBuffer(dy, &bdy, PyBUF_C_CONTIGUOUS) < 0) {
        PyErr_SetString(PyExc_RuntimeError, "could not get dy buffer");
        return -1;
    }
    Py_BEGIN_ALLOW_THREADS
        distortion_destroy(self->dist);
        dist = distortion_init(dim1, dim2, bdx.buf, bdy.buf);
    Py_END_ALLOW_THREADS
    PyBuffer_Release(&bdx);
    PyBuffer_Release(&bdy);

    if (dist == NULL) {
        PyErr_SetString(PyExc_MemoryError, "could not allocate memory for lookup tables");
        return -1;
    }
    self->dist = dist;
    return 0;
}


static void
_distortion_dealloc(_distortion *self) {
    distortion_destroy(self->dist);
    Py_TYPE(self)->tp_free((PyObject *) self);
}


static PyTypeObject _distortion_type = {
        PyVarObject_HEAD_INIT(NULL, 0)
        "_decor._distortion",                       /* tp_name */
        sizeof(_distortion),                        /* tp_basicsize */
        0,                                          /* tp_itemsize */
        (destructor) _distortion_dealloc,           /* tp_dealloc */
        0,                                          /* tp_print */
        0,                                          /* tp_getattr */
        0,                                          /* tp_setattr */
        0,                                          /* tp_reserved */
        0,                                          /* tp_repr */
        0,                                          /* tp_as_number */
        0,                                          /* tp_as_sequence */
        0,                                          /* tp_as_mapping */
        0,                                          /* tp_hash  */
        0,                                          /* tp_call */
        0,                                          /* tp_str */
        0,                                          /* tp_getattro */
        0,                                          /* tp_setattro */
        0,                                          /* tp_as_buffer */
        Py_TPFLAGS_DEFAULT,                         /* tp_flags */
        "_distortion object",                       /* tp_doc */
        0,                                          /* tp_traverse */
        0,                                          /* tp_clear */
        0,                                          /* tp_richcompare */
        0,                                          /* tp_weaklistoffset */
        0,                                          /* tp_iter */
        0,                                          /* tp_iternext */
        0,                                          /* tp_methods */
        0,                                          /* tp_members */
        0,                                          /* tp_getset */
        0,                                          /* tp_base */
        0,                                          /* tp_dict */
        0,                                          /* tp_descr_get */
        0,                                          /* tp_descr_set */
        0,                                          /* tp_dictoffset */
        (initproc) _distortion_init,                /* tp_init */
        0,                                          /* tp_alloc */
        PyType_GenericNew,                          /* tp_new */
};


typedef struct {
    PyObject_HEAD
    double *corrected;
    Py_ssize_t shape[2];
    Py_ssize_t strides[2];
} _distortion_cor;


static int
_distortion_cor_init(_distortion_cor *self, PyObject *args) {
    PyObject *np_image;
    _distortion *py_distortion;
    Py_buffer image;
    double *res;

    if (!PyArg_ParseTuple(args, "OO", &py_distortion, &np_image))
        return -1;

    free(self->corrected);
    self->corrected = NULL;
    if (PyObject_GetBuffer(np_image, &image, PyBUF_C_CONTIGUOUS) < 0) {
        PyErr_SetString(PyExc_RuntimeError, "could not get buffer for image");
        return -1;
    }
    if (!(res = malloc(image.len))) {
        PyErr_SetString(PyExc_MemoryError, "failed to allocate memory for corrected image");
        return -1;
    }
    Py_BEGIN_ALLOW_THREADS
        memset(res, 0, image.len);
        distortion_correct(py_distortion->dist, image.buf, res);
    Py_END_ALLOW_THREADS
    self->corrected = res;
    self->shape[0] = image.shape[0];
    self->shape[1] = image.shape[1];
    self->strides[0] = image.shape[0] * sizeof(double);
    self->strides[1] = sizeof(double);
    PyBuffer_Release(&image);
    return 0;
}


static void
_distortion_cor_dealloc(_distortion_cor *self) {
    free(self->corrected);
    Py_TYPE(self)->tp_free((PyObject *) self);
}


static int
_distortion_cor_getbuffer(PyObject *obj, Py_buffer *view, int flags) {
    (void) flags;
    if (view == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer");
        return -1;
    }
    _distortion_cor *self = (_distortion_cor *) obj;
    view->obj = (PyObject *) self;
    view->buf = (void *) self->corrected;
    view->len = self->shape[0] * self->shape[1] * sizeof(double);
    view->readonly = 1;
    view->itemsize = sizeof(double);
    view->format = "d";
    view->ndim = 2;
    view->shape = self->shape;
    view->strides = self->strides;
    view->suboffsets = NULL;
    view->internal = NULL;
    Py_INCREF(self);
    return 0;
}

static PyBufferProcs _distortion_cor_as_buffer = {
        (getbufferproc) _distortion_cor_getbuffer,
        (releasebufferproc) 0,
};

static PyTypeObject _distortion_cor_type = {
        PyVarObject_HEAD_INIT(NULL, 0)
        "_decor._distortion_cor",                   /* tp_name */
        sizeof(_distortion_cor),                    /* tp_basicsize */
        0,                                          /* tp_itemsize */
        (destructor) _distortion_cor_dealloc,       /* tp_dealloc */
        0,                                          /* tp_print */
        0,                                          /* tp_getattr */
        0,                                          /* tp_setattr */
        0,                                          /* tp_reserved */
        0,                                          /* tp_repr */
        0,                                          /* tp_as_number */
        0,                                          /* tp_as_sequence */
        0,                                          /* tp_as_mapping */
        0,                                          /* tp_hash  */
        0,                                          /* tp_call */
        0,                                          /* tp_str */
        0,                                          /* tp_getattro */
        0,                                          /* tp_setattro */
        &_distortion_cor_as_buffer,                 /* tp_as_buffer */
        Py_TPFLAGS_DEFAULT,                         /* tp_flags */
        "_distortion_cor object",                   /* tp_doc */
        0,                                          /* tp_traverse */
        0,                                          /* tp_clear */
        0,                                          /* tp_richcompare */
        0,                                          /* tp_weaklistoffset */
        0,                                          /* tp_iter */
        0,                                          /* tp_iternext */
        0,                                          /* tp_methods */
        0,                                          /* tp_members */
        0,                                          /* tp_getset */
        0,                                          /* tp_base */
        0,                                          /* tp_dict */
        0,                                          /* tp_descr_get */
        0,                                          /* tp_descr_set */
        0,                                          /* tp_dictoffset */
        (initproc) _distortion_cor_init,             /* tp_init */
        0,                                          /* tp_alloc */
        PyType_GenericNew,                          /* tp_new */
};


typedef struct {
    PyObject_HEAD
} _bispev;


static void add_one(double *array, int axis, int dim1, int dim2) {
    int i, j, n;

    switch (axis) {
        case 0:
            for (i = 0; i < dim1; ++i) {
                n = i * dim2;
                for (j = 0; j < dim2; ++j)
                    array[n + j] += j;
            }
            break;
        case 1:
            for (i = 0; i < dim1; ++i) {
                n = i * dim2;
                for (j = 0; j < dim2; ++j)
                    array[n + j] += i;
            }
            break;
        default:
            return;
    }
}


static int
_bispev_init(_bispev *self, PyObject *args) {
    (void) self;
    int dim1, dim2, ret, axis;
    PyObject *tx, *ty, *c, *res;
    Py_buffer _tx, _ty, _c, _res;
    spline_coefs b;

    if (!PyArg_ParseTuple(args, "OOOiiOi", &tx, &ty, &c, &dim1, &dim2, &res, &axis))
        return -1;
    b.dim1 = dim1;
    b.dim2 = dim2;
    if (PyObject_GetBuffer(tx, &_tx, PyBUF_C_CONTIGUOUS) < 0) {
        PyErr_SetString(PyExc_RuntimeError, "could not get buffer for tx");
        return -1;
    }
    if (PyObject_GetBuffer(ty, &_ty, PyBUF_C_CONTIGUOUS) < 0) {
        PyErr_SetString(PyExc_RuntimeError, "could not get buffer for ty");
        return -1;
    }
    if (PyObject_GetBuffer(c, &_c, PyBUF_C_CONTIGUOUS) < 0) {
        PyErr_SetString(PyExc_RuntimeError, "could not get buffer for c");
        return -1;
    }
    if (PyObject_GetBuffer(res, &_res, PyBUF_C_CONTIGUOUS) < 0) {
        PyErr_SetString(PyExc_RuntimeError, "could not get buffer for res");
        return -1;
    }
    b.tx = _tx.buf;
    b.tx_size = _tx.shape[0];
    b.ty = _ty.buf;
    b.ty_size = _ty.shape[0];
    b.c = _c.buf;
    b.c_size = _c.shape[0];
    Py_BEGIN_ALLOW_THREADS
        ret = bisplev(&b, _res.buf);
        add_one(_res.buf, axis, dim1, dim2);
    Py_END_ALLOW_THREADS
    if (ret < 0) {
        PyErr_SetString(PyExc_MemoryError, "failed to allocate memory for spline calculations");
        return -1;
    }
    PyBuffer_Release(&_tx);
    PyBuffer_Release(&_ty);
    PyBuffer_Release(&_c);
    PyBuffer_Release(&_res);
    return 0;
}


static void
_bispev_dealloc(_bispev *self) {
    Py_TYPE(self)->tp_free((PyObject *) self);
}


static PyTypeObject _bispev_type = {
        PyVarObject_HEAD_INIT(NULL, 0)
        "_decor._bispev",                           /* tp_name */
        sizeof(_bispev),                            /* tp_basicsize */
        0,                                          /* tp_itemsize */
        (destructor) _bispev_dealloc,               /* tp_dealloc */
        0,                                          /* tp_print */
        0,                                          /* tp_getattr */
        0,                                          /* tp_setattr */
        0,                                          /* tp_reserved */
        0,                                          /* tp_repr */
        0,                                          /* tp_as_number */
        0,                                          /* tp_as_sequence */
        0,                                          /* tp_as_mapping */
        0,                                          /* tp_hash  */
        0,                                          /* tp_call */
        0,                                          /* tp_str */
        0,                                          /* tp_getattro */
        0,                                          /* tp_setattro */
        0,                                          /* tp_as_buffer */
        Py_TPFLAGS_DEFAULT,                         /* tp_flags */
        "_bispev object",                           /* tp_doc */
        0,                                          /* tp_traverse */
        0,                                          /* tp_clear */
        0,                                          /* tp_richcompare */
        0,                                          /* tp_weaklistoffset */
        0,                                          /* tp_iter */
        0,                                          /* tp_iternext */
        0,                                          /* tp_methods */
        0,                                          /* tp_members */
        0,                                          /* tp_getset */
        0,                                          /* tp_base */
        0,                                          /* tp_dict */
        0,                                          /* tp_descr_get */
        0,                                          /* tp_descr_set */
        0,                                          /* tp_dictoffset */
        (initproc) _bispev_init,                    /* tp_init */
        0,                                          /* tp_alloc */
        PyType_GenericNew,                          /* tp_new */
};


static PyMethodDef _decor_methods[] = {
        {NULL, NULL, 0, NULL}
};


struct module_state {
    PyObject *error;
};


#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))


static int _decor_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}


static int _decor_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "_decor",
        NULL,
        sizeof(struct module_state),
        _decor_methods,
        NULL,
        _decor_traverse,
        _decor_clear,
        NULL
};


PyMODINIT_FUNC PyInit__decor(void) {
    PyObject *module;
    struct module_state *st;

    if (PyType_Ready(&_distortion_type) < 0)
        return NULL;
    if (PyType_Ready(&_distortion_cor_type) < 0)
        return NULL;
    if (PyType_Ready(&_bispev_type) < 0)
        return NULL;
    if (PyType_Ready(&_bitmask_type) < 0)
        return NULL;

    module = PyModule_Create(&moduledef);
    if (module == NULL)
        return NULL;
    st = GETSTATE(module);
    st->error = PyErr_NewException("_decor.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&_distortion_type);
    PyModule_AddObject(module, "_distortion", (PyObject *) &_distortion_type);
    Py_INCREF(&_distortion_cor_type);
    PyModule_AddObject(module, "_distortion_cor", (PyObject *) &_distortion_cor_type);
    Py_INCREF(&_bispev_type);
    PyModule_AddObject(module, "_bispev", (PyObject *) &_bispev_type);
    Py_INCREF(&_bitmask_type);
    PyModule_AddObject(module, "_bitmask", (PyObject *) &_bitmask_type);

    return module;
}
