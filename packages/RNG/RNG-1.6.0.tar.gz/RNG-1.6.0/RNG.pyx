#!python3
#distutils: language = c++


__all__ = (
    "bernoulli_variate", "uniform_int_variate", "generate_canonical", "uniform_real_variate",
    "binomial_variate", "negative_binomial_variate", "geometric_variate", "poisson_variate",
    "normal_variate", "lognormal_variate", "exponential_variate", "gamma_variate", "weibull_variate",
    "extreme_value_variate", "chi_squared_variate", "cauchy_variate", "fisher_f_variate", "student_t_variate",
)


cdef extern from "RNG.hpp":
    int         rng_bernoulli       "RNG::bernoulli_variate"(double)
    long long   rng_uniform_int     "RNG::uniform_int_variate"(long long, long long)
    long long   rng_binomial        "RNG::binomial_variate"(long long, double)
    long long   rng_neg_binomial    "RNG::negative_binomial_variate"(long long, double)
    long long   rng_geometric       "RNG::geometric_variate"(double)
    long long   rng_poisson         "RNG::poisson_variate"(double)
    double      rng_canonical       "RNG::canonical_variate"()
    double      rng_uniform_real    "RNG::uniform_real_variate"(double, double)
    double      rng_exponential     "RNG::exponential_variate"(double)
    double      rng_gamma           "RNG::gamma_variate"(double, double)
    double      rng_weibull         "RNG::weibull_variate"(double, double)
    double      rng_normal          "RNG::normal_variate"(double, double)
    double      rng_lognormal       "RNG::lognormal_variate"(double, double)
    double      rng_extreme_value   "RNG::extreme_value_variate"(double, double)
    double      rng_chi_squared     "RNG::chi_squared_variate"(double)
    double      rng_cauchy          "RNG::cauchy_variate"(double, double)
    double      rng_fisher_f        "RNG::fisher_f_variate"(double, double)
    double      rng_student_t       "RNG::student_t_variate"(double)


def bernoulli_variate(ratio_of_truth) -> bool:
    return rng_bernoulli(ratio_of_truth) == 1

def uniform_int_variate(left_limit, right_limit) -> int:
    return rng_uniform_int(left_limit, right_limit)

def binomial_variate(number_of_trials, probability) -> int:
    return rng_binomial(number_of_trials, probability)

def negative_binomial_variate(number_of_trials, probability) -> int:
    return rng_neg_binomial(number_of_trials, probability)

def geometric_variate(probability) -> int:
    return rng_geometric(probability)

def poisson_variate(mean) -> int:
    return rng_poisson(mean)

def generate_canonical():
    return rng_canonical()

def uniform_real_variate(left_limit, right_limit) -> float:
    return rng_uniform_real(left_limit, right_limit)
    
def exponential_variate(lambda_rate) -> float:
    return rng_exponential(lambda_rate)

def gamma_variate(shape, scale) -> float:
    return rng_gamma(shape, scale)
    
def weibull_variate(shape, scale) -> float:
    return rng_weibull(shape, scale)
    
def normal_variate(mean, std_dev) -> float:
    return rng_normal(mean, std_dev)

def lognormal_variate(log_mean, log_deviation) -> float:
    return rng_lognormal(log_mean, log_deviation)
    
def extreme_value_variate(location, scale) -> float:
    return rng_extreme_value(location, scale)

def chi_squared_variate(degrees_of_freedom) -> float:
    return rng_chi_squared(degrees_of_freedom)
    
def cauchy_variate(location, scale) -> float:
    return rng_cauchy(location, scale)
    
def fisher_f_variate(degrees_of_freedom_1, degrees_of_freedom_2) -> float:
    return rng_fisher_f(degrees_of_freedom_1, degrees_of_freedom_2)
    
def student_t_variate(degrees_of_freedom) -> float:
    return rng_student_t(degrees_of_freedom)
