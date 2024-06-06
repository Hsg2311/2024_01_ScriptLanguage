#include <python.h>
#include <deque>
#include <chrono>
#include <string>
#include <stdexcept>
#include <string_view>
#include <fstream>
#include <ranges>
#include <algorithm>
#include <array>

using namespace std::literals;

const std::string mkTimeStamp() {
	auto tp = std::chrono::system_clock::now();
	auto tt = std::chrono::system_clock::to_time_t(tp);
	auto tm = *std::localtime(&tt);
	char buf[32];
	std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", &tm);
	return buf;
}

class SearchLog {
public:
	static consteval std::string_view searchType_Title() { return "Title"sv; }
	static consteval std::string_view searchType_Author() { return "Author"sv; }
	static consteval std::string_view searchType_Journal() { return "Journal"sv; }
	static consteval std::string_view searchType_Institution() { return "Institution"sv; }

	SearchLog(const std::string& keyword, const std::string& type, const std::string& timeStamp)
		: keyword_(keyword), type_(type), timeStamp_(timeStamp)
	{
		if (type != searchType_Title() && type != searchType_Author() && type != searchType_Journal() && type != searchType_Institution())
			throw std::invalid_argument("Invalid search type\n"
				"Available search types are Title, Author, Journal, Institution"
			);
	}

	SearchLog(const std::string& keyword, const std::string& type)
		: keyword_(keyword), type_(type), timeStamp_(mkTimeStamp())
	{
		if (type != searchType_Title() && type != searchType_Author() && type != searchType_Journal() && type != searchType_Institution())
			throw std::invalid_argument("Invalid search type\n"
				"Available search types are Title, Author, Journal, Institution"
			);
	}

	const std::string& keyword() const { return keyword_; }
	const std::string& type() const { return type_; }
	const std::string& timeStamp() const { return timeStamp_; }

private:
	std::string keyword_;
	std::string type_;
	std::string timeStamp_;
};

class ViewLog {
public:
	ViewLog(const std::string& title, const std::string& author, std::size_t year, const std::string& timeStamp)
		: title_(title), author_(author), year_(year), timeStamp_(timeStamp) {}

	ViewLog(const std::string& title, const std::string& author, std::size_t year)
		: title_(title), author_(author), year_(year), timeStamp_(mkTimeStamp()) {}

	const std::string& title() const { return title_; }
	const std::string& author() const { return author_; }
	std::size_t year() const { return year_; }
	const std::string& timeStamp() const { return timeStamp_; }

private:
	std::string title_;
	std::string author_;
	std::size_t year_;
	std::string timeStamp_;
};

std::deque<SearchLog> gSearchLog;
std::deque<ViewLog> gViewLog;

static PyObject* loadSearchLog(PyObject* self, PyObject* args)
{
	const char* filename = nullptr;
	if (!PyArg_ParseTuple(args, "s", &filename))
		return nullptr;

	auto in = std::ifstream(filename);
	if (!in) {
		PyErr_SetString(PyExc_FileNotFoundError, "File log/search.log not found");
		return nullptr;
	}

	std::string line;
	while (std::getline(in, line)) {
		std::array<std::string, 3> log;
		std::ranges::copy( line | std::views::split('|')
			| std::views::transform( [](auto&& sv) { return std::string(sv.begin(), sv.end()); } ),
			log.begin()
		);

		gSearchLog.emplace_back(log[1], log[2], log[0]);
	}

	Py_RETURN_NONE;
}

static PyObject* saveSearchLog(PyObject* self, PyObject* args)
{
	const char* filename = nullptr;
	if (!PyArg_ParseTuple(args, "s", &filename))
		return nullptr;

	auto out = std::ofstream(filename);

	std::string line;
	for (const auto& log : gSearchLog) {
		line = log.timeStamp() + "|" + log.keyword() + "|" + log.type() + "\n";
		out << line;
	}

	Py_RETURN_NONE;
}

static PyObject* loadViewLog(PyObject* self, PyObject* args)
{
	const char* filename = nullptr;
	if (!PyArg_ParseTuple(args, "s", &filename))
		return nullptr;

	auto in = std::ifstream(filename);
	if (!in) {
		PyErr_SetString(PyExc_FileNotFoundError, "File log/view.log not found");
		return nullptr;
	}

	std::string line;
	while (std::getline(in, line)) {
		std::array<std::string, 4> log;
		std::ranges::copy(line | std::views::split('|')
			| std::views::transform([](auto&& sv) { return std::string(sv.begin(), sv.end()); }),
			log.begin()
		);

		gViewLog.emplace_back(log[1], log[2], std::stoi(log[3]), log[0]);
	}

	Py_RETURN_NONE;
}

static PyObject* saveViewLog(PyObject* self, PyObject* args)
{
	const char* filename = nullptr;
	if (!PyArg_ParseTuple(args, "s", &filename))
		return nullptr;

	auto out = std::ofstream("log/view.log");

	std::string line;
	for (const auto& log : gViewLog) {
		line = log.timeStamp() + "|" + log.title() + "|" + log.author() + "|" + std::to_string(log.year()) + "\n";
		out << line;
	}

	Py_RETURN_NONE;
}

// don't include | in keyword and type
static PyObject* logSearch(PyObject* self, PyObject* args)
{
	const char* keyword = nullptr;
	const char* type = nullptr;

	if (!PyArg_ParseTuple(args, "ss", &keyword, &type))
		return nullptr;

	try {
		gSearchLog.emplace_back(keyword, type);
	}
	catch (const std::exception& e) {
		PyErr_SetString(PyExc_ValueError, e.what());
		return nullptr;
	}

	Py_RETURN_NONE;
}

// don't include | in title and author
static PyObject* logView(PyObject* self, PyObject* args)
{
	const char* title = nullptr;
	const char* author = nullptr;
	int year;

	if (!PyArg_ParseTuple(args, "ssi", &title, &author, &year))
		return nullptr;

	gViewLog.emplace_back(title, author, year);

	Py_RETURN_NONE;
}

static PyObject* searchLogSize(PyObject* self, PyObject* args)
{
	return PyLong_FromSize_t(gSearchLog.size());
}

static PyObject* viewLogSize(PyObject* self, PyObject* args)
{
	return PyLong_FromSize_t(gViewLog.size());
}

static PyObject* getSearchLog(PyObject* self, PyObject* args)
{
	std::size_t index;
	if (!PyArg_ParseTuple(args, "n", &index)) {
		PyErr_BadArgument();
		return nullptr;
	}

	if (index >= gSearchLog.size()) {
		PyErr_SetString(PyExc_IndexError, "Index out of range");
		return nullptr;
	}

	const auto& log = gSearchLog[index];

	// make dictionary
	PyObject* dict = PyDict_New();
	PyDict_SetItemString(dict, "keyword", PyUnicode_FromString(log.keyword().c_str()));
	PyDict_SetItemString(dict, "type", PyUnicode_FromString(log.type().c_str()));
	PyDict_SetItemString(dict, "timeStamp", PyUnicode_FromString(log.timeStamp().c_str()));

	return dict;
}

static PyObject* getViewLog(PyObject* self, PyObject* args)
{
	std::size_t index;
	if (!PyArg_ParseTuple(args, "n", &index)) {
		PyErr_BadArgument();
		return nullptr;
	}

	if (index >= gViewLog.size()) {
		PyErr_SetString(PyExc_IndexError, "Index out of range");
		return nullptr;
	}

	const auto& log = gViewLog[index];

	// make dictionary
	PyObject* dict = PyDict_New();
	PyDict_SetItemString(dict, "title", PyUnicode_FromString(log.title().c_str()));
	PyDict_SetItemString(dict, "author", PyUnicode_FromString(log.author().c_str()));
	PyDict_SetItemString(dict, "year", PyLong_FromSize_t(log.year()));
	PyDict_SetItemString(dict, "timeStamp", PyUnicode_FromString(log.timeStamp().c_str()));

	return dict;
}



static PyMethodDef SpamMethods[] = {
	{ "loadSearchLog", loadSearchLog, METH_VARARGS, "Load search log" },
	{ "saveSearchLog", saveSearchLog, METH_VARARGS, "Save search log" },
	{ "loadViewLog", loadViewLog, METH_VARARGS, "Load view log" },
	{ "saveViewLog", saveViewLog, METH_VARARGS, "Save view log" },
	{ "logSearch", logSearch, METH_VARARGS, "Log search" },
	{ "logView", logView, METH_VARARGS, "Log view" },
	{ "searchLogSize", searchLogSize, METH_NOARGS, "Get search log size" },
	{ "viewLogSize", viewLogSize, METH_NOARGS, "Get view log size" },
	{ "getSearchLog", getSearchLog, METH_VARARGS, "Get search log" },
	{ "getViewLog", getViewLog, METH_VARARGS, "Get view log" },
	{ NULL, NULL, 0, NULL } // 배열의 끝을 나타냅니다.
};

static struct PyModuleDef spammodule = {
	PyModuleDef_HEAD_INIT,
	"spam",
	"It is logging module.",
	-1,
	SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
	return PyModule_Create(&spammodule);
}
