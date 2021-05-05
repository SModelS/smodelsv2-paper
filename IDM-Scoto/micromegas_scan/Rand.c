/* -------------------------------------------------------------------------- 
 * This is an ANSI C library for generating random variates from six discrete 
 * distributions
 *
 *      Generator         Range (x)     Mean         Variance
 *
 *      Bernoulli(p)      x = 0,1       p            p*(1-p)
 *      Binomial(n, p)    x = 0,...,n   n*p          n*p*(1-p)
 *      Equilikely(a, b)  x = a,...,b   (a+b)/2      ((b-a+1)*(b-a+1)-1)/12
 *      Geometric(p)      x = 0,...     p/(1-p)      p/((1-p)*(1-p))
 *      Pascal(n, p)      x = 0,...     n*p/(1-p)    n*p/((1-p)*(1-p))
 *      Poisson(m)        x = 0,...     m            m
 * 
 * and seven continuous distributions
 *
 *      Uniform(a, b)     a < x < b     (a + b)/2    (b - a)*(b - a)/12 
 *      Exponential(m)    x > 0         m            m*m
 *      Erlang(n, b)      x > 0         n*b          n*b*b
 *      Normal(m, s)      all x         m            s*s
 *      Lognormal(a, b)   x > 0            see below
 *      Chisquare(n)      x > 0         n            2*n 
 *      Student(n)        all x         0  (n > 1)   n/(n - 2)   (n > 2)
 *
 * For the a Lognormal(a, b) random variable, the mean and variance are
 *
 *                        mean = exp(a + 0.5*b*b)
 *                    variance = (exp(b*b) - 1) * exp(2*a + b*b)
 *
 * Name              : rvgs.c  (Random Variate GeneratorS)
 * Author            : Steve Park & Dave Geyer
 * Language          : ANSI C
 * Latest Revision   : 10-28-98
 * --------------------------------------------------------------------------
 */

#include <math.h>
#include <time.h>

/* ------------------------------------------------------------- 
 * Name            : rvgs.h (header file for the library rvgs.c)
 * Author          : Steve Park & Dave Geyer
 * Language        : ANSI C
 * Latest Revision : 11-03-96
 * -------------------------------------------------------------- 
 */

#if !defined( _RVGS_ )
#define _RVGS_

long Bernoulli(double p);
long Binomial(long n, double p);
long Equilikely(long a, long b);
long Geometric(double p);
long Pascal(long n, double p);
long Poisson(double m);

double Uniform(double a, double b);
double Exponential(double m);
double Erlang(long n, double b);
double Normal(double m, double s);
double Lognormal(double a, double b);
double Chisquare(long n);
double Student(long n);
double SelfRepel(double m,double a);

#endif


/* ----------------------------------------------------------------------- 
 * Name            : rngs.h  (header file for the library file rngs.c) 
 * Author          : Steve Park & Dave Geyer
 * Language        : ANSI C
 * Latest Revision : 09-22-98
 * ----------------------------------------------------------------------- 
 */

#if !defined( _RNGS_ )
#define _RNGS_

double Random(void);
void   PlantSeeds(long x);
void   GetSeed(long *x);
void   PutSeed(long x);
void   SelectStream(int index);
void   TestRandom(void);

#endif

#define MODULUS    2147483647 /* DON'T CHANGE THIS VALUE                  */
#define MULTIPLIER 48271      /* DON'T CHANGE THIS VALUE                  */
#define CHECK      399268537  /* DON'T CHANGE THIS VALUE                  */
#define STREAMS    256        /* # of streams, DON'T CHANGE THIS VALUE    */
#define A256       22925      /* jump multiplier, DON'T CHANGE THIS VALUE */
#define DEFAULT    123456789  /* initial seed, use 0 < DEFAULT < MODULUS  */
      
//static long seed[STREAMS] = {DEFAULT};  /* current state of each stream   */
static long seed[STREAMS] = 
{180771391, 362695771, 10809521, 2019160643, 1976618437, 43554761, 717226259, 
 630680989, 452214853, 1237348921, 1973168723, 1455316061, 322330909, 
 1964903839, 410398907, 487545691, 1560908527, 360226067, 987283411, 
 1021858091, 87137153, 600656933, 529242377, 1113301697, 1407466537, 
 526091743, 1164853429, 1606533811, 813155341, 1534698857, 405735691, 
 2034122059, 1291528367, 1770571529, 1834989641, 866823691, 1687351151, 
 289222393, 655716043, 2008478063, 694783861, 359778323, 1631173517, 
 619534807, 707262191, 2031062329, 497237599, 946186013, 656724097, 
 1028915887, 61789367, 485236487, 1360774931, 39886169, 1697614099, 
 1766924773, 934731209, 1173472367, 1202685307, 318186137, 806737439, 
 1973118557, 181056221, 783907457, 211846559, 34687087, 1932483907, 
 1062992011, 214734953, 348325001, 418697269, 1279562659, 655596961, 
 1172777533, 791477317, 160219151, 315904357, 271839739, 105187909, 
 689725643, 587113739, 691563289, 1575933449, 1431295553, 109116941, 
 1187387053, 543421741, 720931807, 1296668029, 1782447853, 229970843, 
 798146771, 307651181, 1580971757, 519287599, 645136333, 799854619, 
 236437277, 1424706527, 186983267, 608369869, 244216439, 80937287, 609710987, 
 152858561, 916088759, 1801861111, 1575814579, 487065529, 1427536127, 
 1440216403, 556444781, 1744880773, 822375607, 398972087, 1683840947, 
 1803830909, 856490819, 462554927, 1106564999, 406215113, 894329543, 
 1014471037, 1814827187, 1602741071, 305006413, 409838699, 1452816749, 
 1278208951, 573932917, 576020903, 980562409, 463463153, 978456407, 
 1098825019, 1803623179, 1185796267, 340408037, 44058877, 1974376597, 
 947945329, 1624749173, 339845747, 1850499137, 782476693, 4785059, 633970201, 
 525212647, 1246408573, 1571042933, 107166307, 353955461, 543167159, 
 1209536299, 18446413, 451312373, 110287033, 1345650329, 1805940989, 
 1914692581, 993240197, 1923137063, 1458805813, 232637411, 1399746871, 
 831395111, 704257859, 75235189, 1396351207, 2013585157, 97890491, 
 1974760141, 1251809239, 1961439913, 430981049, 515717303, 304500293, 
 973859863, 921064393, 821984447, 677586311, 631543673, 1207278581, 73402943, 
 204700187, 372217861, 958103753, 548723453, 1523914631, 870353707, 
 244149089, 944290031, 864778249, 511810903, 1100714051, 16556933, 
 1529425379, 1446603043, 194591011, 26750663, 480184429, 1750083191, 
 1378014023, 313270829, 908679641, 245321053, 1921506817, 1908358087, 
 1459090463, 1450429553, 570665947, 337320073, 477733171, 1757005343, 
 1243921493, 859958509, 265266217, 498645317, 1260919679, 99163681, 
 135521081, 1050864679, 762486889, 583751419, 86188853, 1857294371, 
 2013943523, 1537627603, 100058261, 153901259, 759458789, 913196059, 
 1796150767, 717501319, 819556711, 749627741, 1168579637, 1697092699, 
 136035821, 467746649, 1115968499, 305183237, 2730011, 355522627, 647551249, 
 1137761957, 1424811043, 1312601119, 49806959, 1214441387, 293886371, 
 1715159987, 1067165501, 947554079, 109438447, 2011191569};
static int  stream        = 0;          /* stream index, 0 is the default */


   double Random(void)
/* ----------------------------------------------------------------
 * Random returns a pseudo-random real number uniformly distributed 
 * between 0.0 and 1.0. 
 * ----------------------------------------------------------------
 */
{
  const long Q = MODULUS / MULTIPLIER;
  const long R = MODULUS % MULTIPLIER;
        long t;

  t = MULTIPLIER * (seed[stream] % Q) - R * (seed[stream] / Q);
  if (t > 0) 
    seed[stream] = t;
  else 
    seed[stream] = t + MODULUS;
  return ((double) seed[stream] / MODULUS);
}

   long Bernoulli(double p)
/* ========================================================
 * Returns 1 with probability p or 0 with probability 1 - p. 
 * NOTE: use 0.0 < p < 1.0                                   
 * ========================================================
 */ 
{
  return ((Random() < (1.0 - p)) ? 0 : 1);
}

   long Binomial(long n, double p)
/* ================================================================ 
 * Returns a binomial distributed integer between 0 and n inclusive. 
 * NOTE: use n > 0 and 0.0 < p < 1.0
 * ================================================================
 */
{ 
  long i, x = 0;

  for (i = 0; i < n; i++)
    x += Bernoulli(p);
  return (x);
}

   long Equilikely(long a, long b)
/* ===================================================================
 * Returns an equilikely distributed integer between a and b inclusive. 
 * NOTE: use a < b
 * ===================================================================
 */
{
  return (a + (long) ((b - a + 1) * Random()));
}

   long Geometric(double p)
/* ====================================================
 * Returns a geometric distributed non-negative integer.
 * NOTE: use 0.0 < p < 1.0
 * ====================================================
 */
{
  return ((long) (log(1.0 - Random()) / log(p)));
}

   long Pascal(long n, double p)
/* ================================================= 
 * Returns a Pascal distributed non-negative integer. 
 * NOTE: use n > 0 and 0.0 < p < 1.0
 * =================================================
 */
{ 
  long i, x = 0;

  for (i = 0; i < n; i++)
    x += Geometric(p);
  return (x);
}

   long Poisson(double m)
/* ================================================== 
 * Returns a Poisson distributed non-negative integer. 
 * NOTE: use m > 0
 * ==================================================
 */
{ 
  double t = 0.0;
  long   x = 0;

  while (t < m) {
    t += Exponential(1.0);
    x++;
  }
  return (x - 1);
}

   double Uniform(double a, double b)
/* =========================================================== 
 * Returns a uniformly distributed real number between a and b. 
 * NOTE: use a < b
 * ===========================================================
 */
{ 
  return (a + (b - a) * Random());
}

   double Exponential(double m)
/* =========================================================
 * Returns an exponentially distributed positive real number. 
 * NOTE: use m > 0.0
 * =========================================================
 */
{
  return (-m * log(1.0 - Random()));
}

   double Erlang(long n, double b)
/* ================================================== 
 * Returns an Erlang distributed positive real number.
 * NOTE: use n > 0 and b > 0.0
 * ==================================================
 */
{ 
  long   i;
  double x = 0.0;

  for (i = 0; i < n; i++) 
    x += Exponential(b);
  return (x);
}

   double Normal(double m, double s)
/* ========================================================================
 * Returns a normal (Gaussian) distributed real number.
 * NOTE: use s > 0.0
 *
 * Uses a very accurate approximation of the normal idf due to Odeh & Evans, 
 * J. Applied Statistics, 1974, vol 23, pp 96-97.
 * ========================================================================
 */
{ 
  const double p0 = 0.322232431088;     const double q0 = 0.099348462606;
  const double p1 = 1.0;                const double q1 = 0.588581570495;
  const double p2 = 0.342242088547;     const double q2 = 0.531103462366;
  const double p3 = 0.204231210245e-1;  const double q3 = 0.103537752850;
  const double p4 = 0.453642210148e-4;  const double q4 = 0.385607006340e-2;
  double u, t, p, q, z;

  u   = Random();
  if (u < 0.5)
    t = sqrt(-2.0 * log(u));
  else
    t = sqrt(-2.0 * log(1.0 - u));
  p   = p0 + t * (p1 + t * (p2 + t * (p3 + t * p4)));
  q   = q0 + t * (q1 + t * (q2 + t * (q3 + t * q4)));
  if (u < 0.5)
    z = (p / q) - t;
  else
    z = t - (p / q);
  return (m + s * z);
}

   double Lognormal(double a, double b)
/* ==================================================== 
 * Returns a lognormal distributed positive real number. 
 * NOTE: use b > 0.0
 * ====================================================
 */
{
  return (exp(a + b * Normal(0.0, 1.0)));
}

   double Chisquare(long n)
/* =====================================================
 * Returns a chi-square distributed positive real number. 
 * NOTE: use n > 0
 * =====================================================
 */
{ 
  long   i;
  double z, x = 0.0;

  for (i = 0; i < n; i++) {
    z  = Normal(0.0, 1.0);
    x += z * z;
  }
  return (x);
}

   double Student(long n)
/* =========================================== 
 * Returns a student-t distributed real number.
 * NOTE: use n > 0
 * ===========================================
 */
{
  return (Normal(0.0, 1.0) / sqrt(Chisquare(n) / n));
}

   double SelfRepel(double m,double a)
/* ==================================================
 * Retruns a random number away from m with mean = m
 * and most probable distance being 1.34*a
 * ==================================================
 */
{
  double r,x;
	r=Random();
	if(r > 0.50){ x = m + sqrt(-2.0*a*a*log(1/r-1)); }
	else        { x = m - sqrt( 2.0*a*a*log(1/r-1)); }
  return (x);
}


