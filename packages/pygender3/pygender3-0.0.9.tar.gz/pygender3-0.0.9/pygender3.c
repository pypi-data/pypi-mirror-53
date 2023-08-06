#include <Python.h>
#include "gender.c"

// Function that does the work.
static PyObject* py_getGender(PyObject* self, PyObject* args)
{
    char *name;
    PyArg_ParseTuple(args, "s", &name);
    return Py_BuildValue("c", get_gender(name,0,0));
}

// Bind python function to c function here
static PyMethodDef pygender3_methods[] = {
    {"get_gender", py_getGender, METH_VARARGS},
    {NULL, NULL}
};


static struct PyModuleDef pygender3 =
{
    PyModuleDef_HEAD_INIT,
    "pygender3", /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    pygender3_methods
};

PyMODINIT_FUNC PyInit_pygender3(void)
{
    return PyModule_Create(&pygender3);
}
