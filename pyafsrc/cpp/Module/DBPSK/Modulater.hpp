/*!
 * \file
 * \brief Filters a signal.
 *
 * \section LICENSE
 * This file is under MIT license (https://opensource.org/licenses/MIT).
 */
#ifndef MODULATER
#define MODULATER

#include <vector>

#include "Module/Module.hpp"
#include "Tools/Interface/Interface_reset.hpp"

namespace aff3ct
{
namespace module
{
/*!
 * \class modulater
 *
 * \brief Pi/2 BPSK modulation
 *
 */
class Modulater : public Module
{
protected:
  const int N;
  const int C;

public:
	/*!
	 * \brief Constructor.
	 */
	Modulater(const int N, const int C);

	/*!
	 * \brief Destructor.
	 */
	virtual ~Modulater() = default;

protected:
  virtual void _modulate(const float *U_K1,  float *U_K2, const int frame_id);

};
}
}

#endif /* MODULATER */
