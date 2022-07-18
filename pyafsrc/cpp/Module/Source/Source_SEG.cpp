#include <cstring>
#include <memory>
#include <stdexcept>
#include <cmath>
#include <sstream>

#include "Tools/Exception/exception.hpp"

#include "Module/Source/Source_SEG.hpp"

namespace aff3ct
{
namespace module
{

Source_SEG::
Source_SEG(const int A, const int C)
: Module(), A(A), C(C)
{
	const std::string name = "Source_SEG2";
	this->set_name(name);
	this->set_short_name(name);
	this->set_single_wave(true);


	auto &p1 = this->create_task("generate");
	auto p1s_U_K = this->template create_socket_in <int>(p1, "U_K", this->A);
	auto p1s_V_K = this->template create_socket_out<int>(p1, "V_K", this->A);
	this->create_codelet(p1, [p1s_U_K, p1s_V_K](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<Source_SEG&>(m)._generate(static_cast<int*>(t[p1s_U_K].get_dataptr()),
		                                      static_cast<int*>(t[p1s_V_K].get_dataptr()),
										                      frame_id);

		return 0;
	});
}

void Source_SEG::
_generate(const int *U_K, int *V_K, const int frame_id)
{
	std::memcpy(V_K, U_K, sizeof(int)*this->A);
}

}
}
