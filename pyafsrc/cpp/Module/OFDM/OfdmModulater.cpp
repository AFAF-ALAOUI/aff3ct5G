#include <cstring>
#include <memory>
#include <stdexcept>
#include <cmath>
#include <sstream>
#include <vector>
#include <armadillo>

#include "Tools/Exception/exception.hpp"

#include "Module/OFDM/OfdmModulater.hpp"

using namespace arma;

namespace aff3ct
{
namespace module
{

OfdmModulater::
OfdmModulater(const int Mgrid, const int Na, const int Nr, const int Msc, const int Nifft, const int k0)
: Module(), Mgrid(Mgrid), Na(Na), Nr(Nr), Msc(Msc), Nifft(Nifft), k0(k0)
{

  const std::string name = "OFDM2";
	this->set_name(name);
	this->set_short_name(name);
	this->set_single_wave(true);


  auto &p1 = this->create_task("modulate");
  auto p1s_U_K = this->template create_socket_in <float>(p1, "X_N", 2* this->Mgrid * this->Na);
  auto p1s_V_K = this->template create_socket_out<float>(p1, "Y_N", 2* this->Nifft *this->Mgrid * this->Na /this->Msc );
  this->create_codelet(p1, [p1s_U_K, p1s_V_K](Module &m, Task &t, const size_t frame_id) -> int
  {
    static_cast<OfdmModulater&>(m)._modulate(static_cast<float*>(t[p1s_U_K].get_dataptr()),
                                          static_cast<float*>(t[p1s_V_K].get_dataptr()),
                                          frame_id);

    return 0;
  });

  auto &p2 = this->create_task("demodulate");
  auto p2s_U_K = this->template create_socket_in <float>(p2, "Y_N", 2* this->Nifft *this->Mgrid * this->Nr /this->Msc  );
  auto p2s_V_K = this->template create_socket_out<float>(p2, "X_N", 2* this->Mgrid * this->Nr );
  this->create_codelet(p2, [p2s_U_K, p2s_V_K](Module &m, Task &t, const size_t frame_id) -> int
  {
    static_cast<OfdmModulater&>(m)._demodulate(static_cast<float*>(t[p2s_U_K].get_dataptr()),
                                          static_cast<float*>(t[p2s_V_K].get_dataptr()),
                                          frame_id);

    return 0;
  });


}

void OfdmModulater::
_modulate(const float *X_N, float *Y_N, const int frame_id)
{
  cx_fmat I(this->Mgrid*this->Na / this->Msc,this->Nifft, fill::zeros);

  for (int i = 0; i < this->Mgrid*this->Na / this->Msc ;  i++)
  {
    for (int j =(this->Nifft-this->Msc)/2 + this->k0; j<this->Nifft-((this->Nifft-this->Msc)/2-this->k0); j++)
    {
      I(i,j) = cx_float(X_N[2*(i*this->Msc+j-(this->Nifft-this->Msc)/2 -this->k0)],X_N[2*(i*this->Msc+j-(this->Nifft-this->Msc)/2 -this->k0)+1]);
    }
  }

  I = ifft(shift(I, this->Nifft/2,1).st(),this->Nifft).st();

  for (int i = 0; i < this->Mgrid * this->Na /this->Msc ;  i++)
  {
    for (int j = 0; j < this->Nifft ;  j++)
    {
      Y_N[2*(i*this->Nifft+j)] = I(i,j).real();
      Y_N[2*(i*this->Nifft+j)+1] = I(i,j).imag();

    }
  }



}

void OfdmModulater::
_demodulate(const float *Y_N, float *X_N, const int frame_id)
{

  cx_fmat I(this->Mgrid*this->Nr / this->Msc,this->Nifft, fill::zeros);

  for (int i = 0; i < this->Mgrid*this->Nr / this->Msc ;  i++)
  {
    for (int j =0; j<this->Nifft; j++)
    {
      I(i,j) = cx_float(Y_N[2*(i*this->Nifft+j)],Y_N[2*(i*this->Nifft+j)+1]);
    }
  }

  I = shift(fft(I.st(), this->Nifft).st(),this->Nifft/2,1);

  for (int i = 0; i < this->Mgrid*this->Nr /this->Msc ;  i++)
  {
    for (int j = (this->Nifft-this->Msc)/2 + this->k0; j < this->Nifft-((this->Nifft-this->Msc)/2-this->k0) ;  j++)
    {
      X_N[2*(i*this->Msc+j-(this->Nifft-this->Msc)/2 - this->k0)] = I(i,j).real();
      X_N[2*(i*this->Msc+j-(this->Nifft-this->Msc)/2 - this->k0)+1] = I(i,j).imag();
    }
  }

}



}
}
