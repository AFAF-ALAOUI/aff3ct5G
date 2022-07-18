

#ifndef PUNCTURER
#define PUNCTURER

#include <vector>

#include "Module/Module.hpp"
#include "Tools/Interface/Interface_reset.hpp"

namespace aff3ct
{
namespace module
{
/*!
 * \class Puncturer
 *
 * \brief rate matching block
 *
 */
class Puncturer : public Module
{
protected:
	const int C;               /*!< Number of frames*/
	const int Kp;              /*!< Size of one frame before encoding */
	const int K;               /*!< Size of one frame before encoding */
  const int N;               /*!< Size of one input frame*/
  const int E1;              /*!< Size of the first output frames */
  const int E2;              /*!< Size of the last output frames */
  const int f;               /*!< Number of frames of size E1 */
  const int Zc;              /*!< Lifting size */
	const int stp;             /*!< starting position */

public:
	/*!
	 * \brief Constructor.
	 */
	Puncturer(const int C, const int Kp, const int K, const int N, const int E1, const int E2, const int f, const int Zc,  const int stp);

  /*!
	 * \brief Destructor.
	 */
	virtual ~Puncturer() = default;

protected:
  virtual void _puncture(int *D_K,  int * D, const int frame_id);
	virtual void _recover(int *D,  int *D_K, const int frame_id);
	virtual void _recoverLLR(float *D,  float *D_K, const int frame_id);

};
}
}
#endif /* Puncturer */
