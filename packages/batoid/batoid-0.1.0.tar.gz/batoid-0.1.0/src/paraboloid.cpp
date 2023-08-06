#include "paraboloid.h"
#include "utils.h"
#include <cmath>

namespace batoid {

    Paraboloid::Paraboloid(double R) : _R(R), _Rinv(1./R), _2Rinv(1./2/R) {}

    double Paraboloid::sag(double x, double y) const {
        if (_R != 0) {
            double r2 = x*x + y*y;
            return r2*_2Rinv;
        }
        return 0.0;
    }

    Vector3d Paraboloid::normal(double x, double y) const {
        if (_R == 0)
            return Vector3d(0,0,1);
        return Vector3d(-x*_Rinv, -y*_Rinv, 1).normalized();
    }

    bool Paraboloid::timeToIntersect(const Ray& r, double& t) const {
        double a = (r.v[0]*r.v[0] + r.v[1]*r.v[1])*_2Rinv;
        double b = (r.r[0]*r.v[0] + r.r[1]*r.v[1])*_Rinv - r.v[2];
        double c = (r.r[0]*r.r[0] + r.r[1]*r.r[1])*_2Rinv - r.r[2];
        double r1, r2;
        int n = solveQuadratic(a, b, c, r1, r2);

        if (n == 0)
            return false;
        else if (n == 1) {
            if (r1 < 0)
                return false;
            t = r1;
        } else {
            if (r1 < 0) {
                if (r2 < 0)
                    return false;
                else
                    t = r2;
            } else
                t = std::min(r1, r2);
        }
        t += r.t;
        return true;
    }
}
