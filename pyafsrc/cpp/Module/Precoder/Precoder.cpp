/*!
 * \file
 * \brief Filters a signal.
 *
 * \section LICENSE
 * This file is under MIT license (https://opensource.org/licenses/MIT).
 */

#include <cstring>
#include <memory>
#include <stdexcept>
#include <cmath>
#include <sstream>

#include "Tools/Exception/exception.hpp"

#include "Module/Precoder/Precoder.hpp"

namespace aff3ct
{
namespace module
{

Precoder::
Precoder(const int Nb, const int Nl, const int Na, const int TPMI, const int val)
: Module(), Nb(Nb), Nl(Nl), Na(Na), TPMI(TPMI), val(val)
{
	const std::string name = "Precoder2";
	this->set_name(name);
	this->set_short_name(name);
	this->set_single_wave(true);

	this->W.zeros(this->Na, this->Nl);
	this->_precoding_matrix();

	auto &p1 = this->create_task("precode");
	auto p1s_X_N1 = this->template create_socket_in <float>(p1, "U_K1", this->Nb);
	auto p1s_Y_N2 = this->template create_socket_out<float>(p1, "U_K2", this->Nb/this->Nl * this->Na);
	this->create_codelet(p1, [p1s_X_N1, p1s_Y_N2](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Precoder&>(m)._precode(static_cast<float*>(t[p1s_X_N1].get_dataptr()),
		                                           static_cast<float*>(t[p1s_Y_N2].get_dataptr()),
										frame_id);

		return 0;
	});


	auto &p2 = this->create_task("decode");
	auto p2s_X_N1 = this->template create_socket_in <float>(p2, "V_K1", this->Nb/this->Nl * this->Na);
	auto p2s_Y_N2 = this->template create_socket_out<float>(p2, "V_K2", this->Nb);
	this->create_codelet(p2, [p2s_X_N1, p2s_Y_N2](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Precoder&>(m)._decode(static_cast<float*>(t[p2s_X_N1].get_dataptr()),
																							 static_cast<float*>(t[p2s_Y_N2].get_dataptr()),
										frame_id);

		return 0;
	});
}

void Precoder::
_precode(const float *U_K1, float *U_K2, const int frame_id)
{
	cx_fmat P(this->Nl, this->Nb/(2*this->Nl), fill::zeros);
	cx_fmat A(this->Na, this->Nb/(2*this->Nl), fill::zeros);

	for (int i = 0; i < this->Nl ;  i++)
  {
    for (int j = 0; j < this->Nb/(2*this->Nl) ;  j++)
    {
      P(i,j) = cx_float(U_K1[2*(i*this->Nb/(2*this->Nl)+j)], U_K1[2*(i*this->Nb/(2*this->Nl)+j)+1]);
    }
  }
	//std::cout <<  this->W*P  << std::endl;


}

void Precoder::
_decode(const float *V_K1, float *V_K2, const int frame_id)
{

}

void Precoder::
_precoding_matrix()
{
	fmat A(this->Na, this->Nl, fill::zeros);
	fmat B(this->Na, this->Nl, fill::zeros);
  switch (this->Nl)
  {
    case 1:
    switch (this->Na)
    {
      case 2:
      switch (this->TPMI)
      {
        case 0:
			  A = fmat({1.0/sqrt(2),0.0}).t();
				B = fmat({0.0,0.0}).t();
        break;
        case 1:
				A = fmat({0.0,1.0/sqrt(2)}).t();
				B = fmat({0.0,0.0}).t();
        break;
        case 2:
				A = fmat({1.0/sqrt(2),1.0/sqrt(2)}).t();
				B = fmat({0.0,0.0}).t();
        break;
        case 3:
				A = fmat({1.0/sqrt(2),-1.0/sqrt(2)}).t();
				B = fmat({0.0,0.0}).t();
        break;
        case 4:
				A = fmat({1.0/sqrt(2),0.0}).t();
				B = fmat({0.0,1.0/sqrt(2)}).t();
        break;
        case 5:
				A = fmat({1.0/sqrt(2),0.0}).t();
				B = fmat({0.0,-1.0/sqrt(2)}).t();
        break;
      }

      break;
      case 4:
      switch(this->val)
      {
        case 0:
        switch (this->TPMI)
        {
          case 0:
          break;
          case 1:
          break;
          case 2:
          break;
          case 3:
          break;
          case 4:
          break;
          case 5:
          break;
          case 6:
          break;
          case 7:
          break;
          case 8:
          break;
          case 9:
          break;
          case 10:
          break;
        }
        break;
        case 1:
        switch (this->TPMI)
        {
          case 0:
          break;
          case 1:
          break;
          case 2:
          break;
          case 3:
          break;
          case 4:
          break;
          case 5:
          break;
          case 6:
          break;
          case 7:
          break;
          case 8:
          break;
          case 9:
          break;
          case 10:
          break;
        }
        break;
      }
      break;

    }
    break;
    case 2:
    switch (this->Na)
    {
      case 2:
      switch (this->TPMI)
      {
        case 0:
        break;
        case 1:
        break;
        case 2:
        break;
      }
      break;
      case 4:
      switch (this->TPMI)
      {
        case 0:
        break;
        case 1:
        break;
        case 2:
        break;
        case 3:
        break;
        case 4:
        break;
        case 5:
        break;
        case 6:
        break;
        case 7:
        break;
        case 8:
        break;
        case 9:
        break;
        case 10:
        break;
      }

      break;

    }
    break;
    case 3:
    switch (this->TPMI)
    {
      case 0:
      break;
      case 1:
      break;
      case 2:
      break;
      case 3:
      break;
      case 4:
      break;
      case 5:
      break;
      case 6:
      break;
    }

    break;
    case 4:
    switch (this->TPMI)
    {
      case 0:
      break;
      case 1:
      break;
      case 2:
      break;
      case 3:
      break;
      case 4:
      break;
    }

    break;
  }
	this->W.set_real(A);
	this->W.set_imag(B);

}

}
}
