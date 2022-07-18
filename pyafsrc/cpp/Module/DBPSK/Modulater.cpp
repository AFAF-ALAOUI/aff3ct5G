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

#include "Module/DBPSK/Modulater.hpp"

namespace aff3ct
{
namespace module
{

Modulater::
Modulater(const int N, const int C)
: Module(), N(N), C(C)
{
	const std::string name = "Modulater2";
	this->set_name(name);
	this->set_short_name(name);
	this->set_single_wave(true);

  auto &p1 = this->create_task("pimodulate");
	auto p1s_X_N1 = this->template create_socket_in <float>(p1, "U_K1", this->N);
	auto p1s_Y_N2 = this->template create_socket_out<float>(p1, "U_K2", this->N);
	this->create_codelet(p1, [p1s_X_N1, p1s_Y_N2](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Modulater&>(m)._modulate(static_cast<float*>(t[p1s_X_N1].get_dataptr()),
		                                           static_cast<float*>(t[p1s_Y_N2].get_dataptr()),
										frame_id);

		return 0;
	});


	auto &p2 = this->create_task("pidemodulate");
	auto p2s_X_N1 = this->template create_socket_in <float>(p2, "U_K2", this->N);
	auto p2s_Y_N2 = this->template create_socket_out<float>(p2, "U_K1", this->N);
	this->create_codelet(p2, [p2s_X_N1, p2s_Y_N2](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Modulater&>(m)._modulate(static_cast<float*>(t[p2s_X_N1].get_dataptr()),
																							 static_cast<float*>(t[p2s_Y_N2].get_dataptr()),
										frame_id);

		return 0;
	});
}

void Modulater::
_modulate(const float *U_K1, float *U_K2, const int frame_id)
{
  std::memcpy(U_K2, U_K1, sizeof(float)*this->N);
  for (int c = 0; c < this->C ;  c++)
  {
    for (int k = 2; k < this->N ;  k+=4)
    {
      U_K2[k+c*this->N] = -U_K1[k+c*this->N];
    }
  }
}

}
}
