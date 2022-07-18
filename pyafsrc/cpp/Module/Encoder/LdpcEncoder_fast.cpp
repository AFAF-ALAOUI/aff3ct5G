#include <cstring>
#include <string>
#include <memory>
#include <stdexcept>
#include <cmath>
#include <sstream>
#include <fstream>
#include <vector>
#include <iostream>
#include <algorithm>
#include <numeric>
#include <iterator>
#include <functional>


#include "Tools/Exception/exception.hpp"

#include "Module/Encoder/LdpcEncoder_fast.hpp"

namespace aff3ct
{
namespace module
{

LdpcEncoder_fast::
LdpcEncoder_fast(const int K, const int N, const int BG, const int ils, const int Zc, const int C)
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
	std::vector<int> v(this->Zc);


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

	for (int j = 0; j < this->K/this->Zc ;  j++)
	{
		for (int i = 0; i < (this->N-this->K)/this->Zc ;  i++)
		{
			std::copy(this->G[j].begin()+i*this->Zc, this->G[j].begin()+(i+1)*this->Zc, v.begin());
			this->Rot.push_back(std::vector<int>());
			this->Rot.reserve(this->Rot.empty()?0:this->Rot.front().size());
			this->Rot[i+(this->N-this->K)/this->Zc*j] = _findItems(v, 1);
		}
	}

	auto &p1 = this->create_task("encode");
	auto p1s_U_K = this->template create_socket_in <int>(p1, "U_K", this->K);
	auto p1s_V_K = this->template create_socket_out<int>(p1, "X_N", this->N);
	this->create_codelet(p1, [p1s_U_K, p1s_V_K](Module &m, Task &t, const size_t frame_id) -> int
	{
		static_cast<LdpcEncoder_fast&>(m)._encode(static_cast<int*>(t[p1s_U_K].get_dataptr()),
		                                      static_cast<int*>(t[p1s_V_K].get_dataptr()),
										                      frame_id);

		return 0;
	});


}


std::vector<int> LdpcEncoder_fast::
_findItems(std::vector<int> v, int target)
{
    std::vector<int> indices;
    auto it = v.begin();
    while ((it = std::find_if(it, v.end(),[target] (int &e) { return e == target; }))!= v.end())
    {
        indices.push_back(std::distance(v.begin(), it));
        it++;
    }
    return indices;
}

std::vector<int> LdpcEncoder_fast::
_CSRAA(const int * vect, const int beg)
{

	std::vector<int> info(this->Zc,0);
	std::vector<int> res(this->N-this->K,0);


	for (int i = 0; i < (this->N-this->K)/this->Zc ;  i++)
	{
		for (long unsigned int j = 0; j < this->Rot[i+(this->N-this->K)/this->Zc*beg].size() ;  j++)
	  {
			for (int k = 0; k < this->Zc ;  k++)
			{
				info[k] = vect[k];
			}
			std::rotate(info.begin(), info.end()-this->Rot[i+(this->N-this->K)/this->Zc*beg][j],info.end());
			std::transform (info.begin(), info.end(), res.begin()+i*this->Zc, res.begin()+i*this->Zc, [](int &c, int&b){return (c+b)%2; });
		}
	}
	return res;
}



void LdpcEncoder_fast::
_encode(const int *U_K, int *X_N, const int frame_id)
{

	for (int c = 0; c < this->C ;  c++)
	{
		memcpy(X_N+c*this->N,U_K+c*this->K,sizeof(int)*this->K);
		std::vector<int> vect(this->N-this->K,0);

		for (int i = 0; i < this->K/this->Zc ;  i++)
		{
			std::vector<int> res = this->_CSRAA(U_K+i*this->Zc+c*this->K, i);
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
