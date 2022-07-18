/*!
 * \file
 * \brief Filters a signal.
 *
 * \section LICENSE
 * This file is under MIT license (https://opensource.org/licenses/MIT).
 */
#ifndef MAPPER
#define MAPPER

#include <vector>

#include "Module/Module.hpp"
#include "Tools/Interface/Interface_reset.hpp"

namespace aff3ct
{
namespace module
{
/*!
 * \class mapper
 *
 * \brief maps symbols into layers
 *
 */
class Mapper : public Module
{
protected:
  const int N;
  const int Nl;
  const int C;

public:
	/*!
	 * \brief Constructor.
	 */
	Mapper(const int N, const int Nl, const int C);

	/*!
	 * \brief Destructor.
	 */
	virtual ~Mapper() = default;

protected:
  virtual void _map(const float *U_K1,  float *U_K2, const int frame_id);
  virtual void _demap(const float *V_K1,  float *V_K2, const int frame_id);

};
}
}

#endif /* MAPPER */
