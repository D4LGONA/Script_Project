#include <Python.h>
#include <chrono>
#include <sstream>
#include <iomanip>

// 날짜 문자열을 chrono::system_clock::time_point로 변환하는 함수
std::chrono::system_clock::time_point parse_date(const std::string& date) {
    std::istringstream ss(date);
    std::tm dt = {};
    ss >> std::get_time(&dt, "%Y%m%d");
    return std::chrono::system_clock::from_time_t(std::mktime(&dt));
}

// 주어진 날짜가 범위 안에 포함되는지 확인하는 함수
bool is_date_in_range(const std::string& start_date, const std::string& end_date, const std::string& target_date) {
    auto start = parse_date(start_date);
    auto end = parse_date(end_date);
    auto target = parse_date(target_date);
    return target >= start && target <= end;
}

// 두 개의 날짜 범위가 겹치는지 확인하는 함수
bool are_ranges_overlapping(const std::string& start_date1, const std::string& end_date1,
    const std::string& start_date2, const std::string& end_date2) {
    auto start1 = parse_date(start_date1);
    auto end1 = parse_date(end_date1);
    auto start2 = parse_date(start_date2);
    auto end2 = parse_date(end_date2);

    // 두 범위 중 하나라도 겹치는 경우가 있는지 확인
    return (start1 <= end2 && end1 >= start2);
}

// 파이썬에서 호출할 수 있도록 래핑하는 함수: 주어진 날짜가 범위 안에 들어가는지 확인
static PyObject* spam_is_date_in_range(PyObject* self, PyObject* args) {
    const char* start_date;
    const char* end_date;
    const char* target_date;

    // 파라미터 파싱
    if (!PyArg_ParseTuple(args, "sss", &start_date, &end_date, &target_date)) {
        return NULL;
    }

    // 날짜 범위 확인
    bool result = is_date_in_range(start_date, end_date, target_date);

    // 결과 반환
    if (result) {
        Py_RETURN_TRUE;
    }
    else {
        Py_RETURN_FALSE;
    }
}

// 파이썬에서 호출할 수 있도록 래핑하는 함수: 두 개의 날짜 범위가 겹치는지 확인
static PyObject* spam_are_ranges_overlapping(PyObject* self, PyObject* args) {
    const char* start_date1;
    const char* end_date1;
    const char* start_date2;
    const char* end_date2;

    // 파라미터 파싱
    if (!PyArg_ParseTuple(args, "ssss", &start_date1, &end_date1, &start_date2, &end_date2)) {
        return NULL;
    }

    // 범위 겹치는지 확인
    bool result = are_ranges_overlapping(start_date1, end_date1, start_date2, end_date2);

    // 결과 반환
    if (result) {
        Py_RETURN_TRUE;
    }
    else {
        Py_RETURN_FALSE;
    }
}

// 메소드 정의
static PyMethodDef SpamMethods[] = {
    { "is_date_in_range", spam_is_date_in_range, METH_VARARGS, "Check if the target date is within the range." },
    { "are_ranges_overlapping", spam_are_ranges_overlapping, METH_VARARGS, "Check if two date ranges are overlapping." },
    { NULL, NULL, 0, NULL }
};

// 모듈 정의
static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",
    "It is a test module.",
    -1,
    SpamMethods
};

// 모듈 초기화 함수
PyMODINIT_FUNC PyInit_spam(void) {
    return PyModule_Create(&spammodule);
}
