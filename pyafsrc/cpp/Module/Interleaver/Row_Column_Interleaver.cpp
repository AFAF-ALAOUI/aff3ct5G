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

#include "Module/Interleaver/Row_Column_Interleaver.hpp"

namespace aff3ct
{
namespace module
{

Row_Column_Interleaver::
Row_Column_Interleaver(const int E1, const int E2, const int f, const int Qm, const int G, const int C)
: Module(), E1(E1), E2(E2), f(f), Qm(Qm), G(G), C(C)
{
	const std::string name = "Interleaver2";
	this->set_name(name);
	this->set_short_name(name);
	this->set_single_wave(true);


	auto &p1 = this->create_task("interleave");
	auto p1s_U_K = this->template create_socket_in <int>(p1, "U_K", this->E2);
	auto p1s_V_K = this->template create_socket_out<int>(p1, "itl", this->G);
	this->create_codelet(p1, [p1s_U_K, p1s_V_K](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Row_Column_Interleaver&>(m)._interleave(static_cast<int*>(t[p1s_U_K].get_dataptr()),
		                                      static_cast<int*>(t[p1s_V_K].get_dataptr()),
										                      frame_id);

		return 0;
	});

	auto &p2 = this->create_task("deinterleave");
	auto p2s_U_K = this->template create_socket_in <int>(p2, "itl", this->G);
	auto p2s_V_K = this->template create_socket_out<int>(p2, "U_K", this->E2);
	this->create_codelet(p2, [p2s_U_K, p2s_V_K](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Row_Column_Interleaver&>(m)._deinterleave(static_cast<int*>(t[p2s_U_K].get_dataptr()),
		                                      static_cast<int*>(t[p2s_V_K].get_dataptr()),
										                      frame_id);

		return 0;
	});

	auto &p3 = this->create_task("deinterleaveLLR");
	auto p3s_U_K = this->template create_socket_in <float>(p3, "itl", this->G);
	auto p3s_V_K = this->template create_socket_out<float>(p3, "U_K", this->E2);
	this->create_codelet(p3, [p3s_U_K, p3s_V_K](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Row_Column_Interleaver&>(m)._deinterleaveLLR(static_cast<float*>(t[p3s_U_K].get_dataptr()),
		                                      static_cast<float*>(t[p3s_V_K].get_dataptr()),
										                      frame_id);

		return 0;
	});
}

void Row_Column_Interleaver::
_interleave(const int *U_K, int *V_K, const int frame_id)
{
	int E = this->E2;
	for (int c = 0; c < this->C ; c++)
	{
		if (c < this->f) E = this->E1;
    for (int j = 0; j < E/this->Qm ; j++)
		{
			for (int i = 0; i < this->Qm ; i++)
			{
				V_K[c*E + i + j*this->Qm] = U_K[c*this->E2 + i*E/this->Qm + j];
			}
		}
	}

}

void Row_Column_Interleaver::
_deinterleave(const int *V_K, int *U_K, const int frame_id)
{

	int E = this->E2;
	for (int c = 0; c < this->C ; c++)
	{
		if (c < this->f) E = this->E1;
    for (int j = 0; j < E/this->Qm ; j++)
		{
			for (int i = 0; i < this->Qm ; i++)
			{
				U_K[c*this->E2 + i*E/this->Qm + j] = V_K[c*E + i + j*this->Qm];
			}
		}
	}

}

void Row_Column_Interleaver::
_deinterleaveLLR(const float *V_K, float *U_K, const int frame_id)
{

	int E = this->E2;
	for (int c = 0; c < this->C ; c++)
	{
		if (c < this->f) E = this->E1;
    for (int j = 0; j < E/this->Qm ; j++)
		{
			for (int i = 0; i < this->Qm ; i++)
			{
				U_K[c*this->E2 + i*E/this->Qm + j] = V_K[c*E + i + j*this->Qm];
			}
		}
	}

}


}
}
