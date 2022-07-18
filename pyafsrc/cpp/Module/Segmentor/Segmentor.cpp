#include <cstring>
#include <memory>
#include <stdexcept>
#include <cmath>
#include <sstream>

#include "Tools/Exception/exception.hpp"

#include "Module/Segmentor/Segmentor.hpp"

namespace aff3ct
{
namespace module
{

Segmentor::
Segmentor(const int B, const int C)
: Module(), B(B), C(C)
{
	const std::string name = "Segmentor2";
	this->set_name(name);
	this->set_short_name(name);
	this->set_single_wave(true);


	auto &p1 = this->create_task("segment");
	auto p1s_U_K = this->template create_socket_in <int>(p1, "B_K", this->B);
	auto p1s_V_K = this->template create_socket_out<int>(p1, "C_K", this->B/this->C);
	this->create_codelet(p1, [p1s_U_K, p1s_V_K](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Segmentor&>(m)._segment(static_cast<int*>(t[p1s_U_K].get_dataptr()),
		                                      static_cast<int*>(t[p1s_V_K].get_dataptr()),
										                      frame_id);

		return 0;
	});

  auto &p2 = this->create_task("concatenate");
	auto p2s_U_K = this->template create_socket_in <int>(p2, "C_K", ceil(this->B/this->C));
	auto p2s_V_K = this->template create_socket_out<int>(p2, "B_K", this->B    );
	this->create_codelet(p2, [p2s_U_K, p2s_V_K](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Segmentor&>(m)._concatenate(static_cast<int*>(t[p2s_U_K].get_dataptr()),
		                                      static_cast<int*>(t[p2s_V_K].get_dataptr()),
										                      frame_id);

		return 0;
	});
}

void Segmentor::
_segment(const int *B_K, int *C_K, const int frame_id)
{
	std::memcpy(C_K, B_K, sizeof(int)*this->B);
}

void Segmentor::
_concatenate(const int *C_K, int *B_K, const int frame_id)
{
	std::memcpy(B_K, C_K, sizeof(int)*this->B);
}



}
}
