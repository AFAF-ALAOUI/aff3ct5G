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

#include "Module/Puncturer/Puncturer.hpp"

namespace aff3ct
{
namespace module
{

Puncturer::
Puncturer(const int C, const int Kp, const int K, const int N,  const int E1, const int E2, const int f,  const int Zc,  const int stp)
: Module(), C(C), Kp(Kp), K(K), N(N), E1(E1), E2(E2), f(f), Zc(Zc), stp(stp)
{
	const std::string name = "Puncturer2";
	this->set_name(name);
	this->set_short_name(name);
	this->set_single_wave(true);

	auto &p1 = this->create_task("puncture");
	auto p1s_U_K = this->template create_socket_in <int>(p1, "D_K", this->N    );
	auto p1s_V_K = this->template create_socket_out<int>(p1, "D", this->E2);
	this->create_codelet(p1, [p1s_U_K, p1s_V_K](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Puncturer&>(m)._puncture(static_cast<int*>(t[p1s_U_K].get_dataptr()),
		                                      static_cast<int*>(t[p1s_V_K].get_dataptr()),
										                      frame_id);

		return 0;
	});

  auto &p2 = this->create_task("recover");
	auto p2s_U_K = this->template create_socket_in <int>(p2, "D", this->E2 );
	auto p2s_V_K = this->template create_socket_out<int>(p2, "D_K", this->N );
	this->create_codelet(p2, [p2s_U_K, p2s_V_K](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Puncturer&>(m)._recover(static_cast<int*>(t[p2s_U_K].get_dataptr()),
		                                      static_cast<int*>(t[p2s_V_K].get_dataptr()),
										                      frame_id);

		return 0;
	});

	auto &p3 = this->create_task("recoverLLR");
	auto p3s_U_K = this->template create_socket_in <float>(p3, "D", this->E2 );
	auto p3s_V_K = this->template create_socket_out<float>(p3, "D_K", this->N );
	this->create_codelet(p3, [p3s_U_K, p3s_V_K](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Puncturer&>(m)._recoverLLR(static_cast<float*>(t[p3s_U_K].get_dataptr()),
		                                      static_cast<float*>(t[p3s_V_K].get_dataptr()),
										                      frame_id);

		return 0;
	});


}

void Puncturer::
_puncture(int *D_K, int *D, const int frame_id)
{
	int k,j,E = this->E2;
	for (int c = 0; c < this->C ;  c++){
		k = 0;
	  j = 0;
		if (c < this->f) E = this->E1;
	  while(k < E)
		{
			if (!((stp+j)%(N-2*Zc) + 2*Zc < K && Kp <=(stp+j)%(N-2*Zc) + 2*Zc))
			{
				D[k+c*this->E2] = D_K[(stp+j)%(N-2*Zc) + 2*Zc+c*this->N];
				k++;
			}
	    j++;
		}
	}
}

void Puncturer::
_recover(int *D, int *D_K, const int frame_id)
{
	int k,j,E= this->E2;
	for (int c = 0; c < this->C ;  c++){
		k = 0;
	  j = 0;
		if (c < this->f) E = this->E1;
		while(k < E)
		{
			if (!((stp+j)%(N-2*Zc) + 2*Zc < K && Kp <=(stp+j)%(N-2*Zc) + 2*Zc))
			{
				D_K[(stp+j)%(N-2*Zc) + 2*Zc+c*this->N] = D[k+c*this->E2];
				k++;
			}
	    j++;
		}
	}
}

void Puncturer::
_recoverLLR(float *D, float *D_K, const int frame_id)
{
	int k,j,E= this->E2;
	for (int c = 0; c < this->C ;  c++){
		k = 0;
	  j = 0;
		if (c < this->f) E = this->E1;
		while(k < E)
		{
			if (!((stp+j)%(N-2*Zc) + 2*Zc < K && Kp <=(stp+j)%(N-2*Zc) + 2*Zc))
			{
				D_K[(stp+j)%(N-2*Zc) + 2*Zc+c*this->N] = D[k+c*this->E2];
				k++;
			}
	    j++;
		}
		std::memset(D_K+c*this->N, 0, sizeof(float)*2*Zc);
		std::memset(D_K+c*this->N+this->Kp, 100, sizeof(float)*(this->K-this->Kp));
	}
}

}
}
