#include <cstring>
#include <string>
#include <memory>
#include <stdexcept>
#include <cmath>
#include <sstream>
#include <fstream>


#include "Tools/Exception/exception.hpp"

#include "Module/Encoder/LdpcEncoder.hpp"

namespace aff3ct
{
namespace module
{

LdpcEncoder::
LdpcEncoder(const int K, const int N, const int BG, const int ils, const int Zc, const int C)
: Module(), K(K), N(N), BG(BG), ils(ils), Zc(Zc), C(C)
{
	const std::string name = "LdpcEncoder2";
	this->set_name(name);
	this->set_short_name(name);
	this->set_single_wave(true);

	std::ifstream fichier("/home/afaf/Bureau/pyaf/py_aff3ct/Test/LDPC/gen_matrices/NR_"+std::to_string(this->BG)+"_"+std::to_string(this->ils)
	+"_"+std::to_string(this->Zc)+".txt", std::ios::in);
	std::string ligne;
	std::istream_iterator<int> stream_end;
	if(fichier)
	{
		while(getline(fichier, ligne))
		{
			this->G.push_back(std::vector<int>());
			this->G.reserve(this->G.empty()?0:this->G.front().size());
			std::istringstream ligne_stream(ligne);
			std::copy(std::istream_iterator<int>(ligne_stream), stream_end, std::back_inserter(this->G.back()));
		}
	}

	auto &p1 = this->create_task("encode");
	auto p1s_U_K = this->template create_socket_in <int>(p1, "U_K", this->K);
	auto p1s_V_K = this->template create_socket_out<int>(p1, "X_N", this->N);
	this->create_codelet(p1, [p1s_U_K, p1s_V_K](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<LdpcEncoder&>(m)._encode(static_cast<int*>(t[p1s_U_K].get_dataptr()),
		                                      static_cast<int*>(t[p1s_V_K].get_dataptr()),
										                      frame_id);

		return 0;
	});


}

void LdpcEncoder::
_MultiplyAdd(std::vector<int>&v, int k, std::vector<int>&r){
    std::vector<int> i(v.size(),0);
    std::transform(v.begin(), v.end(), i.begin(), [k](int &c){ return c*k; });
    std::transform (i.begin(), i.end(), r.begin(), r.begin(), [](int &c, int&b){return (c+b)%2; });
}



std::vector<int> LdpcEncoder::
 _CSRAA(const int Zc, std::vector<int> Gen, const int * vect, const int K, const int N)
{
  int u;
  std::vector<int> res(N-K,0);

  for (int i = 0; i < Zc ;  i++)
  {
    u = vect[i];
    this->_MultiplyAdd(Gen, u, res);
    for (int j = 0; j < (N-K)/Zc ;  j++)
    {
      std::rotate(Gen.begin()+j*Zc, Gen.begin()+(j+1)*Zc-1,Gen.begin()+(j+1)*Zc);
    }
  }
  return res;
}



void LdpcEncoder::
_encode(const int *U_K, int *X_N, const int frame_id)
{
	for (int c = 0; c < this->C ;  c++)
	{
		memcpy(X_N+c*this->N,U_K+c*this->K,sizeof(int)*this->K);
		std::vector<int> vect(this->N-this->K,0);

		for (int i = 0; i < this->K/this->Zc ;  i++)
		{
			std::vector<int> res = this->_CSRAA(this->Zc, this->G[i], U_K+i*this->Zc+c*this->K, this->K, this->N);
			std::transform (vect.begin(), vect.end(), res.begin(), vect.begin(), [](int &c, int&b){return (c+b)%2; });
		}

		for (int i = this->K; i < this->N ;  i++)
		{
			X_N[i+c*this->N]=vect[i-this->K];
		}

	}

}

}
}
