#ifndef PRECODER
#define PRECODER


#include <vector>
#include <complex>
#include <armadillo>

#include "Module/Module.hpp"
#include "Tools/Interface/Interface_reset.hpp"

using namespace arma;

namespace aff3ct
{
namespace module
{
/*!
 * \class Precoder
 *
 * \brief
 */
class Precoder : public Module
{
protected:
	const int Nb;       /*!< Bit Length */
  const int Nl;       /*!< Number of layers */
  const int Na;       /*!< Number of transmit antennas */
  const int TPMI;     /*!< Matrix index*/
  const int val;      /*!< Transform precoding flag */
	cx_fmat W;


public:
	/*!
	 * \brief Constructor.
	 */
	Precoder(const int Nb, const int Nl, const int Na, const int TPMI, const int val);

	/*!
	 * \brief Destructor.
	 */
	virtual ~Precoder() = default;

protected:
  virtual void _precode(const float *U_K1,  float *U_K2, const int frame_id);
	virtual void _decode(const float *V_K1,  float *V_K2, const int frame_id);
  virtual void _precoding_matrix();
};
}
}

#endif /* Precoder */
