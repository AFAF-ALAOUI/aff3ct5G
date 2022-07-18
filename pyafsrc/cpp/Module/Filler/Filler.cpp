#include <cstring>
#include <memory>
#include <stdexcept>
#include <cmath>
#include <sstream>

#include "Tools/Exception/exception.hpp"

#include "Module/Filler/Filler.hpp"

namespace aff3ct
{
namespace module
{

Filler::
Filler(const int Kp, const int K, const int C)
: Module(), Kp(Kp), K(K), C(C)
{
	const std::string name = "Filler2";
	this->set_name(name);
	this->set_short_name(name);
	this->set_single_wave(true);

  auto &p1 = this->create_task("fill");
  auto p1s_U_K = this->template create_socket_in <int>(p1, "C_K1", this->Kp    );
  auto p1s_V_K = this->template create_socket_out<int>(p1, "C_K2", this->K    );
  this->create_codelet(p1, [p1s_U_K, p1s_V_K](Module &m, Task &t, const size_t frame_id) -> int
  {
    static_cast<Filler&>(m)._fill(static_cast<int*>(t[p1s_U_K].get_dataptr()),
                                          static_cast<int*>(t[p1s_V_K].get_dataptr()),
                                          frame_id);

    return 0;
  });

  auto &p2 = this->create_task("shorten");
  auto p2s_U_K = this->template create_socket_in <int>(p2, "C_K2", this->K    );
  auto p2s_V_K = this->template create_socket_out<int>(p2, "C_K1", this->Kp    );
  this->create_codelet(p2, [p2s_U_K, p2s_V_K](Module &m, Task &t, const size_t frame_id) -> int
  {
    static_cast<Filler&>(m)._shorten(static_cast<int*>(t[p2s_U_K].get_dataptr()),
                                          static_cast<int*>(t[p2s_V_K].get_dataptr()),
                                          frame_id);

    return 0;
  });


}

void Filler::
_fill(const int *C_K1, int *C_K2, const int frame_id)
{
  for (int c = 0; c < this->C ;  c++)
	{
		std::memcpy(C_K2+c*this->K, C_K1+c*this->Kp, sizeof(int)*this->Kp);
	}

}

void Filler::
_shorten(const int *C_K2, int *C_K1, const int frame_id)
{
  for (int c = 0; c < this->C ;  c++)
	{
		std::memcpy(C_K1+c*this->Kp, C_K2+c*this->K, sizeof(int)*this->Kp);
	}
}
}
}
