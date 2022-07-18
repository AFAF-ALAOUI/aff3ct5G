#ifndef ALLOCATER
#define ALLOCATER

#include <vector>

#include "Module/Module.hpp"
#include "Tools/Interface/Interface_reset.hpp"

namespace aff3ct
{
namespace module
{
/*!
 * \class Allocater
 *
 * \briefs allocates ressources for data and DMRS signal.
 *
 */
class Allocater : public Module
{
protected:
  const int M;
  const int Mgrid;
  const int Na;
  const int Nr;
  const int Nslot;
  const int Nofdms;
  const int Dl;
  const int Msc;
	int * DataPos;

public:
	/*!

	 */
	Allocater(const int M, const int Mgrid, const int Na, const int Nr, const int Nslot, const int Nofdms, const int DMRS_length,
    const int Msc, const int pos1, const int pos2 , const int pos3, const int pos4);

  /*!
	 * \brief Destructor.
	 */
	virtual ~Allocater() = default;

protected:
  virtual void _allocate(const float *B_N,  float *S_N, const int frame_id);
	virtual void _extract(const float *S_N,  float *B_N, const int frame_id);

public:
  virtual void _DMRS_list(const int pos1, const int pos2, const int pos3, const int pos4, int *DMRS_list, int *size);
  virtual void _DMRSTimePos(const int *DMRS_list, int *DMRS_TPos, int *size);
  virtual void _DataTimePos(int *Data_l, int *DataPos, int size);
  virtual void _Data_list(int *DMRS_list, int * size, int * Data_l);

};
}
}
#endif /*Allocater */
