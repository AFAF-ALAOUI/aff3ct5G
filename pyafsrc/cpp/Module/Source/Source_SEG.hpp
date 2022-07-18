#ifndef SOURCE_SEG
#define SOURCE_SEG

#include <vector>

#include "Module/Module.hpp"
#include "Tools/Interface/Interface_reset.hpp"

namespace aff3ct
{
namespace module
{
/*!
 * \class Source_SEG
 *
 * \brief sets the last segments to zero.
 *
 */
class Source_SEG : public Module
{
protected:
	const int A;     /*!< Size of one frame (= number of samples in one frame) */
	const int C;     /*!< Number of frames */

public:
	/*!
	 * \brief Constructor.
	 *
	 * \param A:        Size of one frame (= number of samples in one frame)
	 * \param C:        Number of frames
	 */
	Source_SEG(const int A, const int C);

	/*!
	 * \brief Destructor.
	 */
	virtual ~Source_SEG() = default;

protected:
	virtual void _generate(const int *U_K,  int *V_K, const int frame_id);
};
}
}

#endif /* Source_SEG */
