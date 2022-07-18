#ifndef FILLER
#define FILLER

#include <vector>

#include "Module/Module.hpp"
#include "Tools/Interface/Interface_reset.hpp"

namespace aff3ct
{
namespace module
{
/*!
 * \class Filler
 *
 * \brief inserts filler bits.
 *
 */
class Filler : public Module
{
protected:
	const int Kp;     /*!< Size of one input frame (= number of samples in one frame) */
  const int K;      /*!< Size of one output frame */
	const int C;      /*!< Number of frames */

public:
	/*!
	 * \brief Constructor.
	 *
	 * \param Kp:      Size of one input frame (= number of samples in one frame)
   * \param K:       Size of one output frame
	 * \param C:       Number of frames
	 */
	Filler(const int Kp, const int K, const int C);

  /*!
	 * \brief Destructor.
	 */
	virtual ~Filler() = default;

protected:
  virtual void _fill(const int *C_K1,  int *C_K2, const int frame_id);
	virtual void _shorten(const int *C_K2,  int *C_K1, const int frame_id);

};
}
}
#endif /* Filler */
