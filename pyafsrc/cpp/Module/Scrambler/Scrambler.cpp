/*!
 * \file
 * \brief Filters a signal.
 *
 * \section LICENSE
 * This file is under MIT license (https://opensource.org/licenses/MIT).
 */

#include <string>
#include <memory>
#include <stdexcept>
#include <cmath>
#include <sstream>

#include "Tools/Exception/exception.hpp"

#include "Module/Scrambler/Scrambler.hpp"

namespace aff3ct
{
namespace module
{

Scrambler::
Scrambler(const int G, const int C_init)
: Module(), G(G), C_init(C_init)
{
	const std::string name = "Scrambler2";
	this->set_name(name);
	this->set_short_name(name);
	this->set_single_wave(true);

  this->SEQ = (int*)calloc(this->G, sizeof(int));
  this->_Goldseq31(this->G, this->C_init, this->SEQ);

	auto &p1 = this->create_task("scramble");
	auto p1s_X_N1 = this->template create_socket_in <int>(p1, "S_K1", this->G);
	auto p1s_Y_N2 = this->template create_socket_out<int>(p1, "S_K2", this->G);
	this->create_codelet(p1, [p1s_X_N1, p1s_Y_N2](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Scrambler&>(m)._scramble(static_cast<int*>(t[p1s_X_N1].get_dataptr()),
		                                           static_cast<int*>(t[p1s_Y_N2].get_dataptr()),
										frame_id);

		return 0;
	});

  auto &p2 = this->create_task("descramble");
	auto p2s_X_N1 = this->template create_socket_in <int>(p2, "S_K2", this->G);
	auto p2s_Y_N2 = this->template create_socket_out<int>(p2, "S_K1", this->G);
	this->create_codelet(p2, [p2s_X_N1, p2s_Y_N2](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Scrambler&>(m)._scramble(static_cast<int*>(t[p2s_X_N1].get_dataptr()),
		                                           static_cast<int*>(t[p2s_Y_N2].get_dataptr()),
										frame_id);

		return 0;
	});

	auto &p3 = this->create_task("descrambleLLR");
	auto p3s_X_N1 = this->template create_socket_in <float>(p3, "S_K2", this->G);
	auto p3s_Y_N2 = this->template create_socket_out<float>(p3, "S_K1", this->G);
	this->create_codelet(p3, [p3s_X_N1, p3s_Y_N2](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Scrambler&>(m)._descrambleLLR(static_cast<float*>(t[p3s_X_N1].get_dataptr()),
																							 static_cast<float*>(t[p3s_Y_N2].get_dataptr()),
										frame_id);

		return 0;
	});
}

void Scrambler::
_scramble(const int *S_K1, int *S_K2, const int frame_id)
{
  for (int i = 0; i < this->G ;  i++)
  {
    S_K2[i] = (S_K1[i]+this->SEQ[i])%2;
  }

}

void Scrambler::
_descrambleLLR(const float *S_K2, float *S_K1, const int frame_id)
{
  for (int i = 0; i < this->G ;  i++)
  {
    S_K1[i]= S_K2[i]*(1 - 2*this->SEQ[i]);
  }
}

void Scrambler::
_Goldseq31(const int N, int C_init, int * SEQ)
{
    int Nc = 1600, i= 0;
    int *X = (int*)calloc(N+Nc, sizeof(int));
    int *Y = (int*)calloc(N+Nc, sizeof(int));
    X[0] = 1;

    while(C_init > 0)
    {
      Y[i++] = (C_init & 1);
      C_init = C_init >> 1;
    }

    for (int k = 0; k < N+Nc-31 ;  k++)
    {
      X[k+31] = (X[k+3] + X[k])%2;
      Y[k+31] = (Y[k+3] + Y[k+2] + Y[k+1] + Y[k])%2;
    }

		for (int k = 0; k < N ;  k++)
    {
			SEQ[k] = (X[k+Nc]+Y[k+Nc])%2;
		}
}

}
}
