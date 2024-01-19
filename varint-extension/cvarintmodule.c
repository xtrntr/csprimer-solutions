#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *cvarint_encode(PyObject *self, PyObject *args) {
  uint64_t n;
  int i = 0;
  char part, out[10];

  if (!PyArg_ParseTuple(args, "K", &n))
    return NULL;

  while (n > 0) {
    part = n & 0x7F;
    n >>= 7;
    if (n > 0) {
      part |= 0x80;
    }
    out[i++] = part;
  }

  return PyBytes_FromStringAndSize(out, i);
}

static PyObject *cvarint_decode(PyObject *self, PyObject *args) {
  const char *bytes;
  Py_ssize_t length;
  uint64_t rtn = 0;

  if (!PyArg_ParseTuple(args, "y#", &bytes, &length))
    return NULL;
  //printf("bytes = %s\n", bytes);


  for (Py_ssize_t i = length - 1; i >= 0; --i) {
    rtn <<= 7;
    rtn |= (uint8_t)bytes[i] & 0x7f;
  }


  return PyLong_FromUnsignedLongLong(rtn);
}

static PyMethodDef CVarintMethods[] = {
    {"encode", cvarint_encode, METH_VARARGS, "Encode an integer as varint."},
    {"decode", cvarint_decode, METH_VARARGS,
     "Decode varint bytes to an integer."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef cvarintmodule = {
    PyModuleDef_HEAD_INIT, "cvarint",
    "A C implementation of protobuf varint encoding", -1, CVarintMethods};

PyMODINIT_FUNC PyInit_cvarint(void) { return PyModule_Create(&cvarintmodule); }
