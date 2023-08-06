#include "medium.h"
#include <cmath>
#include <sstream>

namespace batoid {
    std::ostream& operator<<(std::ostream& os, const Medium& m) {
        return os << m.repr();
    }


    ConstMedium::ConstMedium(double n) : _n(n) {}

    double ConstMedium::getN(double wavelength) const {
        return _n;
    }

    std::string ConstMedium::repr() const {
        std::ostringstream oss;
        oss << "ConstMedium(" << getN(0.0) << ")";
        return oss.str();
    }

    bool operator==(const ConstMedium& cm1, const ConstMedium& cm2)
        { return cm1.getN(0.0) == cm2.getN(0.0); }
    bool operator!=(const ConstMedium& cm1, const ConstMedium& cm2)
        { return cm1.getN(0.0) != cm2.getN(0.0); }



    TableMedium::TableMedium(std::shared_ptr<Table<double,double>> table) :
        _table(table) {}

    std::shared_ptr<Table<double,double>> TableMedium::getTable() const {
        return std::shared_ptr<Table<double,double>>(_table);
    }

    double TableMedium::getN(double wavelength) const {
        return (*_table)(wavelength);
    }

    std::string TableMedium::repr() const {
        std::ostringstream oss;
        oss << "TableMedium(" << *_table << ")";
        return oss.str();
    }

    bool operator==(const TableMedium& tm1, const TableMedium& tm2)
        { return *tm1.getTable() == *tm2.getTable(); }
    bool operator!=(const TableMedium& tm1, const TableMedium& tm2)
        { return *tm1.getTable() != *tm2.getTable(); }


    SellmeierMedium::SellmeierMedium(
        double B1, double B2, double B3,
        double C1, double C2, double C3) :
        _B1(B1), _B2(B2), _B3(B3), _C1(C1), _C2(C2), _C3(C3) {}

    SellmeierMedium::SellmeierMedium(std::array<double,6> arr) :
        _B1(arr[0]), _B2(arr[1]), _B3(arr[2]), _C1(arr[3]), _C2(arr[4]), _C3(arr[5]) {}

    double SellmeierMedium::getN(double wavelength) const {
        // Sellmeier coefficients assume wavelength is in microns, so we have to multiply (1e6)**2
        double x = wavelength*wavelength*1e12;
        return std::sqrt(1.0 + _B1*x/(x-_C1) + _B2*x/(x-_C2) + _B3*x/(x-_C3));
    }

    std::array<double,6> SellmeierMedium::getCoefs() const {
        return std::array<double,6>{{_B1, _B2, _B3, _C1, _C2, _C3}};
    }

    std::string SellmeierMedium::repr() const {
        std::ostringstream oss;
        oss << "SellmeierMedium("
            << _B1 << ", "
            << _B2 << ", "
            << _B3 << ", "
            << _C1 << ", "
            << _C2 << ", "
            << _C3 << ")";
        return oss.str();
    }

    bool operator==(const SellmeierMedium& sm1, const SellmeierMedium& sm2)
        { return sm1.getCoefs() == sm2.getCoefs(); }
    bool operator!=(const SellmeierMedium& sm1, const SellmeierMedium& sm2)
        { return sm1.getCoefs() != sm2.getCoefs(); }


    SumitaMedium::SumitaMedium(
        double A0, double A1, double A2,
        double A3, double A4, double A5) :
        _A0(A0), _A1(A1), _A2(A2), _A3(A3), _A4(A4), _A5(A5) {}

    SumitaMedium::SumitaMedium(std::array<double,6> arr) :
        _A0(arr[0]), _A1(arr[1]), _A2(arr[2]), _A3(arr[3]), _A4(arr[4]), _A5(arr[5]) {}

    double SumitaMedium::getN(double wavelength) const {
        //Sumita coefficients assume wavelength is in microns, so we have to multiply (1e6)**2
        double x = wavelength*wavelength*1e12;
        double y = 1./x;
        return std::sqrt(_A0 + _A1*x + y*(_A2 + y*(_A3 + y*(_A4 + y*_A5))));
    }

    std::array<double,6> SumitaMedium::getCoefs() const {
        return std::array<double,6>{{_A0, _A1, _A2, _A3, _A4, _A5}};
    }

    std::string SumitaMedium::repr() const {
        std::ostringstream oss;
        oss << "SumitaMedium("
            << _A0 << ", "
            << _A1 << ", "
            << _A2 << ", "
            << _A3 << ", "
            << _A4 << ", "
            << _A5 << ")";
        return oss.str();
    }

    bool operator==(const SumitaMedium& sm1, const SumitaMedium& sm2)
        { return sm1.getCoefs() == sm2.getCoefs(); }
    bool operator!=(const SumitaMedium& sm1, const SumitaMedium& sm2)
        { return sm1.getCoefs() != sm2.getCoefs(); }

    // Uses the formulae given in Filippenko (1982), which appear to come from Edlen (1953),
    // and Coleman, Bozman, and Meggers (1960).  The units of the original formula are non-SI,
    // being mmHg for pressure (and water vapor pressure), and degrees C for temperature.  This
    // class accepts SI units, however, and transforms them when plugging into the formula.
    //
    // The default values for temperature, pressure and water vapor pressure are expected to be
    // appropriate for LSST at Cerro Pachon, Chile, but they are broadly reasonable for most
    // observatories.
    //
    // @param pressure       Air pressure in kiloPascals.
    // @param temperature    Temperature in Kelvins.
    // @param H2O_pressure   Water vapor pressure in kiloPascals.
    Air::Air(double pressure, double temperature, double h2o_pressure) :
        _pressure(pressure), _temperature(temperature), _h2o_pressure(h2o_pressure),
        _P(pressure * 7.50061683), _T(temperature - 273.15), _W(h2o_pressure * 7.50061683) {}

    double Air::getN(double wavelength) const {
        // inverse wavenumber squared in micron^-2
        double sigma_squared = 1e-12 / (wavelength*wavelength);
        double n_minus_one = (64.328 + (29498.1 / (146.0 - sigma_squared))
                              + (255.4 / (41.0 - sigma_squared))) * 1.e-6;
        n_minus_one *= _P * (1.0 + (1.049 - 0.0157 * _T) * 1.e-6 * _P) / (720.883 * (1.0 + 0.003661 * _T));
        n_minus_one -= (0.0624 - 0.000680 * sigma_squared)/(1.0 + 0.003661 * _T) * _W * 1.e-6;
        return 1+n_minus_one;
    }

    std::string Air::repr() const {
        std::ostringstream oss;
        oss << "Air("
            << getPressure() << ", "
            << getTemperature() << ", "
            << getH2OPressure() << ")";
        return oss.str();
    }

    bool operator==(const Air& a1, const Air& a2)
        { return a1.getPressure() == a2.getPressure() &&
                 a1.getTemperature() == a2.getTemperature() &&
                 a1.getH2OPressure() == a2.getH2OPressure(); }
    bool operator!=(const Air& a1, const Air& a2)
        { return a1.getPressure() != a2.getPressure() ||
                 a1.getTemperature() != a2.getTemperature() ||
                 a1.getH2OPressure() != a2.getH2OPressure(); }

}
