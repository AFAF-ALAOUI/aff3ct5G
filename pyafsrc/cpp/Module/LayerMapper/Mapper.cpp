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

#include "Module/LayerMapper/Mapper.hpp"

namespace aff3ct
{
namespace module
{

Mapper::
Mapper(const int N, const int Nl, const int C)
: Module(), N(N), Nl(Nl), C(C)
{
	const std::string name = "LayerMapper2";
	this->set_name(name);
	this->set_short_name(name);
	this->set_single_wave(true);

  auto &p1 = this->create_task("map");
	auto p1s_X_N1 = this->template create_socket_in <float>(p1, "U_K1", this->N);
	auto p1s_Y_N2 = this->template create_socket_out<float>(p1, "U_K2", this->N);
	this->create_codelet(p1, [p1s_X_N1, p1s_Y_N2](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Mapper&>(m)._map(static_cast<float*>(t[p1s_X_N1].get_dataptr()),
		                                           static_cast<float*>(t[p1s_Y_N2].get_dataptr()),
										frame_id);

		return 0;
	});


	auto &p2 = this->create_task("demap");
	auto p2s_X_N1 = this->template create_socket_in <float>(p2, "V_K1", this->N);
	auto p2s_Y_N2 = this->template create_socket_out<float>(p2, "V_K2", this->N);
	this->create_codelet(p2, [p2s_X_N1, p2s_Y_N2](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Mapper&>(m)._demap(static_cast<float*>(t[p2s_X_N1].get_dataptr()),
																							 static_cast<float*>(t[p2s_Y_N2].get_dataptr()),
										frame_id);

		return 0;
	});
}

void Mapper::
_map(const float *U_K1, float *U_K2, const int frame_id)
{
  for (int i = 0; i < this->Nl ;  i++)
  {
    for (int j = 0; j < this->N/this->Nl ;  j++)
    {
      U_K2[i*this->N/this->Nl+j] = U_K1[i+ j*this->Nl];
    }
  }

}

void Mapper::
_demap(const float *V_K1, float *V_K2, const int frame_id)
{

  for (int i = 0; i < this->Nl ;  i++)
  {
    for (int j = 0; j < this->N/this->Nl ;  j++)
    {
      V_K2[i+ j*this->Nl] = V_K1[i*this->N/this->Nl+j];
    }
  }


}

}
}
