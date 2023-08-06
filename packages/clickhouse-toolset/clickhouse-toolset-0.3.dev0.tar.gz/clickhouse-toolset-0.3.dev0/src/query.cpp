#include <exception>
#include <iostream>
#include <map>
#include <set>

#include <Python.h>

#include "ClickHouseQuery.h"


static std::string PyObject_AsString(PyObject * obj)
{
    PyObject* o = PyObject_Str(obj);
    PyObject * str = PyUnicode_AsEncodedString(o, "utf-8", "~");
    std::string s = PyBytes_AsString(str);
    Py_DECREF(str);
    Py_DECREF(o);
    return s;
}


static PyObject * format(PyObject * self, PyObject * args)
{
    char * query;

    if (!PyArg_ParseTuple(args, "s", &query))
        return NULL;

    try
    {
        auto formattedQuery = ClickHouseQuery::format(query);
        return Py_BuildValue("s", formattedQuery.data());
    }
    catch (std::exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.what());
        return NULL;
    }
}

static PyObject * replaceTables(PyObject * self, PyObject * args)
{
    char * query;
    PyObject * replacementsDict;

    if (!PyArg_ParseTuple(args, "sO!", &query, &PyDict_Type, &replacementsDict))
        return NULL;

    std::map<std::pair<std::string, std::string>, std::string> replacements;
    PyObject * key, * value;
    Py_ssize_t pos = 0;

    while (PyDict_Next(replacementsDict, &pos, &key, &value)) {
        if (PyTuple_Check(key))
        {
            if (PyTuple_Size(key) != 2)
            {
                PyErr_SetString(PyExc_ValueError, "Tuple must contain 2 elements");
                return NULL;
            }
            replacements.emplace(std::make_pair(PyObject_AsString(PyTuple_GetItem(key, 0)), PyObject_AsString(PyTuple_GetItem(key, 1))), PyObject_AsString(value));
        }
        else
        {
            replacements.emplace(std::make_pair("", PyObject_AsString(key)), PyObject_AsString(value));
        }
    }

    try
    {
        auto rewrittenQuery = ClickHouseQuery::replaceTables(query, replacements);
        return Py_BuildValue("s", rewrittenQuery.data());
    }
    catch (std::exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.what());
        return NULL;
    }

}

static PyObject * tables(PyObject * self, PyObject * args)
{
    char * query;
    if (!PyArg_ParseTuple(args, "s", &query))
        return NULL;

    try
    {
        auto tablesInQuery = ClickHouseQuery::tables(query);
        PyObject * l = PyList_New(tablesInQuery.size());
        int i = 0;
        for (const auto table : tablesInQuery)
        {
            PyObject* o = Py_BuildValue("(ss)", table.first.data(), table.second.data());
            PyList_SetItem(l, i++, o);
        }
        return l;
    }
    catch (std::exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.what());
        return NULL;
    }
}

static PyObject * tableIfIsSimpleQuery(PyObject * self, PyObject * args)
{
    char * query;
    if (!PyArg_ParseTuple(args, "s", &query))
        return NULL;

    try
    {
        if (auto table = ClickHouseQuery::tableIfIsSimpleQuery(query))
        {
            return Py_BuildValue("(ss)", table->first.data(), table->second.data());
        }
        return Py_BuildValue("");
    }
    catch (std::exception & e)
    {
        return Py_BuildValue("");
    }
}


static PyMethodDef CHToolsetQueryMethods[] =
{
    {"format", format, METH_VARARGS},
    {"_replace_tables", replaceTables, METH_VARARGS},
    {"tables", tables, METH_VARARGS},
    {"table_if_is_simple_query", tableIfIsSimpleQuery, METH_VARARGS},

    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef chquerymodule = {
    PyModuleDef_HEAD_INIT,
    "chtoolset._query",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    CHToolsetQueryMethods
};

PyMODINIT_FUNC
PyInit__query(void)
{
    return PyModule_Create(&chquerymodule);
}
