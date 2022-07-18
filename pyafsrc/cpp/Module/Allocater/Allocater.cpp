#include <cstring>
#include <memory>
#include <stdexcept>
#include <cmath>
#include <sstream>
#include <vector>

#include "Tools/Exception/exception.hpp"

#include "Module/Allocater/Allocater.hpp"

namespace aff3ct
{
namespace module
{

Allocater::
Allocater(const int M, const int Mgrid, const int Na, const int Nr,  const int Nslot, const int Nofdms, const int DMRS_length,
  const int Msc, const int pos1, const int pos2 , const int pos3, const int pos4)
: Module(), M(M), Mgrid(Mgrid), Na(Na), Nr(Nr), Nslot(Nslot), Nofdms(Nofdms), Dl(DMRS_length), Msc(Msc)
{
  int *DMRS_list, *DMRS_TPos, *Data_list;
  int size = 0;

  const std::string name = "Allocater2";
	this->set_name(name);
	this->set_short_name(name);
	this->set_single_wave(true);

  DMRS_list = (int*)calloc(8, sizeof(int));
  this->_DMRS_list(pos1, pos2, pos3, pos4, DMRS_list, &size);
  DMRS_TPos = (int*)calloc(size*this->Nslot, sizeof(int));
  Data_list = (int*)calloc(this->Nofdms-size, sizeof(int));
  this->DataPos = (int*)calloc((this->Nofdms-size)*this->Nslot, sizeof(int));

  this->_DMRSTimePos(DMRS_list, DMRS_TPos, &size);
  this->_Data_list(DMRS_list, &size, Data_list);
  this->_DataTimePos(Data_list, this->DataPos, this->Nofdms-size);

  auto &p1 = this->create_task("allocate");
  auto p1s_U_K = this->template create_socket_in <float>(p1, "B_N", this->M);
  auto p1s_V_K = this->template create_socket_out<float>(p1, "S_N", 2* this->Mgrid * this->Na   );
  this->create_codelet(p1, [p1s_U_K, p1s_V_K](Module &m, Task &t, const size_t frame_id) -> int
  {
    static_cast<Allocater&>(m)._allocate(static_cast<float*>(t[p1s_U_K].get_dataptr()),
                                          static_cast<float*>(t[p1s_V_K].get_dataptr()),
                                          frame_id);

    return 0;
  });

  auto &p2 = this->create_task("extract");
  auto p2s_U_K = this->template create_socket_in <float>(p2, "S_N", 2* this->Mgrid * this->Nr );
  auto p2s_V_K = this->template create_socket_out<float>(p2, "B_N", this->M/this->Na * this->Nr );
  this->create_codelet(p2, [p2s_U_K, p2s_V_K](Module &m, Task &t, const size_t frame_id) -> int
  {
    static_cast<Allocater&>(m)._extract(static_cast<float*>(t[p2s_U_K].get_dataptr()),
                                          static_cast<float*>(t[p2s_V_K].get_dataptr()),
                                          frame_id);

    return 0;
  });


}

void Allocater::
_allocate(const float *B_N, float *S_N, const int frame_id)
{
  int res = this->M/(this->Na) % (2*this->Msc);
  int f = this->M/this->Na;
  for (int n = 0; n < this->Na;  n++)
  {
    for (int i = 0; i < this->M/(this->Na*2*this->Msc) ;  i++)
    {
      std::memcpy(S_N+this->DataPos[i]*2*this->Msc+2*n*this->Mgrid, B_N+i*2*this->Msc+n*f, 2*this->Msc*sizeof(float));

    }
    std::memcpy(S_N+this->DataPos[this->M/(this->Na*2*this->Msc)]*2*this->Msc+2*n*this->Mgrid, B_N+(this->M/(this->Na*2*this->Msc) -1)*2*this->Msc+2*this->Msc+n*f, res*sizeof(float));
  }

}

void Allocater::
_extract(const float *S_N, float *B_N, const int frame_id)
{
  int res = this->M/(this->Na) % (2*this->Msc);
  int f = this->M/this->Na;
  for (int n = 0; n < this->Nr;  n++)
  {
    for (int i = 0; i < this->M/(this->Na*2*this->Msc) ;  i++)
    {
      std::memcpy(B_N+i*2*this->Msc+n*f, S_N+this->DataPos[i]*2*this->Msc+2*n*this->Mgrid, 2*this->Msc*sizeof(float));

    }
    std::memcpy(B_N+(this->M/(this->Na*2*this->Msc))*2*this->Msc+n*f,S_N+this->DataPos[this->M/(this->Na*2*this->Msc)]*2*this->Msc+2*n*this->Mgrid,res*sizeof(float));
  }

}

void Allocater::
_DMRS_list(const int pos1, const int pos2, const int pos3, const int pos4, int *DMRS_list, int * size)
{
  const int tab[4] = {pos1, pos2, pos3, pos4};
  int j= 0;
  for (int i = 0; i < 4 ;  i++)
  {
    if (tab[i] != -1)
    {
      DMRS_list[this->Dl*j] = tab[i];
      DMRS_list[this->Dl*j+1] = tab[i]+1;
      j+=this->Dl;
    }
  }
  *size = j;
}

void Allocater::
_DMRSTimePos(const int *DMRS_list, int *DMRS_TPos, int *size)
{
  for (int k = 0; k < this->Nslot ;  k++)
  {
    for (int i = 0; i < *size ;  i++)
    {
      DMRS_TPos[k+(*size)*i] = DMRS_list[i]+k*this->Nofdms;
    }
  }
}

void Allocater::
_Data_list(int *DMRS_list, int * size, int * Data_l)
{
  int s;
  int j = 0;
  for (int i = 0; i < this->Nofdms ;  i++)
  {
    s=0;
    for (int j = 0; j < *size ;  j++)
    {
      if (i == DMRS_list[j])
      {
        s = 1;
        break;
      }
    }
    if (s==0)
    {
      Data_l[j] = i;
      j++;
    }
  }
}

void Allocater::
_DataTimePos(int *Data_l, int *DataPos, int size)
{
  for (int k = 0; k < this->Nslot ;  k++)
  {
    for (int i = 0; i < size ;  i++)
    {
      DataPos[i+size*k] = Data_l[i]+k*this->Nofdms;
    }
  }
}
}
}
