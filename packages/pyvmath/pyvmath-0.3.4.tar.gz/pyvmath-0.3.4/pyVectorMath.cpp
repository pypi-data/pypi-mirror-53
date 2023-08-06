#include <Python.h>
#include "vmath_doc_en.h"
#include "pyVectorMath.h"

extern PyTypeObject Vec2Type;
extern PyTypeObject Vec3Type;
extern PyTypeObject Vec4Type;
extern PyTypeObject QuatType;
extern PyTypeObject Mat22Type;
extern PyTypeObject Mat33Type;
extern PyTypeObject Mat44Type;
extern PyTypeObject AABBType;


static float* pyObjToFloat(PyObject* obj, float* f, int& d) {
	if (f) {
		f[0] = f[1] = f[2] = f[3] = 0.0f;
	}
	if (obj->ob_type == &Vec2Type || obj->ob_type == &Vec3Type || obj->ob_type == &Vec4Type || obj->ob_type == &QuatType) {
		d = ((vec_obj*)obj)->d;
		return ((vec_obj*)obj)->v;
	}
	else if (PyFloat_Check(obj) || PyLong_Check(obj)) {
		f[0] = (float)PyFloat_AsDouble(obj);
		d = 1;
	}
	else if (PyTuple_Check(obj)) {
		d = (int)PyTuple_Size(obj);
		if (d > 4) d = 4;
		for (int j = 0; j < d; j++) {
			PyObject* val = PyTuple_GET_ITEM(obj, j);
			f[j] = (float)PyFloat_AsDouble(val);
		}
	}
	else if (PyList_Check(obj)) {
		d = (int)PyList_Size(obj);
		if (d > 4) d = 4;
		for (int j = 0; j < d; j++) {
			PyObject* val = PyList_GET_ITEM(obj, j);
			f[j] = (float)PyFloat_AsDouble(val);
		}
	}
	else {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return  NULL;
	}
	return f;
}

static PyObject* vec_new(PyTypeObject* type, PyObject* args, PyObject* kw) {
	vec_obj* self;
	self = (vec_obj*)type->tp_alloc(type, 0);
	if (!self) return NULL;
	if (type == &QuatType) self->v[3] = 1.0f;

	if (type == &Vec2Type) self->d = 2;
	else if (type == &Vec3Type) self->d = 3;
	else if (type == &Vec4Type || type == &QuatType) self->d = 4;

	int vset = 0;
	Py_ssize_t n = PyTuple_Size(args);
	for (Py_ssize_t i = 0; i < n; i++) {
		PyObject* arg = PyTuple_GET_ITEM(args, i);
		if (PyFloat_Check(arg) || PyLong_Check(arg)) {
			self->v[vset] = (float)PyFloat_AsDouble(arg);
			vset++;
			if (vset >= self->d) return (PyObject*)self;
		}
		else if (PyTuple_Check(arg)) {
			for (Py_ssize_t j = 0; j < PyTuple_Size(arg); j++) {
				PyObject* val = PyTuple_GET_ITEM(arg, j);
				self->v[vset] = (float)PyFloat_AsDouble(val);
				vset++;
				if (vset >= self->d) return (PyObject*)self;
			}
		}
		else if (PyList_Check(arg)) {
			for (Py_ssize_t j = 0; j < PyList_Size(arg); j++) {
				PyObject* val = PyList_GET_ITEM(arg, j);
				self->v[vset] = (float)PyFloat_AsDouble(val);
				vset++;
				if (vset >= self->d) return (PyObject*)self;
			}
		}
		else if (arg->ob_type == &Vec2Type || arg->ob_type == &Vec3Type || arg->ob_type == &Vec4Type || arg->ob_type == &QuatType) {
			vec_obj* varg = (vec_obj*)arg;
			for (int j = 0; j < varg->d; j++) {
				self->v[vset] = varg->v[j];
				vset++;
				if (vset >= self->d) return (PyObject*)self;
			}
		}
		else if (arg->ob_type == &Mat33Type && (type == &QuatType)) {
			mat_obj* varg = (mat_obj*)arg;
			vmath_quat(varg->m, self->v);
			return (PyObject*)self;
		}
	}
	return (PyObject*)self;
}

static PyObject* vec_str(vec_obj * self)
{
	char buf[256];
	static const char* format[] = {
		"none",
		"%f",
		"%f,%f",
		"%f,%f,%f",
		"%f,%f,%f,%f"
	};
	snprintf(buf, 256, format[self->d], self->v[0], self->v[1], self->v[2], self->v[3]);
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* vec_richcompare(PyObject * self, PyObject * other, int op)
{
	if (op == Py_LT || op == Py_LE || op == Py_GT || op == Py_GE) {
		PyErr_Format(PyExc_TypeError, "Only '==' and '!=' are allowed as comparison operators");
		return NULL;
	}

	int d1, d2;
	float buff[4];
	float* v1 = pyObjToFloat((PyObject*)self, nullptr, d1);
	float* v2 = pyObjToFloat((PyObject*)other, buff, d2);
	bool eq = true;
	if (d1 != d2 || (!v2)) eq = false;
	else {
		for (int i = 0; i < d1; i++) {
			if (!vmath_almostEqual(v1[i], v2[i])) {
				eq = false;
				break;
			}
		}
	}
	PyObject* result;
	if (op == Py_NE) eq ^= eq;
	if (op == Py_EQ) result = Py_True;
	else  result = Py_False;
	Py_INCREF(result);
	return result;
}

static PyObject * vec_getX(vec_obj * self)
{
	return PyFloat_FromDouble((double)self->v[0]);
}

static PyObject* vec_getY(vec_obj * self)
{
	return PyFloat_FromDouble((double)self->v[1]);
}

static PyObject* vec_getZ(vec_obj * self)
{
	return PyFloat_FromDouble((double)self->v[2]);
}

static PyObject* vec_getW(vec_obj * self)
{
	return PyFloat_FromDouble((double)self->v[3]);
}

static int vec_setX(vec_obj * self, PyObject * value)
{
	self->v[0] = (float)PyFloat_AsDouble(value);
	return 0;
}

static int vec_setY(vec_obj * self, PyObject * value)
{
	self->v[1] = (float)PyFloat_AsDouble(value);
	return 0;
}

static int vec_setZ(vec_obj * self, PyObject * value)
{
	self->v[2] = (float)PyFloat_AsDouble(value);
	return 0;
}

static int vec_setW(vec_obj * self, PyObject * value)
{
	self->v[3] = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* vec_setElem(vec_obj * self, PyObject * args)
{
	int i = 0;
	float val = 0.0f;
	if (!PyArg_ParseTuple(args, "if", &i, &val))
		return NULL;
	if (i < 0 || i >= self->d) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	self->v[i] = val;
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* vec_getElem(vec_obj * self, PyObject * args)
{
	int i = 0;
	if (!PyArg_ParseTuple(args, "i", &i))
		return NULL;
	if (i < 0 || i >= self->d) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	return PyFloat_FromDouble((double)self->v[i]);
}

static PyObject* vec_add(vec_obj * a, PyObject * b)
{
	vec_obj* obj = PyObject_New(vec_obj, a->ob_base.ob_type);
	if (!obj) return NULL;
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
	int d1, d2;
	float buff[4];
	float* v1 = pyObjToFloat((PyObject*)a, nullptr, d1);
	float* v2 = pyObjToFloat((PyObject*)b, buff, d2);
	if (!v2) {
		Py_DECREF(obj);
		return NULL;
	}
	int l = d1 < d2 ? d1 : d2;
	vmath_add(v1, v2, l, obj->v);
	for (int i = d2; i < d1; i++) obj->v[i] = v1[i];
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_sub(vec_obj * a, PyObject * b)
{
	vec_obj* obj = PyObject_New(vec_obj, a->ob_base.ob_type);
	if (!obj) return NULL;
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
	int d1, d2;
	float buff[4];
	float* v1 = pyObjToFloat((PyObject*)a, nullptr, d1);
	float* v2 = pyObjToFloat((PyObject*)b, buff, d2);
	if (!v2) {
		Py_DECREF(obj);
		return NULL;
	}
	int l = d1 < d2 ? d1 : d2;
	vmath_sub(v1, v2, l, obj->v);
	for (int i = d2; i < d1; i++) obj->v[i] = v1[i];
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_mul(vec_obj * a, PyObject * b)
{
	vec_obj* obj = PyObject_New(vec_obj, a->ob_base.ob_type);
	if (!obj) return NULL;
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
	int d1, d2;
	float buff[4];
	float* v1 = pyObjToFloat((PyObject*)a, nullptr, d1);
	float* v2 = pyObjToFloat((PyObject*)b, buff, d2);
	if (!v2) {
		Py_DECREF(obj);
		return NULL;
	}
	if (d2 == 1)
		vmath_mul(v1, v2[0], d1, obj->v);
	else {
		if (b->ob_type == &QuatType) {
			if (d2 != 4) {
				PyErr_SetString(PyExc_ValueError, "invalid arguments");
				Py_DECREF(obj);
				return NULL;
			}
			vmath_quat_mul(v1, v2, obj->v);
		}
		else {
			int l = d1 < d2 ? d1 : d2;
			vmath_mulPerElem(v1, v2, l, obj->v);
			for (int i = d2; i < d1; i++) obj->v[i] = v1[i];
		}
	}
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_div(vec_obj * a, PyObject * b)
{
	vec_obj* obj = PyObject_New(vec_obj, a->ob_base.ob_type);
	if (!obj) return NULL;
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
	int d1, d2;
	float buff[4];
	float* v1 = pyObjToFloat((PyObject*)a, nullptr, d1);
	float* v2 = pyObjToFloat((PyObject*)b, buff, d2);
	if (!v2) {
		Py_DECREF(obj);
		return NULL;
	}
	if (d2 == 1)
		vmath_div(v1, v2[0], d1, obj->v);
	else {
		if (a->ob_base.ob_type == &QuatType) {
			PyErr_SetString(PyExc_ValueError, "invalid arguments");
			Py_DECREF(obj);
			return NULL;
		}
		else {
			int l = d1 < d2 ? d1 : d2;
			vmath_divPerElem(v1, v2, l, obj->v);
			for (int i = d2; i < d1; i++) obj->v[i] = v1[i];
		}
	}
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_neg(vec_obj * a)
{
	vec_obj* obj = PyObject_New(vec_obj, a->ob_base.ob_type);
	if (!obj) return NULL;
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
	int d1;
	float* v1 = pyObjToFloat((PyObject*)a, nullptr, d1);
	vmath_neg(v1, d1, obj->v);
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_mat_add(PyObject * self, PyObject * args)
{
	PyObject* a;
	PyObject* b;
	if (!PyArg_ParseTuple(args, "OO", &a, &b)) return NULL;

	if (a->ob_type == &Mat22Type || a->ob_type == &Mat33Type || a->ob_type == &Mat44Type) {
		if (a->ob_type != b->ob_type) {
			PyErr_SetString(PyExc_ValueError, "invalid arguments");
			return NULL;
		}
		mat_obj* obj = PyObject_New(mat_obj, a->ob_type);
		if (!obj) return NULL;

		vmath_mat_add(((mat_obj*)a)->m, ((mat_obj*)b)->m, ((mat_obj*)a)->d, ((mat_obj*)b)->d,  obj->m);
		obj->d = ((mat_obj*)a)->d;
		return (PyObject*)obj;
	}

	int d1, d2;
	float buff1[4];
	float buff2[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	float* v2 = pyObjToFloat((PyObject*)b, buff2, d2);
	if (!v2) return NULL;

	vec_obj* obj = NULL;
	switch (d1) {
	case 1: return PyFloat_FromDouble((double)(v1[0] + v2[0]));
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;

	if (a->ob_type == &QuatType) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		Py_DECREF(obj);
		return NULL;
	}
	else {
		int l = d1 < d2 ? d1 : d2;
		vmath_add(v1, v2, l, obj->v);
		for (int i = d2; i < d1; i++) obj->v[i] = v1[i];
	}
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_mat_sub(PyObject * self, PyObject * args)
{
	PyObject* a;
	PyObject* b;
	if (!PyArg_ParseTuple(args, "OO", &a, &b)) return NULL;

	if (a->ob_type == &Mat22Type || a->ob_type == &Mat33Type || a->ob_type == &Mat44Type) {
		if (a->ob_type != b->ob_type) {
			PyErr_SetString(PyExc_ValueError, "invalid arguments");
			return NULL;
		}
		mat_obj* obj = PyObject_New(mat_obj, a->ob_type);
		if (!obj) return NULL;

		vmath_mat_sub(((mat_obj*)a)->m, ((mat_obj*)b)->m, ((mat_obj*)a)->d, ((mat_obj*)b)->d, obj->m);
		obj->d = ((mat_obj*)a)->d;
		return (PyObject*)obj;
	}

	int d1, d2;
	float buff1[4];
	float buff2[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	float* v2 = pyObjToFloat((PyObject*)b, buff2, d2);
	if (!v2) return NULL;

	vec_obj* obj = NULL;
	switch (d1) {
	case 1: return PyFloat_FromDouble((double)(v1[0] - v2[0]));
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;

	int l = d1 < d2 ? d1 : d2;
	vmath_sub(v1, v2, l, obj->v);
	for (int i = d2; i < d1; i++) obj->v[i] = v1[i];

	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_mat_mul(PyObject * self, PyObject * args)
{
	PyObject* a;
	PyObject* b;
	if (!PyArg_ParseTuple(args, "OO", &a, &b)) return NULL;

	if (a->ob_type == &Mat22Type || a->ob_type == &Mat33Type || a->ob_type == &Mat44Type) {

		PyObject* obj = NULL;
		if (b->ob_type == a->ob_type) {
			obj = (PyObject*)PyObject_New(mat_obj, a->ob_type);
			if (!obj) return NULL;
			vmath_mul_matrix_matrix(((mat_obj*)a)->m, ((mat_obj*)b)->m, ((mat_obj*)a)->d, ((mat_obj*)b)->d, ((mat_obj*)obj)->m);
			((mat_obj*)obj)->d = ((mat_obj*)a)->d;
		}
		else {
			if (b->ob_type == &QuatType) {
				PyErr_SetString(PyExc_ValueError, "invalid arguments");
				return NULL;
			}
			int d;
			float buf[4];
			float* v = pyObjToFloat(b, buf, d);

			//scalar
			if (d == 1) {
				obj = (PyObject*)PyObject_New(mat_obj, a->ob_type);
				if (!obj) return NULL;
				vmath_mat_mul(((mat_obj*)a)->m, v[0], ((mat_obj*)a)->d, ((mat_obj*)obj)->m);
				((mat_obj*)obj)->d = ((mat_obj*)a)->d;
			}
			//vector
			else if (d) {
				if (((mat_obj*)a)->d == 2)
					obj = (PyObject*)PyObject_New(vec_obj, &Vec2Type);
				else if (((mat_obj*)a)->d == 3)
					obj = (PyObject*)PyObject_New(vec_obj, &Vec3Type);
				else if (((mat_obj*)a)->d == 4)
					obj = (PyObject*)PyObject_New(vec_obj, &Vec4Type);
				if (!obj) return NULL;
				((vec_obj*)obj)->v[0] = ((vec_obj*)obj)->v[1] = ((vec_obj*)obj)->v[2] = ((vec_obj*)obj)->v[3] = 0.0f;
				vmath_mul_matrix_vector(v, ((mat_obj*)a)->m, ((mat_obj*)a)->d, d, ((vec_obj*)obj)->v);
				((vec_obj*)obj)->d = ((mat_obj*)a)->d;
			}
		}
		return (PyObject*)obj;
	}

	int d1, d2;
	float buff1[4];
	float buff2[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	float* v2 = pyObjToFloat((PyObject*)b, buff2, d2);
	if (!v2) return NULL;

	vec_obj* obj = NULL;
	switch (d1) {
	case 1: return PyFloat_FromDouble((double)(v1[0] * v2[0]));
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;

	if (d2 == 1)
		vmath_mul(v1, v2[0], d1, obj->v);
	else {
		if (a->ob_type == &QuatType) {
			if (d2 != 4) {
				PyErr_SetString(PyExc_ValueError, "invalid arguments");
				Py_DECREF(obj);
				return NULL;
			}
			vmath_quat_mul(v1, v2, obj->v);
		}
		else {
			int l = d1 < d2 ? d1 : d2;
			vmath_mulPerElem(v1, v2, l, obj->v);
			for (int i = d2; i < d1; i++) obj->v[i] = v1[i];
		}
	}
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_div2(PyObject * self, PyObject * args)
{
	PyObject* a;
	PyObject* b;
	if (!PyArg_ParseTuple(args, "OO", &a, &b)) return NULL;

	int d1, d2;
	float buff1[4];
	float buff2[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	float* v2 = pyObjToFloat((PyObject*)b, buff2, d2);
	if (!v2) return NULL;

	vec_obj* obj = NULL;
	switch (d1) {
	case 1: return PyFloat_FromDouble((double)(v1[0] / v2[0]));
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;

	if (d2 == 1)
		vmath_div(v1, v2[0], d1, obj->v);
	else {
		int l = d1 < d2 ? d1 : d2;
		vmath_divPerElem(v1, v2, l, obj->v);
		for (int i = d2; i < d1; i++) obj->v[i] = v1[i];
	}
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_recipPerElem(PyObject * self, PyObject * args)
{
	PyObject* a;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;

	int d1;
	float buff1[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1) return  NULL;

	vec_obj* obj = NULL;
	switch (d1) {
	case 1: return PyFloat_FromDouble((double)(1.0f / v1[0]));
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
	vmath_recipPerElem(v1, d1, obj->v);
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_sqrtPerElem(PyObject * self, PyObject * args)
{
	PyObject* a;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;

	int d1;
	float buff1[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;

	vec_obj* obj = NULL;
	switch (d1) {
	case 1: return PyFloat_FromDouble((double)sqrtf(v1[0]));
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
	vmath_sqrtPerElem(v1, d1, obj->v);
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_rsqrtPerElem(PyObject * self, PyObject * args)
{
	PyObject* a;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;

	int d1;
	float buff1[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;

	vec_obj* obj = NULL;
	switch (d1) {
	case 1: return PyFloat_FromDouble((double)(1.0f / sqrtf(v1[0])));
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
	vmath_rsqrtPerElem(v1, d1, obj->v);
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_absPerElem(PyObject * self, PyObject * args)
{
	PyObject* a;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;

	if (a->ob_type == &Mat22Type || a->ob_type == &Mat33Type || a->ob_type == &Mat44Type) {
		mat_obj* obj = PyObject_New(mat_obj, a->ob_type);
		if (!obj) return NULL;
		vmath_mat_abs(((mat_obj*)a)->m, ((mat_obj*)a)->d, obj->m);
		obj->d = ((mat_obj*)a)->d;
		return (PyObject*)obj;
	}

	int d1;
	float buff1[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;

	vec_obj* obj = NULL;
	switch (d1) {
	case 1: return PyFloat_FromDouble((double)fabsf(v1[0]));
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
	vmath_absPerElem(v1, d1, obj->v);
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_maxPerElem(PyObject * self, PyObject * args)
{
	PyObject* a;
	PyObject* b;
	if (!PyArg_ParseTuple(args, "OO", &a, &b)) return NULL;

	int d1, d2;
	float buff1[4];
	float buff2[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	float* v2 = pyObjToFloat((PyObject*)b, buff2, d2);
	if (!v2) return NULL;

	vec_obj* obj = NULL;
	switch (d1) {
	case 1: return PyFloat_FromDouble((double)(v1[0] > v2[0] ? v1[0] : v2[0]));
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;

	if (d2 == 1)
		vmath_maxPerElem(v1, v2[0], d1, obj->v);
	else {
		int l = d1 < d2 ? d1 : d2;
		vmath_maxPerElem(v1, v2, l, obj->v);
		for (int i = d2; i < d1; i++) obj->v[i] = v1[i];
	}
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_maxElem(PyObject * self, PyObject * args)
{
	PyObject* a;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;

	int d1;
	float buff1[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	return PyFloat_FromDouble((double)vmath_maxElem(v1, d1));
}

static PyObject* vec_minPerElem(PyObject * self, PyObject * args)
{
	PyObject* a;
	PyObject* b;
	if (!PyArg_ParseTuple(args, "OO", &a, &b)) return NULL;

	int d1, d2;
	float buff1[4];
	float buff2[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	float* v2 = pyObjToFloat((PyObject*)b, buff2, d2);
	if (!v2) return NULL;

	vec_obj* obj = NULL;
	switch (d1) {
	case 1: return PyFloat_FromDouble((double)(v1[0] < v2[0] ? v1[0] : v2[0]));
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;

	if (d2 == 1)
		vmath_minPerElem(v1, v2[0], d1, obj->v);
	else {
		int l = d1 < d2 ? d1 : d2;
		vmath_minPerElem(v1, v2, l, obj->v);
		for (int i = d2; i < d1; i++) obj->v[i] = v1[i];
	}
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_minElem(PyObject * self, PyObject * args)
{
	PyObject* a;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;

	int d1;
	float buff1[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	return PyFloat_FromDouble((double)vmath_minElem(v1, d1));
}

static PyObject* vec_sum(PyObject * self, PyObject * args)
{
	PyObject* a;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;

	int d1;
	float buff1[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	return PyFloat_FromDouble((double)vmath_sum(v1, d1));
}

static PyObject* vec_dot(PyObject * self, PyObject * args)
{
	PyObject* a;
	PyObject* b;
	if (!PyArg_ParseTuple(args, "OO", &a, &b)) return NULL;

	int d1, d2;
	float buff1[4];
	float buff2[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	float* v2 = pyObjToFloat((PyObject*)b, buff2, d2);
	if (!v2)return NULL;
	if (d1 != d2) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	return PyFloat_FromDouble((double)vmath_dot(v1, v2, d1));
}

static PyObject* vec_lengthSqr(PyObject * self, PyObject * args)
{
	PyObject* a;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;
	int d1;
	float buff1[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	return PyFloat_FromDouble((double)vmath_lengthSqr(v1, d1));
}

static PyObject* vec_length(PyObject * self, PyObject * args)
{
	PyObject* a;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;
	int d1;
	float buff1[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	return PyFloat_FromDouble((double)sqrtf(vmath_lengthSqr(v1, d1)));
}

static PyObject* vec_normalize(PyObject * self, PyObject * args)
{
	PyObject* a;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;

	int d1;
	float buff1[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;

	vec_obj* obj = NULL;
	switch (d1) {
	case 1: return PyFloat_FromDouble((double)(v1[0]));
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
	vmath_normalize(v1, d1, obj->v);
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_cross(PyObject * self, PyObject * args) {
	PyObject* a;
	PyObject* b;
	if (!PyArg_ParseTuple(args, "OO", &a, &b)) return NULL;

	int d1, d2;
	float buff1[4];
	float buff2[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	float* v2 = pyObjToFloat((PyObject*)b, buff2, d2);
	if (!v2)return NULL;

	if (d1 != d2) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	if (d1 == 2)
		return PyFloat_FromDouble((double)sqrtf(vmath_cross2D(v1, v2)));
	else if (d1 >= 3) {
		vec_obj* obj = PyObject_New(vec_obj, a->ob_type);
		if (!obj) return NULL;
		obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
		vmath_cross3D(v1, v2, obj->v);
		obj->d = d1;
		return (PyObject*)obj;
	}
	PyErr_SetString(PyExc_ValueError, "invalid arguments");
	return NULL;
}

static PyObject* vec_lerp(PyObject * self, PyObject * args)
{
	float t;
	PyObject* a;
	PyObject* b;
	if (!PyArg_ParseTuple(args, "fOO", &t, &a, &b)) return NULL;

	int d1, d2;
	float buff1[4];
	float buff2[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	float* v2 = pyObjToFloat((PyObject*)b, buff2, d2);
	if (!v2) return NULL;

	vec_obj* obj = NULL;
	switch (d1) {
	case 1: return PyFloat_FromDouble((double)(v1[0] + ((v2[0] - v1[0]) * t)));
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
	int l = d1 < d2 ? d1 : d2;
	vmath_lerp(t, v1, v2, l, obj->v);
	for (int i = d2; i < d1; i++) obj->v[i] = v1[i];
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_slerp(PyObject * self, PyObject * args)
{
	float t;
	PyObject* a;
	PyObject* b;
	if (!PyArg_ParseTuple(args, "fOO", &t, &a, &b)) return NULL;

	int d1, d2;
	float buff1[4];
	float buff2[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	float* v2 = pyObjToFloat((PyObject*)b, buff2, d2);
	if (!v2) return NULL;

	vec_obj* obj = NULL;
	switch (d1) {
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
	if (a->ob_type == &QuatType) {
		if (d1 != d2) {
			PyErr_SetString(PyExc_ValueError, "invalid arguments");
			Py_DECREF(obj);
			return NULL;
		}
		vmath_quat_slerp(t, v1, v2, obj->v);
	}
	else {
		int l = d1 < d2 ? d1 : d2;
		vmath_slerp(t, v1, v2, l, obj->v);
		for (int i = d2; i < d1; i++) obj->v[i] = v1[i];
	}
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* vec_almostEqual(PyObject* self, PyObject* args)
{
	PyObject* a;
	PyObject* b;
	if (!PyArg_ParseTuple(args, "OO", &a, &b)) return NULL;

	int d1, d2;
	float buffa[4];
	float buffb[4];
	float* v1 = pyObjToFloat((PyObject*)a, buffa, d1);
	float* v2 = pyObjToFloat((PyObject*)b, buffb, d2);
	bool eq = true;
	if (d1 != d2 || (!v2)) eq = false;
	else {
		for (int i = 0; i < d1; i++) {
			if (!vmath_almostEqual(v1[i], v2[i])) {
				eq = false;
				break;
			}
		}
	}
	PyObject* result = eq ? Py_True : Py_False;
	Py_INCREF(result);
	return result;
}

static PyObject* quat_rotation(PyObject * self, PyObject * args)
{
	PyObject* a;
	PyObject* b = nullptr;
	if (!PyArg_ParseTuple(args, "O|O", &a, &b)) return NULL;

	int d1;
	int	d2=3;
	float buff1[4];
	float buff2[4] = {0,0,1,0};
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	float* v2 = buff2;
	if(b) v2 = pyObjToFloat((PyObject*)b, buff2, d2);

	vec_obj* obj = PyObject_New(vec_obj, &QuatType);
	if (!obj) return NULL;

	if (d1 == 1)
		vmath_quat_rotation(v1[0], v2, obj->v);
	else
		vmath_quat_rotation(v1, v2, obj->v);

	obj->d = 4;
	return (PyObject*)obj;
}

static PyObject* quat_rotationX(PyObject * self, PyObject * args)
{
	float r;
	if (!PyArg_ParseTuple(args, "f", &r)) return NULL;
	vec_obj* obj = PyObject_New(vec_obj, &QuatType);
	if (!obj) return NULL;
	vmath_quat_rotationX(r, obj->v);
	obj->d = 4;
	return (PyObject*)obj;
}

static PyObject* quat_rotationY(PyObject * self, PyObject * args)
{
	float r;
	if (!PyArg_ParseTuple(args, "f", &r)) return NULL;
	vec_obj* obj = PyObject_New(vec_obj, &QuatType);
	if (!obj) return NULL;
	vmath_quat_rotationY(r, obj->v);
	obj->d = 4;
	return (PyObject*)obj;
}

static PyObject* quat_rotationZ(PyObject * self, PyObject * args)
{
	float r;
	if (!PyArg_ParseTuple(args, "f", &r)) return NULL;
	vec_obj* obj = PyObject_New(vec_obj, &QuatType);
	if (!obj) return NULL;
	vmath_quat_rotationZ(r, obj->v);
	obj->d = 4;
	return (PyObject*)obj;
}

static PyObject* quat_conj(PyObject * self, PyObject * args) {

	vec_obj* a;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;
	if (a->ob_base.ob_type != &QuatType) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	vec_obj* obj = PyObject_New(vec_obj, &QuatType);
	if (!obj) return NULL;

	vmath_quat_conj(a->v, obj->v);
	obj->d = 4;
	return (PyObject*)obj;
}

static PyObject* quat_squad(PyObject * self, PyObject * args) {

	float t = 0.0f;
	vec_obj* a = NULL;
	vec_obj* b = NULL;
	vec_obj* c = NULL;
	vec_obj* d = NULL;

	if (!PyArg_ParseTuple(args, "fOOOO", &a)) return NULL;
	if (a->ob_base.ob_type != &QuatType || b->ob_base.ob_type != &QuatType || c->ob_base.ob_type != &QuatType || d->ob_base.ob_type != &QuatType) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	vec_obj* obj = PyObject_New(vec_obj, &QuatType);
	if (!obj) return NULL;
	vmath_quat_squad(t, a->v, b->v, c->v, d->v, obj->v);
	obj->d = 4;
	return (PyObject*)obj;
}

static PyObject* quat_rotate(PyObject * self, PyObject * args) {

	PyObject* a;
	PyObject* b;
	if (!PyArg_ParseTuple(args, "OO", &a, &b)) return NULL;
	int d1, d2;
	float buff1[4];
	float buff2[4];
	float* v1 = pyObjToFloat((PyObject*)a, buff1, d1);
	if (!v1)return NULL;
	float* v2 = pyObjToFloat((PyObject*)b, buff2, d2);
	if (!v2) return NULL;
	if (b->ob_type != &QuatType) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}

	vec_obj* obj = NULL;
	switch (d1) {
	case 2: obj = PyObject_New(vec_obj, &Vec2Type); break;
	case 3: obj = PyObject_New(vec_obj, &Vec3Type); break;
	case 4: {
		if (a->ob_type == &QuatType)
			obj = PyObject_New(vec_obj, &QuatType);
		else
			obj = PyObject_New(vec_obj, &Vec4Type);
		break;
	}
	}
	if (!obj) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;
	vmath_quat_rotate(v2, v1, obj->v);
	obj->d = d1;
	return (PyObject*)obj;
}

static PyObject* mat_new(PyTypeObject * type, PyObject * args, PyObject * kw) {

	mat_obj* self;
	self = (mat_obj*)type->tp_alloc(type, 0);
	if (!self) return NULL;

	if (type == &Mat22Type) self->d = 2;
	else if (type == &Mat33Type) self->d = 3;
	else if (type == &Mat44Type) self->d = 4;

	int row = 0;
	int col = 0;
	Py_ssize_t n = PyTuple_Size(args);
	for (Py_ssize_t i = 0; i < n; i++) {
		PyObject* arg = PyTuple_GET_ITEM(args, i);
		if (arg->ob_type == &Mat22Type || arg->ob_type == &Mat33Type || arg->ob_type == &Mat44Type || arg->ob_type == &QuatType) {
			if (col != 0 || row != 0) {
				Py_DECREF(self);
				PyErr_SetString(PyExc_ValueError, "invalid arguments");
				return  NULL;
			}
			if (arg->ob_type == &QuatType)
				vmath_mat_from_quat(((vec_obj*)arg)->v, self->d, self->m);
			else
				vmath_mat_cpy(((mat_obj*)arg)->m, ((mat_obj*)arg)->d,self->d, self->m);
			row += ((mat_obj*)arg)->d > 3 ? ((mat_obj*)arg)->d : 3;
			if (row >= self->d) return (PyObject*)self;
		}
		else if (PyFloat_Check(arg) || PyLong_Check(arg)) {
			self->m[row * self->d + col] = (float)PyFloat_AsDouble(arg);
			if (++col >= self->d) { if (++row >= self->d) { return (PyObject*)self; } col = 0; }
		}
		else if (PyTuple_Check(arg)) {
			for (Py_ssize_t j = 0; j < PyTuple_Size(arg); j++) {
				PyObject* val = PyTuple_GET_ITEM(arg, j);
				self->m[row * self->d + col] = (float)PyFloat_AsDouble(val);
				if (++col >= self->d) { if (++row >= self->d) { return (PyObject*)self; } col = 0; }
			}
		}
		else if (PyList_Check(arg)) {
			for (Py_ssize_t j = 0; j < PyList_Size(arg); j++) {
				PyObject* val = PyList_GET_ITEM(arg, j);
				self->m[row * self->d + col] = (float)PyFloat_AsDouble(val);
				if (++col >= self->d) { if (++row >= self->d) { return (PyObject*)self; } col = 0; }
			}
		}
		else if (arg->ob_type == &Vec2Type || arg->ob_type == &Vec3Type || arg->ob_type == &Vec4Type) {
			if (col != 0) {
				Py_DECREF(self);
				PyErr_SetString(PyExc_ValueError, "invalid arguments");
				return  NULL;
			}
			vec_obj* varg = (vec_obj*)arg;
			for (int j = 0; j < varg->d; j++) {
				self->m[row * self->d + col] = varg->v[col];
				if (++col >= self->d) break;
			}
			if (++row >= self->d) { return (PyObject*)self; } col = 0;
		}
	}
	if (type == &Mat44Type && row != 0) {
		self->m[15] = 1.0f;
	}
	return (PyObject*)self;
}

static PyObject* mat_str(mat_obj * self)
{
	char buf[512];
	char* ptr = buf;
	char tmp[16];

	for (int i = 0; i < self->d; i++) {
		for (int j = 0; j < self->d; j++) {
			snprintf(tmp, 16, "%f", self->m[i * self->d + j]);
			char* ptmp = tmp;
			while (*ptmp) { *ptr = *ptmp; ptr++; ptmp++; }
			if (j == self->d - 1) * ptr = '\n';
			else *ptr = ',';
			ptr++;
		}
	}
	*ptr = 0;
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* mat_setElem(mat_obj * self, PyObject * args)
{
	uint32_t col, row;
	float val;
	if (!PyArg_ParseTuple(args, "iif", &col, &row, &val))
		return NULL;
	if (col >= (uint32_t)self->d || row >= (uint32_t)self->d) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	self->m[row * self->d + col] = val;
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* mat_getElem(mat_obj * self, PyObject * args)
{
	uint32_t col, row;
	float val;
	if (!PyArg_ParseTuple(args, "iif", &col, &row, &val))
		return NULL;
	if (col >= (uint32_t)self->d || row >= (uint32_t)self->d) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	return PyFloat_FromDouble((double)self->m[row * 4 + col]);
}

static PyObject* mat_add(mat_obj * a, PyObject * b)
{
	if (b->ob_type != a->ob_base.ob_type) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	mat_obj* obj = PyObject_New(mat_obj, a->ob_base.ob_type);
	if (!obj) return NULL;

	vmath_mat_add(a->m, ((mat_obj*)b)->m, a->d, ((mat_obj*)b)->d, obj->m);
	obj->d = a->d;
	return (PyObject*)obj;
}

static PyObject* mat_sub(mat_obj * a, PyObject * b)
{
	if (b->ob_type != a->ob_base.ob_type) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	mat_obj* obj = PyObject_New(mat_obj, a->ob_base.ob_type);
	if (!obj) return NULL;

	vmath_mat_sub(a->m, ((mat_obj*)b)->m, a->d, ((mat_obj*)b)->d, obj->m);
	obj->d = a->d;
	return (PyObject*)obj;
}

static PyObject* mat_mul(mat_obj * a, PyObject * b)
{
	PyObject* obj = NULL;
	if (b->ob_type == a->ob_base.ob_type) {
		obj = (PyObject*)PyObject_New(mat_obj, a->ob_base.ob_type);
		if (!obj) return NULL;
		vmath_mul_matrix_matrix(a->m, ((mat_obj*)b)->m, a->d, ((mat_obj*)b)->d, ((mat_obj*)obj)->m);
		((mat_obj*)obj)->d = a->d;
	}
	else {
		if (b->ob_type == &QuatType) {
			PyErr_SetString(PyExc_ValueError, "invalid arguments");
			return NULL;
		}
		int d;
		float buf[4];
		float* v = pyObjToFloat(b, buf, d);

		//scalar
		if (d == 1) {
			obj = (PyObject*)PyObject_New(mat_obj, a->ob_base.ob_type);
			if (!obj) return NULL;
			vmath_mat_mul(a->m, v[0], a->d, ((mat_obj*)obj)->m);
			((mat_obj*)obj)->d = a->d;
		}
		//vector
		else if (d) {
			if (a->d == 2)
				obj = (PyObject*)PyObject_New(vec_obj, &Vec2Type);
			else if (a->d == 3)
				obj = (PyObject*)PyObject_New(vec_obj, &Vec3Type);
			else if (a->d == 4)
				obj = (PyObject*)PyObject_New(vec_obj, &Vec4Type);
			if (!obj) return NULL;
			((vec_obj*)obj)->v[0] = ((vec_obj*)obj)->v[1] = ((vec_obj*)obj)->v[2] = ((vec_obj*)obj)->v[3] = 0.0f;
			vmath_mul_matrix_vector(v, a->m, a->d, d, ((vec_obj*)obj)->v);
			((vec_obj*)obj)->d = a->d;
		}
	}
	return (PyObject*)obj;
}

static PyObject* mat_neg(mat_obj * a)
{
	mat_obj* obj = PyObject_New(mat_obj, a->ob_base.ob_type);
	if (!obj) return NULL;

	vmath_mat_neg(a->m, a->d, obj->m);
	obj->d = a->d;
	return (PyObject*)obj;
}

static PyObject* mat_rotation(PyObject * self, PyObject * args) {

	PyObject* a = NULL;
	float r;
	int d;
	if (!PyArg_ParseTuple(args, "fi|O", &r,&d, &a)) return NULL;

	int d1 = 0;
	float buff1[4] = { 0.0f, 0.0f, 1.0f, 0.0f };
	float* v1 = buff1;
	if (a) {
		v1 = pyObjToFloat((PyObject*)a, buff1, d1);
		if (!v1)return NULL;
	}

	mat_obj* obj;
	if (d == 2)
		obj = PyObject_New(mat_obj, &Mat22Type);
	else if (d == 3)
		obj = PyObject_New(mat_obj, &Mat33Type);
	else if (d == 4)
		obj = PyObject_New(mat_obj, &Mat44Type);
	else {
		PyErr_SetString(PyExc_ValueError, "dimension can only be 2,3or4");
		return  NULL;
	}

	vmath_mat_rotation(r, v1, d, obj->m);

	obj->d = d;
	return (PyObject*)obj;

}

static PyObject* mat_rotationX(PyObject * self, PyObject * args) {
	float r;
	int d;
	if (!PyArg_ParseTuple(args, "fi", &r, &d)) return NULL;

	mat_obj* obj;
	if (d == 2)
		obj = PyObject_New(mat_obj, &Mat22Type);
	else if (d == 3)
		obj = PyObject_New(mat_obj, &Mat33Type);
	else if (d == 4)
		obj = PyObject_New(mat_obj, &Mat44Type);
	else {
		PyErr_SetString(PyExc_ValueError, "dimension can only be 2,3or4");
		return  NULL;
	}
	vmath_mat_rotationX(r, d, obj->m);
	obj->d = d;
	return (PyObject*)obj;

}

static PyObject* mat_rotationY(PyObject * self, PyObject * args) {
	float r;
	int d;
	if (!PyArg_ParseTuple(args, "fi", &r, &d)) return NULL;

	mat_obj* obj;
	if (d == 2)
		obj = PyObject_New(mat_obj, &Mat22Type);
	else if (d == 3)
		obj = PyObject_New(mat_obj, &Mat33Type);
	else if (d == 4)
		obj = PyObject_New(mat_obj, &Mat44Type);
	else {
		PyErr_SetString(PyExc_ValueError, "dimension can only be 2,3or4");
		return  NULL;
	}
	vmath_mat_rotationY(r, d, obj->m);
	obj->d = d;
	return (PyObject*)obj;
}

static PyObject* mat_rotationZ(PyObject * self, PyObject * args) {
	float r;
	int d;
	if (!PyArg_ParseTuple(args, "fi", &r, &d)) return NULL;

	mat_obj* obj;
	if (d == 2)
		obj = PyObject_New(mat_obj, &Mat22Type);
	else if (d == 3)
		obj = PyObject_New(mat_obj, &Mat33Type);
	else if (d == 4)
		obj = PyObject_New(mat_obj, &Mat44Type);
	else {
		PyErr_SetString(PyExc_ValueError, "dimension can only be 2,3or4");
		return  NULL;
	}
	vmath_mat_rotationZ(r, d, obj->m);
	obj->d = d;
	return (PyObject*)obj;
}

static PyObject* mat_identity(PyObject* self, PyObject* args) {
	int d;
	if (!PyArg_ParseTuple(args, "i", &d)) return NULL;

	mat_obj* obj;
	if (d == 2)
		obj = PyObject_New(mat_obj, &Mat22Type);
	else if (d == 3)
		obj = PyObject_New(mat_obj, &Mat33Type);
	else if (d == 4)
		obj = PyObject_New(mat_obj, &Mat44Type);
	else {
		PyErr_SetString(PyExc_ValueError, "dimension can only be 2,3or4");
		return  NULL;
	}
	vmath_identity(obj->m, d);
	obj->d = d;
	return (PyObject*)obj;
}

static void getVectorFromArg(PyObject * args, int d, float* v, int offs = 1) {
	v[0] = v[1] = v[2] = v[3] = 0.0f;
	int vset = 0;
	Py_ssize_t n = PyTuple_Size(args);
	for (Py_ssize_t i = offs; i < n; i++) {
		PyObject* arg = PyTuple_GET_ITEM(args, i);
		if (PyFloat_Check(arg) || PyLong_Check(arg)) {
			v[vset] = (float)PyFloat_AsDouble(arg);
			if (++vset >= d) return;
		}
		else if (PyTuple_Check(arg)) {
			for (Py_ssize_t j = 0; j < PyTuple_Size(arg); j++) {
				PyObject* val = PyTuple_GET_ITEM(arg, j);
				v[vset] = (float)PyFloat_AsDouble(val);
				if (++vset >= d) return;
			}
		}
		else if (PyList_Check(arg)) {
			for (Py_ssize_t j = 0; j < PyList_Size(arg); j++) {
				PyObject* val = PyList_GET_ITEM(arg, j);
				v[vset] = (float)PyFloat_AsDouble(val);
				if (++vset >= d) return;
			}
		}
		else if (arg->ob_type == &Vec2Type || arg->ob_type == &Vec3Type || arg->ob_type == &Vec4Type) {
			vec_obj* varg = (vec_obj*)arg;
			for (int j = 0; j < varg->d; j++) {
				v[vset] = varg->v[j];
				vset++;
				if (vset >= d) return;
			}
		}
	}
}

static PyObject* mat_rotationZYX(PyObject * self, PyObject * args) {

	uint32_t d;
	PyObject* arg = PyTuple_GET_ITEM(args, 0);
	if (!PyLong_Check(arg)) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	d = (uint32_t)PyLong_AsLong(arg);
	if (d > 4) d = 4;
	float v[4];
	getVectorFromArg(args, d, v);

	mat_obj* obj;
	if (d == 2)
		obj = PyObject_New(mat_obj, &Mat22Type);
	else if (d == 3)
		obj = PyObject_New(mat_obj, &Mat33Type);
	else if (d == 4)
		obj = PyObject_New(mat_obj, &Mat44Type);
	else {
		PyErr_SetString(PyExc_ValueError, "dimension can only be 2,3or4");
		return  NULL;
	}
	vmath_mat_rotationZYX(v, d, obj->m);
	obj->d = d;
	return (PyObject*)obj;

}

static PyObject* mat_transpose(PyObject * self, PyObject * args) {

	PyObject* a = NULL;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;
	if (a->ob_type != &Mat22Type && a->ob_type != &Mat33Type && a->ob_type != &Mat44Type) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return  NULL;
	}
	mat_obj* obj = PyObject_New(mat_obj, a->ob_type);
	vmath_mat_transpose(((mat_obj*)a)->m, ((mat_obj*)a)->d, obj->m);
	obj->d = ((mat_obj*)a)->d;
	return (PyObject*)obj;
}

static PyObject* mat_inverse(PyObject * self, PyObject * args) {
	PyObject* a = NULL;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;
	if (a->ob_type != &Mat22Type && a->ob_type != &Mat33Type && a->ob_type != &Mat44Type) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return  NULL;
	}
	mat_obj* obj = PyObject_New(mat_obj, a->ob_type);
	vmath_mat_inverse(((mat_obj*)a)->m, ((mat_obj*)a)->d, obj->m);
	obj->d = ((mat_obj*)a)->d;
	return (PyObject*)obj;
}

static PyObject* mat_orthoInverse(PyObject * self, PyObject * args) {
	PyObject* a = NULL;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;
	if (a->ob_type != &Mat44Type) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return  NULL;
	}
	mat_obj* obj = PyObject_New(mat_obj, a->ob_type);
	vmath_mat4_orthoInverse(((mat_obj*)a)->m, obj->m);
	obj->d = 4;
	return (PyObject*)obj;
}

static PyObject* mat_determinant(PyObject * self, PyObject * args) {
	PyObject* a = NULL;
	if (!PyArg_ParseTuple(args, "O", &a)) return NULL;
	if (a->ob_type != &Mat22Type && a->ob_type != &Mat33Type && a->ob_type != &Mat44Type) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return  NULL;
	}
	float det = vmath_mat_determinant(((mat_obj*)a)->m, ((mat_obj*)a)->d);
	return PyFloat_FromDouble((double)det);
}

static PyObject* mat_scale(PyObject * self, PyObject * args) {

	int d;
	PyObject* arg = PyTuple_GET_ITEM(args, 0);
	if (!PyLong_Check(arg)) {
		PyErr_SetString(PyExc_ValueError, "1st argument needs to integer for dimension.");
		return NULL;
	}
	d = PyLong_AsLong(arg);
	if (d > 4) d = 4;
	float v[4];
	getVectorFromArg(args, d, v);

	mat_obj* obj;
	if (d == 2)
		obj = PyObject_New(mat_obj, &Mat22Type);
	else if (d == 3)
		obj = PyObject_New(mat_obj, &Mat33Type);
	else if (d == 4)
		obj = PyObject_New(mat_obj, &Mat44Type);
	else {
		PyErr_SetString(PyExc_ValueError, "dimension can only be 2,3or4");
		return  NULL;
	}
	vmath_mat_scale(v, d, obj->m);

	obj->d = d;
	return (PyObject*)obj;
}

static PyObject* mat_appendScale(PyObject * self, PyObject * args) {

	PyObject* a = PyTuple_GET_ITEM(args, 0);
	if (a->ob_type != &Mat22Type && a->ob_type != &Mat33Type && a->ob_type != &Mat44Type) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	float v[4];
	getVectorFromArg(args, ((mat_obj*)a)->d, v);

	mat_obj* obj = PyObject_New(mat_obj, a->ob_type);
	if (!obj) return NULL;

	vmath_mat_appendScale(((mat_obj*)a)->m, v, ((mat_obj*)a)->d, ((mat_obj*)a)->d, obj->m);
	obj->d = ((mat_obj*)a)->d;

	return (PyObject*)obj;
}

static PyObject* mat_prependScale(PyObject * self, PyObject * args) {
	PyObject* a = PyTuple_GET_ITEM(args, 0);
	if (a->ob_type != &Mat22Type && a->ob_type != &Mat33Type && a->ob_type != &Mat44Type) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	float v[4];
	getVectorFromArg(args, ((mat_obj*)a)->d, v);

	mat_obj* obj = PyObject_New(mat_obj, a->ob_type);
	if (!obj) return NULL;

	vmath_mat_prependScale(((mat_obj*)a)->m, v, ((mat_obj*)a)->d, ((mat_obj*)a)->d, obj->m);
	obj->d = ((mat_obj*)a)->d;

	return (PyObject*)obj;
}

static PyObject* mat_translation(PyObject * self, PyObject * args) {

	float v[4];
	getVectorFromArg(args, 3, v, 0);

	mat_obj* obj = PyObject_New(mat_obj, &Mat44Type);
	if (!obj) return NULL;

	vmath_mat4_translation(v, obj->m);
	obj->d = 4;

	return (PyObject*)obj;
}

static PyObject* mat_lookAt(PyObject * self, PyObject * args) {

	PyObject* eyePos;
	PyObject* lookAtPos;
	PyObject* upVec;
	if (!PyArg_ParseTuple(args, "OOO", &eyePos, &lookAtPos, &upVec)) return NULL;
	int d1, d2, d3;
	float eyePosBuf[4];
	float lookAtPosBuf[4];
	float upVecBuf[4];
	float* eyePosVect = pyObjToFloat(eyePos, eyePosBuf, d1);
	float* lookAtPosVect = pyObjToFloat(lookAtPos, lookAtPosBuf, d2);
	float* upVecVect = pyObjToFloat(upVec, upVecBuf, d3);

	mat_obj* obj = PyObject_New(mat_obj, &Mat44Type);
	if (!obj) return NULL;
	vmath_mat4_lookAt(eyePosVect, lookAtPosVect, upVecVect, obj->m);
	obj->d = 4;

	return (PyObject*)obj;
}

static PyObject* mat_perspective(PyObject * self, PyObject * args, PyObject* kwdargs) {
	float fovyRadians, aspect, zNear, zFar;

	static char* keywords[]  = { "fovyRadians", "aspect", "zNear", "zFar", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwdargs, "ffff", keywords, &fovyRadians, &aspect, &zNear, &zFar)) return NULL;

	mat_obj* obj = PyObject_New(mat_obj, &Mat44Type);
	if (!obj) return NULL;
	vmath_mat4_perspective(fovyRadians, aspect, zNear, zFar, obj->m);
	obj->d = 4;

	return (PyObject*)obj;
}

static PyObject* mat_frustum(PyObject * self, PyObject * args) {
	float left, right, bottom, top, zNear, zFar;
	if (!PyArg_ParseTuple(args, "ffffff", &left, &right, &bottom, &top, &zNear, &zFar)) return NULL;
	mat_obj* obj = PyObject_New(mat_obj, &Mat44Type);
	if (!obj) return NULL;
	vmath_mat4_frustum(left, right, bottom, top, zNear, zFar, obj->m);
	obj->d = 4;

	return (PyObject*)obj;
}

static PyObject* mat_orthographic(PyObject * self, PyObject * args) {
	float left, right, bottom, top, zNear, zFar;
	if (!PyArg_ParseTuple(args, "ffffff", &left, &right, &bottom, &top, &zNear, &zFar)) return NULL;
	mat_obj* obj = PyObject_New(mat_obj, &Mat44Type);
	if (!obj) return NULL;
	vmath_mat4_orthographic(left, right, bottom, top, zNear, zFar, obj->m);
	obj->d = 4;

	return (PyObject*)obj;
}

static PyObject* vec_self_normalize(PyObject* self) {

	vmath_normalize(((vec_obj*)self)->v, ((vec_obj*)self)->d, ((vec_obj*)self)->v);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* mat_getCol(PyObject* self, PyObject* args) {

	uint32_t row;
	if (!PyArg_ParseTuple(args, "i", &row)) return NULL;
	if (row >= (uint32_t)((mat_obj*)self)->d) {
		PyErr_SetString(PyExc_ValueError, "index is out of range");
		return NULL;
	}
	vec_obj* obj = NULL;
	if (((mat_obj*)self)->d == 2)
		obj = PyObject_New(vec_obj, &Vec2Type);
	else if (((mat_obj*)self)->d == 3)
		obj = PyObject_New(vec_obj, &Vec3Type);
	else if (((mat_obj*)self)->d == 4)
		obj = PyObject_New(vec_obj, &Vec4Type);
	if (!obj) return NULL;
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;

	for (int i = 0; i < ((mat_obj*)self)->d; i++)
		obj->v[i] = ((mat_obj*)self)->m[row * ((mat_obj*)self)->d + i];
	obj->d = ((mat_obj*)self)->d;

	return (PyObject*)obj;
}

static PyObject* mat_getRow(PyObject* self, PyObject* args) {

	uint32_t col;
	if (!PyArg_ParseTuple(args, "i", &col)) return NULL;
	if (col >= (uint32_t)((mat_obj*)self)->d) {
		PyErr_SetString(PyExc_ValueError, "index is out of range");
		return NULL;
	}
	vec_obj* obj = NULL;
	if (((mat_obj*)self)->d == 2)
		obj = PyObject_New(vec_obj, &Vec2Type);
	else if (((mat_obj*)self)->d == 3)
		obj = PyObject_New(vec_obj, &Vec3Type);
	else if (((mat_obj*)self)->d == 4)
		obj = PyObject_New(vec_obj, &Vec4Type);
	if (!obj) return NULL;
	obj->v[0] = obj->v[1] = obj->v[2] = obj->v[3] = 0.0f;

	for (int i = 0; i < ((mat_obj*)self)->d; i++)
		obj->v[i] = ((mat_obj*)self)->m[i * ((mat_obj*)self)->d + col];
	obj->d = ((mat_obj*)self)->d;

	return (PyObject*)obj;
}

static PyObject* mat_setCol(PyObject* self, PyObject* args) {

	uint32_t row;
	PyObject* arg = PyTuple_GET_ITEM(args, 0);
	if (!PyLong_Check(arg)) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	row = (uint32_t)PyLong_AsLong(arg);
	if (row >= (uint32_t)((mat_obj*)self)->d) {
		PyErr_SetString(PyExc_ValueError, "index is out of range");
		return NULL;
	}
	float v[4];
	getVectorFromArg(args, ((mat_obj*)self)->d, v);

	for (int i = 0; i < ((mat_obj*)self)->d; i++)
		((mat_obj*)self)->m[row * ((mat_obj*)self)->d + i] = v[i];

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* mat_setRow(PyObject* self, PyObject* args) {
	uint32_t col;
	PyObject* arg = PyTuple_GET_ITEM(args, 0);
	if (!PyLong_Check(arg)) {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return NULL;
	}
	col = (uint32_t)PyLong_AsLong(arg);
	if (col >= (uint32_t)((mat_obj*)self)->d) {
		PyErr_SetString(PyExc_ValueError, "index is out of range");
		return NULL;
	}
	float v[4];
	getVectorFromArg(args, ((mat_obj*)self)->d, v);

	for (int i = 0; i < ((mat_obj*)self)->d; i++)
		((mat_obj*)self)->m[i * ((mat_obj*)self)->d + col] = v[i];

	Py_INCREF(Py_None);
	return Py_None;
}



static PyObject* aabb_getminEdge(aabb_obj* self)
{
	vec_obj* obj = PyObject_New(vec_obj, &Vec3Type);
	if (!obj) return NULL;
	vmath_cpy(self->min, 3, obj->v);
	obj->d = 3;
	return (PyObject*)obj;
}

static int aabb_setminEdge(aabb_obj* self, PyObject* value)
{
	int d1;
	float buff[4];
	float* v1 = pyObjToFloat((PyObject*)value, buff, d1);
	if (!v1) return NULL;
	vmath_cpy(v1, 3, self->min);
	return 0;
}

static PyObject* aabb_getmaxEdge(aabb_obj* self)
{
	vec_obj* obj = PyObject_New(vec_obj, &Vec3Type);
	if (!obj) return NULL;
	vmath_cpy(self->max, 3, obj->v);
	obj->d = 3;
	return (PyObject*)obj;
}

static int aabb_setmaxEdge(aabb_obj* self, PyObject* value)
{
	int d1;
	float buff[4];
	float* v1 = pyObjToFloat((PyObject*)value, buff, d1);
	if (!v1) return NULL;
	vmath_cpy(v1, 3, self->max);
	return 0;
}

static PyObject* aabb_getcenter(aabb_obj* self)
{
	vec_obj* obj = PyObject_New(vec_obj, &Vec3Type);
	if (!obj) return NULL;
	vmath_add(self->min, self->max, 3, obj->v);
	vmath_div(obj->v, 2.0f, 3, obj->v);
	obj->d = 3;
	return (PyObject*)obj;
}

static PyObject* aabb_getextent(aabb_obj* self)
{
	vec_obj* obj = PyObject_New(vec_obj, &Vec3Type);
	if (!obj) return NULL;
	vmath_sub(self->max, self->min, 3, obj->v);
	obj->d = 3;
	return (PyObject*)obj;
}

static PyObject* aabb_getvolume(aabb_obj* self)
{
	float v[3];
	vmath_sub(self->max, self->min, 3, v);
	return PyFloat_FromDouble(v[0] * v[1] * v[2]);
}

static PyObject* aabb_getarea(aabb_obj* self)
{
	float v[3];
	vmath_sub(self->max, self->min, 3, v);
	return PyFloat_FromDouble(2 * (v[0] * v[1] + v[0] * v[2] + v[1] * v[2]));
}

static PyObject* aabb_getlengthSqr(aabb_obj* self)
{
	float v[3];
	vmath_sub(self->max, self->min, 3, v);
	return PyFloat_FromDouble(vmath_lengthSqr(v, 3));
}

int aabbArgs(PyObject* args, float* buff) {
	int ct = 0;
	Py_ssize_t n = PyTuple_Size(args);
	for (Py_ssize_t i = 0; i < n; i++) {
		PyObject* arg = PyTuple_GET_ITEM(args, i);
		if (PyFloat_Check(arg) || PyLong_Check(arg)) {
			buff[ct] = (float)PyFloat_AsDouble(arg);
			ct++;
			if (ct >= 6) break;
		}
		else if (PyTuple_Check(arg)) {
			for (Py_ssize_t j = 0; j < PyTuple_Size(arg); j++) {
				PyObject* val = PyTuple_GET_ITEM(arg, j);
				buff[ct] = (float)PyFloat_AsDouble(val);
				ct++;
				if (ct >= 6) break;
			}
		}
		else if (PyList_Check(arg)) {
			for (Py_ssize_t j = 0; j < PyList_Size(arg); j++) {
				PyObject* val = PyList_GET_ITEM(arg, j);
				buff[ct] = (float)PyFloat_AsDouble(val);
				ct++;
				if (ct >= 6) break;
			}
		}
		else if (arg->ob_type == &Vec2Type || arg->ob_type == &Vec3Type) {
			vec_obj* varg = (vec_obj*)arg;
			for (int j = 0; j < varg->d; j++) {
				buff[ct] = varg->v[j];
				ct++;
			}
			if (varg->d == 2) {
				buff[ct] = 0.0f;
				ct++;
			}
		}
		else if (arg->ob_type == &AABBType) {
			aabb_obj* varg = (aabb_obj*)arg;
			buff[0] = varg->min[0];
			buff[1] = varg->min[1];
			buff[2] = varg->min[2];
			buff[3] = varg->max[0];
			buff[4] = varg->max[1];
			buff[5] = varg->max[2];
			ct = 6;
			break;
		}
	}
	return ct;
}



static PyObject* aabb_new(PyTypeObject* type, PyObject* args, PyObject* kw) {

	aabb_obj* self;
	self = (aabb_obj*)type->tp_alloc(type, 0);
	if (!self) return NULL;

	float initalvalue[6];
	int ct = aabbArgs(args, initalvalue);

	if (ct == 0) {
		self->min[0] = 3.402823e+38;
		self->min[1] = 3.402823e+38;
		self->min[2] = 3.402823e+38;
		self->max[0] = -3.402823e+38;
		self->max[1] = -3.402823e+38;
		self->max[2] = -3.402823e+38;
	}
	else {
		if (ct >= 3) {
			self->min[0] = initalvalue[0];
			self->min[1] = initalvalue[1];
			self->min[2] = initalvalue[2];
		}
		if (ct == 6) {
			self->max[0] = initalvalue[3];
			self->max[1] = initalvalue[4];
			self->max[2] = initalvalue[5];
		}
		else {
			self->max[0] = initalvalue[0];
			self->max[1] = initalvalue[1];
			self->max[2] = initalvalue[2];
		}
	}
	return (PyObject*)self;
}

static PyObject* aabb_str(aabb_obj* self)
{
	char buf[256];
	snprintf(buf, 256, "min(%f,%f,%f) - max:(%f,%f,%f)", self->min[0], self->min[1], self->min[2], self->max[0], self->max[1], self->max[2]);
	return _PyUnicode_FromASCII(buf, strlen(buf));
}


static PyObject* aabb_reset(aabb_obj* self, PyObject* args)
{
	float initalvalue[6];
	int ct = aabbArgs(args, initalvalue);

	if (ct == 0) {
		self->min[0] = 3.402823e+38;
		self->min[1] = 3.402823e+38;
		self->min[2] = 3.402823e+38;
		self->max[0] = -3.402823e+38;
		self->max[1] = -3.402823e+38;
		self->max[2] = -3.402823e+38;
	}
	else {
		if (ct >= 3) {
			self->min[0] = initalvalue[0];
			self->min[1] = initalvalue[1];
			self->min[2] = initalvalue[2];
		}
		if (ct == 6) {
			self->max[0] = initalvalue[3];
			self->max[1] = initalvalue[4];
			self->max[2] = initalvalue[5];
		}
		else {
			self->max[0] = initalvalue[0];
			self->max[1] = initalvalue[1];
			self->max[2] = initalvalue[2];
		}
	}
	Py_INCREF(Py_None);
	return Py_None;
}


void addInternalPoint(aabb_obj* self, float x, float y, float z)
{
	if (x > self->max[0]) self->max[0]=x;
	if (y > self->max[1]) self->max[1]=y;
	if (z > self->max[2]) self->max[2]=z;
	if (x < self->min[0]) self->min[0]=x;
	if (y < self->min[1]) self->min[1]=y;
	if (z < self->min[2]) self->min[2]=z;
}

static PyObject* aabb_insert(aabb_obj* self, PyObject* args)
{
	float initalvalue[6];
	int ct = aabbArgs(args, initalvalue);
	if (ct >= 3)
		addInternalPoint(self, initalvalue[0], initalvalue[1], initalvalue[2]);
	if (ct == 6)
		addInternalPoint(self, initalvalue[3], initalvalue[4], initalvalue[5]);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* aabb_repair(aabb_obj* self, PyObject* args)
{
	float t;
	for (int i = 0; i < 3; i++) {
		if (self->min[i] > self->max[i]){
			t = self->min[i];
			self->min[i] = self->max[i];
			self->max[i] = t;
		}
	}
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* aabb_isInside(aabb_obj* self, PyObject* args)
{
	float v[6];
	int ct = aabbArgs(args, v);
	bool isInside = false;
	if (ct >= 3) {
		isInside=(v[0] >= self->min[0] && v[0] <= self->max[0] &&
				  v[1] >= self->min[1] && v[1] <= self->max[1] &&
				  v[2] >= self->min[2] && v[2] <= self->max[2]);
	}
	else if (ct == 6) {
		isInside = (self->min[0] <= v[3] && self->min[1] <= v[4] && self->min[2] <= v[5] &&
					self->max[0] >= v[0] && self->max[1] >= v[1] && self->max[2] >= v[2]);
	}
	return PyBool_FromLong((long)isInside);
}

static PyNumberMethods vec_as_number = {
(binaryfunc)vec_add,   /* nb_add */
(binaryfunc)vec_sub,   /* nb_subtract */
(binaryfunc)vec_mul,   /* nb_multiply */
0,						/* nb_remainder */
0,						/* nb_divmod */
0,						/* nb_power */
(unaryfunc)vec_neg,		/* nb_negative */
0,						/* nb_positive */
0,						/* nb_absolute */
0,						/* nb_bool */
0,						/* nb_invert */
0,						/* nb_lshift */
0,						/* nb_rshift */
0,						/* nb_and */
0,						/* nb_xor */
0,						/* nb_or */
0,						/* nb_int */
0,						/* nb_reserved */
0,						/* nb_float */
0,						/* nb_inplace_add */
0,						/* nb_inplace_subtract */
0,						/* nb_inplace_multiply */
0,						/* nb_inplace_remainder */
0,						/* nb_inplace_power */
0,						/* nb_inplace_lshift */
0,						/* nb_inplace_rshift */
0,						/* nb_inplace_and */
0,						/* nb_inplace_xor */
0,						/* nb_inplace_or */
0,						/* nb_floor_divide */
(binaryfunc)vec_div,	/* nb_true_divide */
0,						/* nb_inplace_floor_divide */
0,						/* nb_inplace_true_divide */
};

static PyNumberMethods mat_as_number = {
(binaryfunc)mat_add,   /* nb_add */
(binaryfunc)mat_sub,   /* nb_subtract */
(binaryfunc)mat_mul,   /* nb_multiply */
0,						/* nb_remainder */
0,						/* nb_divmod */
0,						/* nb_power */
(unaryfunc)mat_neg,		/* nb_negative */
0,						/* nb_positive */
0,						/* nb_absolute */
0,						/* nb_bool */
0,						/* nb_invert */
0,						/* nb_lshift */
0,						/* nb_rshift */
0,						/* nb_and */
0,						/* nb_xor */
0,						/* nb_or */
0,						/* nb_int */
0,						/* nb_reserved */
0,						/* nb_float */
0,						/* nb_inplace_add */
0,						/* nb_inplace_subtract */
0,						/* nb_inplace_multiply */
0,						/* nb_inplace_remainder */
0,						/* nb_inplace_power */
0,						/* nb_inplace_lshift */
0,						/* nb_inplace_rshift */
0,						/* nb_inplace_and */
0,						/* nb_inplace_xor */
0,						/* nb_inplace_or */
0,						/* nb_floor_divide */
0,						/* nb_true_divide */
0,						/* nb_inplace_floor_divide */
0,						/* nb_inplace_true_divide */
};

static PyMethodDef vec_methods[] = {
	{ "setElem",	(PyCFunction)vec_setElem,	METH_VARARGS },
	{ "getElem",	(PyCFunction)vec_getElem,	METH_VARARGS },
	{ "normalize",	(PyCFunction)vec_self_normalize,METH_VARARGS },
	{ NULL,	NULL }
};

static PyMethodDef mat_methods[] = {
	{ "setElem",	(PyCFunction)mat_setElem,	METH_VARARGS },
	{ "getElem",	(PyCFunction)mat_getElem,	METH_VARARGS },
	{ "getCol",		(PyCFunction)mat_getCol,	METH_VARARGS },
	{ "getRow",		(PyCFunction)mat_getRow,	METH_VARARGS },
	{ "setCol",		(PyCFunction)mat_setCol,	METH_VARARGS },
	{ "setRow",		(PyCFunction)mat_setRow,	METH_VARARGS },
	{ NULL,	NULL }
};

PyGetSetDef vec2_getsets[] = {
	{ const_cast<char*>("x"), (getter)vec_getX, (setter)vec_setX,NULL, NULL },
	{ const_cast<char*>("y"), (getter)vec_getY, (setter)vec_setY,NULL, NULL },
	{ NULL, NULL }
};
PyGetSetDef vec3_getsets[] = {
	{ const_cast<char*>("x"), (getter)vec_getX, (setter)vec_setX,NULL, NULL },
	{ const_cast<char*>("y"), (getter)vec_getY, (setter)vec_setY,NULL, NULL },
	{ const_cast<char*>("z"), (getter)vec_getZ, (setter)vec_setZ,NULL, NULL },
	{ NULL, NULL }
};
PyGetSetDef vec4_getsets[] = {
	{ const_cast<char*>("x"), (getter)vec_getX, (setter)vec_setX,NULL, NULL },
	{ const_cast<char*>("y"), (getter)vec_getY, (setter)vec_setY,NULL, NULL },
	{ const_cast<char*>("z"), (getter)vec_getZ, (setter)vec_setZ,NULL, NULL },
	{ const_cast<char*>("w"), (getter)vec_getW, (setter)vec_setW,NULL, NULL },
	{ NULL, NULL }
};


PyObject* mat_getM00(mat_obj * self) { return PyFloat_FromDouble((double)self->m[0]); }
int mat_setM00(mat_obj * self, PyObject * value) { self->m[0] = (float)PyFloat_AsDouble(value); return 0; }
PyObject* mat_getM01(mat_obj * self) { return PyFloat_FromDouble((double)self->m[1]); }
int mat_setM01(mat_obj * self, PyObject * value) { self->m[1] = (float)PyFloat_AsDouble(value); return 0; }
PyObject* mat_getM02(mat_obj * self) { return PyFloat_FromDouble((double)self->m[2]); }
int mat_setM02(mat_obj * self, PyObject * value) { self->m[2] = (float)PyFloat_AsDouble(value); return 0; }
PyObject* mat_getM03(mat_obj * self) { return PyFloat_FromDouble((double)self->m[3]); }
int mat_setM03(mat_obj * self, PyObject * value) { self->m[3] = (float)PyFloat_AsDouble(value); return 0; }

PyObject* mat_getM10(mat_obj * self) { return PyFloat_FromDouble((double)self->m[self->d + 0]); }
int mat_setM10(mat_obj * self, PyObject * value) { self->m[4] = (float)PyFloat_AsDouble(value); return 0; }
PyObject* mat_getM11(mat_obj * self) { return PyFloat_FromDouble((double)self->m[self->d + 1]); }
int mat_setM11(mat_obj * self, PyObject * value) { self->m[5] = (float)PyFloat_AsDouble(value); return 0; }
PyObject* mat_getM12(mat_obj * self) { return PyFloat_FromDouble((double)self->m[self->d + 2]); }
int mat_setM12(mat_obj * self, PyObject * value) { self->m[6] = (float)PyFloat_AsDouble(value); return 0; }
PyObject* mat_getM13(mat_obj * self) { return PyFloat_FromDouble((double)self->m[self->d + 3]); }
int mat_setM13(mat_obj * self, PyObject * value) { self->m[7] = (float)PyFloat_AsDouble(value); return 0; }

PyObject* mat_getM20(mat_obj * self) { return PyFloat_FromDouble((double)self->m[self->d*2 + 0]); }
int mat_setM20(mat_obj * self, PyObject * value) { self->m[8] = (float)PyFloat_AsDouble(value); return 0; }
PyObject* mat_getM21(mat_obj * self) { return PyFloat_FromDouble((double)self->m[self->d * 2 + 1]); }
int mat_setM21(mat_obj * self, PyObject * value) { self->m[9] = (float)PyFloat_AsDouble(value); return 0; }
PyObject* mat_getM22(mat_obj * self) { return PyFloat_FromDouble((double)self->m[self->d * 2 + 2]); }
int mat_setM22(mat_obj * self, PyObject * value) { self->m[10] = (float)PyFloat_AsDouble(value); return 0; }
PyObject* mat_getM23(mat_obj * self) { return PyFloat_FromDouble((double)self->m[self->d * 2 + 3]); }
int mat_setM23(mat_obj * self, PyObject * value) { self->m[11] = (float)PyFloat_AsDouble(value); return 0; }

PyObject* mat_getM30(mat_obj * self) { return PyFloat_FromDouble((double)self->m[12]); }
int mat_setM30(mat_obj * self, PyObject * value) { self->m[12] = (float)PyFloat_AsDouble(value); return 0; }
PyObject* mat_getM31(mat_obj * self) { return PyFloat_FromDouble((double)self->m[13]); }
int mat_setM31(mat_obj * self, PyObject * value) { self->m[13] = (float)PyFloat_AsDouble(value); return 0; }
PyObject* mat_getM32(mat_obj * self) { return PyFloat_FromDouble((double)self->m[14]); }
int mat_setM32(mat_obj * self, PyObject * value) { self->m[14] = (float)PyFloat_AsDouble(value); return 0; }
PyObject* mat_getM33(mat_obj * self) { return PyFloat_FromDouble((double)self->m[15]); }
int mat_setM33(mat_obj * self, PyObject * value) { self->m[15] = (float)PyFloat_AsDouble(value); return 0; }

PyGetSetDef mat22_getsets[] = {
	{ const_cast<char*>("m00"), (getter)mat_getM00, (setter)mat_setM00,NULL, NULL },
	{ const_cast<char*>("m01"), (getter)mat_getM01, (setter)mat_setM01,NULL, NULL },
	{ const_cast<char*>("m10"), (getter)mat_getM10, (setter)mat_setM10,NULL, NULL },
	{ const_cast<char*>("m11"), (getter)mat_getM11, (setter)mat_setM11,NULL, NULL },
	{ NULL, NULL }
};

PyGetSetDef mat33_getsets[] = {
	{ const_cast<char*>("m00"), (getter)mat_getM00, (setter)mat_setM00,NULL, NULL },
	{ const_cast<char*>("m01"), (getter)mat_getM01, (setter)mat_setM01,NULL, NULL },
	{ const_cast<char*>("m02"), (getter)mat_getM02, (setter)mat_setM02,NULL, NULL },

	{ const_cast<char*>("m10"), (getter)mat_getM10, (setter)mat_setM10,NULL, NULL },
	{ const_cast<char*>("m11"), (getter)mat_getM11, (setter)mat_setM11,NULL, NULL },
	{ const_cast<char*>("m12"), (getter)mat_getM12, (setter)mat_setM12,NULL, NULL },

	{ const_cast<char*>("m20"), (getter)mat_getM20, (setter)mat_setM20,NULL, NULL },
	{ const_cast<char*>("m21"), (getter)mat_getM21, (setter)mat_setM21,NULL, NULL },
	{ const_cast<char*>("m22"), (getter)mat_getM22, (setter)mat_setM22,NULL, NULL },
	{ NULL, NULL }
};

PyGetSetDef mat44_getsets[] = {
	{ const_cast<char*>("m00"), (getter)mat_getM00, (setter)mat_setM00,NULL, NULL },
	{ const_cast<char*>("m01"), (getter)mat_getM01, (setter)mat_setM01,NULL, NULL },
	{ const_cast<char*>("m02"), (getter)mat_getM02, (setter)mat_setM02,NULL, NULL },
	{ const_cast<char*>("m03"), (getter)mat_getM03, (setter)mat_setM03,NULL, NULL },

	{ const_cast<char*>("m10"), (getter)mat_getM10, (setter)mat_setM10,NULL, NULL },
	{ const_cast<char*>("m11"), (getter)mat_getM11, (setter)mat_setM11,NULL, NULL },
	{ const_cast<char*>("m12"), (getter)mat_getM12, (setter)mat_setM12,NULL, NULL },
	{ const_cast<char*>("m13"), (getter)mat_getM13, (setter)mat_setM13,NULL, NULL },

	{ const_cast<char*>("m20"), (getter)mat_getM20, (setter)mat_setM20,NULL, NULL },
	{ const_cast<char*>("m21"), (getter)mat_getM21, (setter)mat_setM21,NULL, NULL },
	{ const_cast<char*>("m22"), (getter)mat_getM22, (setter)mat_setM22,NULL, NULL },
	{ const_cast<char*>("m23"), (getter)mat_getM23, (setter)mat_setM23,NULL, NULL },

	{ const_cast<char*>("m30"), (getter)mat_getM30, (setter)mat_setM30,NULL, NULL },
	{ const_cast<char*>("m31"), (getter)mat_getM31, (setter)mat_setM31,NULL, NULL },
	{ const_cast<char*>("m32"), (getter)mat_getM32, (setter)mat_setM32,NULL, NULL },
	{ const_cast<char*>("m33"), (getter)mat_getM33, (setter)mat_setM33,NULL, NULL },
	{ NULL, NULL }
};

PyGetSetDef aabb_getsets[] = {
	{ const_cast<char*>("minEdge"),   (getter)aabb_getminEdge,   (setter)aabb_setminEdge, minEdge_doc, NULL },
	{ const_cast<char*>("maxEdge"),   (getter)aabb_getmaxEdge,   (setter)aabb_setmaxEdge, maxEdge_doc, NULL },
	{ const_cast<char*>("center"),    (getter)aabb_getcenter,    (setter)NULL,center_doc, NULL },
	{ const_cast<char*>("extent"),    (getter)aabb_getextent,    (setter)NULL,extent_doc, NULL },
	{ const_cast<char*>("volume"),    (getter)aabb_getvolume,    (setter)NULL,volume_doc, NULL },
	{ const_cast<char*>("area"),      (getter)aabb_getarea,      (setter)NULL,area_doc, NULL },
	{ const_cast<char*>("lengthSqr"), (getter)aabb_getlengthSqr, (setter)NULL,aabb_lengthSqr_doc, NULL },
	{ NULL, NULL }
	};

static PyMethodDef aabb_methods[] = {
	{"reset", (PyCFunction)aabb_reset, METH_VARARGS, reset_doc},
	{"insert", (PyCFunction)aabb_insert, METH_VARARGS, insert_doc},
	{"repair", (PyCFunction)aabb_repair, METH_VARARGS, repair_doc},
	{"isInside", (PyCFunction)aabb_isInside, METH_VARARGS, isInside_doc},
	{ nullptr, nullptr, 0, nullptr }
};

PyTypeObject Vec2Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"pyvmath.vec2",						/* tp_name */
	sizeof(vec_obj),                    /* tp_basicsize */
	0,                                  /* tp_itemsize */
	0,						            /* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	&vec_as_number,                     /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)vec_str,                  /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	vec2_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	vec_richcompare,                    /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	vec_methods,						/* tp_methods */
	0,                                  /* tp_members */
	vec2_getsets,                       /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	vec_new,							/* tp_new */
	0,									/* tp_free */
};
PyTypeObject Vec3Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"pyvmath.vec3",						/* tp_name */
	sizeof(vec_obj),                    /* tp_basicsize */
	0,                                  /* tp_itemsize */
	0,						            /* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	&vec_as_number,                     /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)vec_str,                  /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	vec3_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	vec_richcompare,                    /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	vec_methods,						/* tp_methods */
	0,                                  /* tp_members */
	vec3_getsets,                       /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	vec_new,							/* tp_new */
	0,									/* tp_free */
};
PyTypeObject Vec4Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"pyvmath.vec4",						/* tp_name */
	sizeof(vec_obj),                    /* tp_basicsize */
	0,                                  /* tp_itemsize */
	0,						            /* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	&vec_as_number,                     /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)vec_str,                  /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	vec4_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	vec_richcompare,                    /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	vec_methods,						/* tp_methods */
	0,                                  /* tp_members */
	vec4_getsets,                       /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	vec_new,							/* tp_new */
	0,									/* tp_free */
};
PyTypeObject QuatType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"pyvmath.quat",						/* tp_name */
	sizeof(vec_obj),                    /* tp_basicsize */
	0,                                  /* tp_itemsize */
	0,						            /* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	&vec_as_number,                     /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)vec_str,                  /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	quat_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	vec_richcompare,                    /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	vec_methods,						/* tp_methods */
	0,                                  /* tp_members */
	vec4_getsets,                       /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	vec_new,							/* tp_new */
	0,									/* tp_free */
};
PyTypeObject Mat22Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"pyvmath.mat22",						/* tp_name */
	sizeof(mat_obj),                    /* tp_basicsize */
	0,                                  /* tp_itemsize */
	0,						            /* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	&mat_as_number,                     /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)mat_str,                  /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	mat22_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	mat_methods,						/* tp_methods */
	0,                                  /* tp_members */
	mat22_getsets,                      /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	mat_new,							/* tp_new */
	0,									/* tp_free */
};
PyTypeObject Mat33Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"pyvmath.mat33",						/* tp_name */
	sizeof(mat_obj),                    /* tp_basicsize */
	0,                                  /* tp_itemsize */
	0,						            /* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	&mat_as_number,                     /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)mat_str,                  /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	mat33_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	mat_methods,						/* tp_methods */
	0,                                  /* tp_members */
	mat33_getsets,                      /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	mat_new,							/* tp_new */
	0,									/* tp_free */
};
PyTypeObject Mat44Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"pyvmath.mat44",						/* tp_name */
	sizeof(mat_obj),                    /* tp_basicsize */
	0,                                  /* tp_itemsize */
	0,						            /* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	&mat_as_number,                     /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)mat_str,                  /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	mat44_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	mat_methods,						/* tp_methods */
	0,                                  /* tp_members */
	mat44_getsets,                      /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	mat_new,							/* tp_new */
	0,									/* tp_free */
};
PyTypeObject AABBType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"pyvmath.aabb",						/* tp_name */
	sizeof(mat_obj),                    /* tp_basicsize */
	0,                                  /* tp_itemsize */
	0,						            /* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,									/* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)aabb_str,                 /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	aabb_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	aabb_methods,						/* tp_methods */
	0,                                  /* tp_members */
	aabb_getsets,                      /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	aabb_new,							/* tp_new */
	0,									/* tp_free */
};

static PyMethodDef vmath_methods[] = {
	{ "add", (PyCFunction)vec_mat_add, METH_VARARGS,add_doc },
	{ "sub", (PyCFunction)vec_mat_sub, METH_VARARGS,sub_doc },
	{ "mul", (PyCFunction)vec_mat_mul, METH_VARARGS,mul_doc },
	{ "div", (PyCFunction)vec_div2, METH_VARARGS, div_doc},
	{ "recip", (PyCFunction)vec_recipPerElem, METH_VARARGS, recip_doc},
	{ "sqrt", (PyCFunction)vec_sqrtPerElem, METH_VARARGS, sqrt_doc},
	{ "rsqrt", (PyCFunction)vec_rsqrtPerElem, METH_VARARGS, rsqrt_doc},
	{ "abs", (PyCFunction)vec_absPerElem, METH_VARARGS, abs_doc},
	{ "max", (PyCFunction)vec_maxPerElem, METH_VARARGS, max_doc},
	{ "maxElem", (PyCFunction)vec_maxElem, METH_VARARGS, maxElem_doc},
	{ "min", (PyCFunction)vec_minPerElem, METH_VARARGS, min_doc},
	{ "minElem", (PyCFunction)vec_minElem, METH_VARARGS, minElem_doc},
	{ "sum", (PyCFunction)vec_sum, METH_VARARGS, sum_doc},
	{ "dot", (PyCFunction)vec_dot, METH_VARARGS, dot_doc},
	{ "lengthSqr", (PyCFunction)vec_lengthSqr, METH_VARARGS, lengthSqr_doc},
	{ "length", (PyCFunction)vec_length, METH_VARARGS, length_doc},
	{ "normalize", (PyCFunction)vec_normalize, METH_VARARGS, normalize_doc},
	{ "cross", (PyCFunction)vec_cross, METH_VARARGS, cross_doc},
	{ "lerp", (PyCFunction)vec_lerp, METH_VARARGS, lerp_doc},
	{ "slerp", (PyCFunction)vec_slerp, METH_VARARGS, slerp_doc},
	{"quat_rotation", (PyCFunction)quat_rotation, METH_VARARGS, quat_rotation_doc},
	{"quat_rotationX", (PyCFunction)quat_rotationX, METH_VARARGS, quat_rotationX_doc},
	{"quat_rotationY", (PyCFunction)quat_rotationY, METH_VARARGS, quat_rotationY_doc},
	{"quat_rotationZ", (PyCFunction)quat_rotationZ, METH_VARARGS, quat_rotationZ_doc},
	{"conj", (PyCFunction)quat_conj, METH_VARARGS, conj_doc},
	{"squad", (PyCFunction)quat_squad, METH_VARARGS, squad_doc},
	{"rotate", (PyCFunction)quat_rotate, METH_VARARGS, rotate_doc},
	{"mat_rotation", (PyCFunction)mat_rotation, METH_VARARGS, mat_rotation_doc},
	{"mat_rotationX", (PyCFunction)mat_rotationX, METH_VARARGS, mat_rotationX_doc},
	{"mat_rotationY", (PyCFunction)mat_rotationY, METH_VARARGS, mat_rotationY_doc},
	{"mat_rotationZ", (PyCFunction)mat_rotationZ, METH_VARARGS, mat_rotationZ_doc},
	{"mat_rotationZYX", (PyCFunction)mat_rotationZYX, METH_VARARGS, mat_rotationZYX_doc},
	{"mat_identity", (PyCFunction)mat_identity, METH_VARARGS, mat_identity_doc},
	{"mat_scale", (PyCFunction)mat_scale, METH_VARARGS, mat_scale_doc},
	{"mat_translation", (PyCFunction)mat_translation, METH_VARARGS, mat_translation_doc},
	{"transpose", (PyCFunction)mat_transpose, METH_VARARGS, transpose_doc},
	{"inverse", (PyCFunction)mat_inverse, METH_VARARGS, inverse_doc},
	{"orthoInverse", (PyCFunction)mat_orthoInverse, METH_VARARGS, orthoInverse_doc},
	{"determinant", (PyCFunction)mat_determinant, METH_VARARGS, determinant_doc},
	{"appendScale", (PyCFunction)mat_appendScale, METH_VARARGS, appendScale_doc},
	{"prependScale", (PyCFunction)mat_prependScale, METH_VARARGS, prependScale_doc},
	{"lookAt", (PyCFunction)mat_lookAt, METH_VARARGS, lookAt_doc},
	{"perspective", (PyCFunction)mat_perspective, METH_VARARGS | METH_KEYWORDS, perspective_doc},
	{"frustum", (PyCFunction)mat_frustum, METH_VARARGS, frustum_doc},
	{"orthographic", (PyCFunction)mat_orthographic, METH_VARARGS, orthographic_doc},
	{"almostEqual", (PyCFunction)vec_almostEqual, METH_VARARGS, almostEqual_doc},
{ nullptr, nullptr, 0, nullptr }
};

static PyModuleDef vmath_module = {
	PyModuleDef_HEAD_INIT,
	"pyvmath",								// Module name to use with Python import statements
	"Vector Math Module.",					// Module description
	0,
	vmath_methods							// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_pyvmath() {
	PyObject* module = PyModule_Create(&vmath_module);

	if (PyType_Ready(&Vec2Type) < 0) return NULL;
	if (PyType_Ready(&Vec3Type) < 0) return NULL;
	if (PyType_Ready(&Vec4Type) < 0) return NULL;
	if (PyType_Ready(&QuatType) < 0) return NULL;
	if (PyType_Ready(&Mat22Type) < 0) return NULL;
	if (PyType_Ready(&Mat33Type) < 0) return NULL;
	if (PyType_Ready(&Mat44Type) < 0) return NULL;
	if (PyType_Ready(&AABBType) < 0) return NULL;

	Py_INCREF(&Vec2Type);
	PyModule_AddObject(module, "vec2", (PyObject*)& Vec2Type);
	Py_INCREF(&Vec3Type);
	PyModule_AddObject(module, "vec3", (PyObject*)& Vec3Type);
	Py_INCREF(&Vec4Type);
	PyModule_AddObject(module, "vec4", (PyObject*)& Vec4Type);
	Py_INCREF(&QuatType);
	PyModule_AddObject(module, "quat", (PyObject*)& QuatType);
	Py_INCREF(&Mat22Type);
	PyModule_AddObject(module, "mat22", (PyObject*)& Mat22Type);
	Py_INCREF(&Mat33Type);
	PyModule_AddObject(module, "mat33", (PyObject*)& Mat33Type);
	Py_INCREF(&Mat44Type);
	PyModule_AddObject(module, "mat44", (PyObject*)& Mat44Type);
	Py_INCREF(&AABBType);
	PyModule_AddObject(module, "aabb", (PyObject*)& AABBType);

	return module;
}
