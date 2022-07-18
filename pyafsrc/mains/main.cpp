/*#include <iostream>
#include <armadillo>

using namespace std;
using namespace arma;

int main()
  {
    cx_mat P(2, 8, fill::zeros);
  	cx_mat W(2, 1, fill::zeros);

    mat A = mat({1.0/sqrt(2),1.0/sqrt(2)}).t();
    mat B = mat({0.0,0.0}).t();

    W.set_real(A);
  	W.set_imag(B);

  	for (int i = 0; i < 2 ;  i++)
    {
      for (int j = 0; j < 6 ;  j++)
      {
        P(i,j) = cx_double(0.7, -0.7);
      }
    }
    cout <<  P  << endl;
    cout <<  shift(P,-ceil(P.n_cols/2),1) << endl;


  return 0;
}*/
