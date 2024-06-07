#include <Python.h>
#include <chrono>
#include <sstream>
#include <iomanip>

// ��¥ ���ڿ��� chrono::system_clock::time_point�� ��ȯ�ϴ� �Լ�
std::chrono::system_clock::time_point parse_date(const std::string& date) {
    std::istringstream ss(date);
    std::tm dt = {};
    ss >> std::get_time(&dt, "%Y%m%d");
    return std::chrono::system_clock::from_time_t(std::mktime(&dt));
}

// �־��� ��¥�� ���� �ȿ� ���ԵǴ��� Ȯ���ϴ� �Լ�
bool is_date_in_range(const std::string& start_date, const std::string& end_date, const std::string& target_date) {
    auto start = parse_date(start_date);
    auto end = parse_date(end_date);
    auto target = parse_date(target_date);
    return target >= start && target <= end;
}

// �� ���� ��¥ ������ ��ġ���� Ȯ���ϴ� �Լ�
bool are_ranges_overlapping(const std::string& start_date1, const std::string& end_date1,
    const std::string& start_date2, const std::string& end_date2) {
    auto start1 = parse_date(start_date1);
    auto end1 = parse_date(end_date1);
    auto start2 = parse_date(start_date2);
    auto end2 = parse_date(end_date2);

    // �� ���� �� �ϳ��� ��ġ�� ��찡 �ִ��� Ȯ��
    return (start1 <= end2 && end1 >= start2);
}

// ���̽㿡�� ȣ���� �� �ֵ��� �����ϴ� �Լ�: �־��� ��¥�� ���� �ȿ� ������ Ȯ��
static PyObject* spam_is_date_in_range(PyObject* self, PyObject* args) {
    const char* start_date;
    const char* end_date;
    const char* target_date;

    // �Ķ���� �Ľ�
    if (!PyArg_ParseTuple(args, "sss", &start_date, &end_date, &target_date)) {
        return NULL;
    }

    // ��¥ ���� Ȯ��
    bool result = is_date_in_range(start_date, end_date, target_date);

    // ��� ��ȯ
    if (result) {
        Py_RETURN_TRUE;
    }
    else {
        Py_RETURN_FALSE;
    }
}

// ���̽㿡�� ȣ���� �� �ֵ��� �����ϴ� �Լ�: �� ���� ��¥ ������ ��ġ���� Ȯ��
static PyObject* spam_are_ranges_overlapping(PyObject* self, PyObject* args) {
    const char* start_date1;
    const char* end_date1;
    const char* start_date2;
    const char* end_date2;

    // �Ķ���� �Ľ�
    if (!PyArg_ParseTuple(args, "ssss", &start_date1, &end_date1, &start_date2, &end_date2)) {
        return NULL;
    }

    // ���� ��ġ���� Ȯ��
    bool result = are_ranges_overlapping(start_date1, end_date1, start_date2, end_date2);

    // ��� ��ȯ
    if (result) {
        Py_RETURN_TRUE;
    }
    else {
        Py_RETURN_FALSE;
    }
}

// �޼ҵ� ����
static PyMethodDef SpamMethods[] = {
    { "is_date_in_range", spam_is_date_in_range, METH_VARARGS, "Check if the target date is within the range." },
    { "are_ranges_overlapping", spam_are_ranges_overlapping, METH_VARARGS, "Check if two date ranges are overlapping." },
    { NULL, NULL, 0, NULL }
};

// ��� ����
static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",
    "It is a test module.",
    -1,
    SpamMethods
};

// ��� �ʱ�ȭ �Լ�
PyMODINIT_FUNC PyInit_spam(void) {
    return PyModule_Create(&spammodule);
}
