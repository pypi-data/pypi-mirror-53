#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <algorithm>

#include "autocorr.h"

namespace py = pybind11;

py::tuple multitau_mt(py::array_t<double, py::array::c_style | py::array::forcecast> Signal,
                 int m) {

    unsigned nrow = 1, ntimes =0;
    if (Signal.ndim() == 1)
        ntimes = Signal.shape()[0];
    else if (Signal.ndim() == 2) {
        nrow = Signal.shape()[0];
        ntimes = Signal.shape()[1];
    }
    else
        throw std::runtime_error("Input signal must be a 1-D or a 2-D numpy array");

    /* get pointer to encapsulated data */
    double * signal = (double *) Signal.request().ptr;

    /* compute the autocorrelations */
    MultiTauAutocorrelator corr(signal, nrow, ntimes);
    corr.process((unsigned) m);

    /* get sizes of from the correlator objest */
    size_t len = corr.length();
    std::vector<ssize_t> shape;
    shape.push_back(nrow);
    shape.push_back(len);
        
    /* allocate the buffers for result */
    auto G2  = py::array_t<double>(shape);
    auto Tau = py::array_t<double>(len);

    /* get data-pointers */
    double * g2 = (double *) G2.request().ptr;
    double * tau = (double *) Tau.request().ptr;

    /* copy data */
    std::memcpy(g2, corr.g2(), sizeof(double) * len * nrow);
    std::memcpy(tau, corr.tau(), sizeof(double) * len);

    py::tuple result(2);
    result[0] = G2;
    result[1] = Tau;
    return result;
}


py::tuple fftautocorr(py::array_t<double, py::array::c_style | py::array::forcecast> Signal) {
    int nrow = 1, ntimes =0;
    if (Signal.ndim() == 1)
        ntimes = Signal.shape()[0];
    else if (Signal.ndim() == 2) {
        nrow = Signal.shape()[0];
        ntimes = Signal.shape()[1];
    }
    else
        throw std::runtime_error("Input signal must be a 1-D or a 2-D numpy array");

    /* get pointer to encapsulated data */
    double * signal = (double *) Signal.request().ptr;

    /* create return array */
    std::vector<ssize_t> shape;
    shape.push_back(nrow);
    shape.push_back(ntimes);
    auto G2 = py::array_t<double>(shape);
    auto Tau = py::array_t<double>(ntimes);

    /* get data-pointers */
    double * g2 = (double *) G2.request().ptr;
    double * tau = (double *) Tau.request().ptr;

    /* FFT method calculates for all taus */
    for (int i = 0; i < ntimes; i++) tau[i] = (double) i;

    /* calculate g2's */
    FFTAutocorr(signal, g2, ntimes, nrow);

    py::tuple result(2);
    result[0] = G2;
    result[1] = Tau;
    return result;
}

PYBIND11_MODULE (cAutocorr, m) {
    m.def("multitau_mt", &multitau_mt, "Same algorithm as python, except uses multiple cores");
    m.def("fftautocorr", &fftautocorr, "Compute autocorrelation using FFT");
}
