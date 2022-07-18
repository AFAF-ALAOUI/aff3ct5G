/*!
 * \file
 * \brief Filters a signal.
 *
 * \section LICENSE
 * This file is under MIT license (https://opensource.org/licenses/MIT).
 */
#ifndef SCRAMBLER
#define SCRAMBLER

#include <vector>

#include "Module/Module.hpp"
#include "Tools/Interface/Interface_reset.hpp"

namespace aff3ct
{
namespace module
{
/*!
 * \class scrambler
 *
 * \brief scrambles the signal.
 *
 */
class Scrambler : public Module
{
protected:
  const int G;
  const int C_init;
	int * SEQ;

public:
	/*!
	 * \brief Constructor.
	 */
	Scrambler(const int G, const int C_init);

	/*!
	 * \brief Destructor.
	 */
	virtual ~Scrambler() = default;

protected:
  virtual void _scramble(const int *S_K1,  int *S_K2, const int frame_id);
	virtual void _descrambleLLR(const float *S_K2,  float *S_K1, const int frame_id);
  virtual void _Goldseq31(const int N, int C_init, int * SEQ);
};
}
}

#endif /* SCRAMBLER */
