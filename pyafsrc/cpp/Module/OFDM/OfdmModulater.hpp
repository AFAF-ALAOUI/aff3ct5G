#ifndef OFDMMODULATER
#define OFDMMODULATER

#include <vector>
#include <armadillo>

#include "Module/Module.hpp"
#include "Tools/Interface/Interface_reset.hpp"

namespace aff3ct
{
namespace module
{
/*!
 * \class OfdmModulater
 *
 * \briefs OFDM Modulation.
 *
 */
class OfdmModulater : public Module
{
protected:
  const int Mgrid;
  const int Na;
  const int Nr;
  const int Msc;
  const int Nifft;
  const int k0;

public:
	/*!

	 */
	OfdmModulater(const int Mgrid, const int Na, const int Nr,  const int Msc,  const int Nifft,  const int k0);

  /*!
	 * \brief Destructor.
	 */
	virtual ~OfdmModulater() = default;

protected:
  virtual void _modulate(const float *X_N,  float *Y_N, const int frame_id);
	virtual void _demodulate(const float *Y_N,  float *X_N, const int frame_id);

};
}
}
#endif /*OfdmModulater */
