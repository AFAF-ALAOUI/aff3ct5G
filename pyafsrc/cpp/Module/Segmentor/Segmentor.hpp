#ifndef SEGMENTOR
#define SEGMENTOR

#include <vector>

#include "Module/Module.hpp"
#include "Tools/Interface/Interface_reset.hpp"

namespace aff3ct
{
namespace module
{
/*!
 * \class Segmentor
 *
 * \brief segments the first frame into C frames.
 *
 */
class Segmentor : public Module
{
protected:
	const int B;     /*!< Size of one frame before segmentation (= number of samples in one frame) */
	const int C;     /*!< Number of frames */

public:
	/*!
	 * \brief Constructor.
	 *
	 * \param A:        Size of one frame before segmentation(= number of samples in one frame)
	 * \param C:        Number of frames
	 */
	Segmentor(const int B, const int C);

	/*!
	 * \brief Destructor.
	 */
	virtual ~Segmentor() = default;

protected:
	virtual void _segment(const int *B_K,  int *C_K, const int frame_id);
	virtual void _concatenate(const int *C_K,  int *B_K, const int frame_id);
};
}
}

#endif /* Segmentor */
